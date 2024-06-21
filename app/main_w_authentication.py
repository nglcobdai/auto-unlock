#!/usr/bin/env python

import asyncio
import json
import os
import time
import wave
from datetime import datetime
import logging
from logging import Formatter, StreamHandler, getLogger, DEBUG

import dotenv
import numpy as np
import pyaudio
import pytz
import requests

dotenv.load_dotenv()

# 環境変数からログレベルを取得
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "DEBUG").upper()
numeric_level = getattr(logging, LOGGING_LEVEL, DEBUG)

RATE = int(os.getenv("AUDIO_RATE"))
CHUNK = int(os.getenv("AUDIO_CHUNK"))
THRESHOLD = float(os.getenv("AUDIO_THRESHOLD"))
CHANNELS = int(os.getenv("AUDIO_CHANNELS"))
AUTO_UNLOCK_API_URL = os.getenv("AUTO_UNLOCK_API_URL")
CONSECUTIVE_SEC_THRESHOLD = float(os.getenv("CONSECUTIVE_SEC_THRESHOLD"))
CONSECUTIVE_SEC_RATE = float(os.getenv("CONSECUTIVE_SEC_RATE"))
INTERVAL_SEC_THRESHOLD = int(os.getenv("INTERVAL_SEC_THRESHOLD"))
FORMAT = pyaudio.paInt16

CONSECUTIVE_FRAMES_THRESHOLD = (
    int(CONSECUTIVE_SEC_THRESHOLD) * (RATE / CHUNK) * CONSECUTIVE_SEC_RATE
)
INTERVAL_FRAMES_THRESHOLD = int(INTERVAL_SEC_THRESHOLD) * (RATE / CHUNK)

logger = getLogger(__name__)

JST = pytz.timezone("Asia/Tokyo")


# タイムゾーンを日本時間に設定するためのカスタム関数
def jst_time(*args):
    return datetime.now(JST).timetuple()


def set_logger():
    # 全体のログ設定
    root_logger = getLogger()
    root_logger.setLevel(numeric_level)

    # コンソール出力のためのハンドラを設定
    console_handler = StreamHandler()
    format = Formatter("%(asctime)s : %(levelname)s : %(filename)s - %(message)s")
    format.converter = jst_time  # 日本時間を使用するように設定
    console_handler.setFormatter(format)

    # ルートロガーにコンソールハンドラを追加
    root_logger.addHandler(console_handler)


class AutoUnlockApp:

    def __init__(self):
        logger.info("Start AutoUnlockApp.")
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )

        self.consecutive_frames = 0
        self.interval_frames = INTERVAL_FRAMES_THRESHOLD
        self.is_phrase_authorized = False
        self.is_retry = False

    def __call__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.record_loop())

    async def record_loop(self):
        while self.stream.is_active():
            try:
                x = self.fetch_audio_data()
                if self.is_unlock_event(x):
                    logger.info("Unlock event detected.")
                    await self.recording()
                    await self.event(is_file=True)
                elif self.is_event_call(x):
                    await self.event()
                elif x.max() > THRESHOLD:
                    self.consecutive_frames += 1
                else:
                    self.consecutive_frames = 0
                self.interval_frames += 1
            except KeyboardInterrupt:
                break
        self.__del__()

    def fetch_audio_data(self):
        data = self.stream.read(CHUNK)
        x = np.frombuffer(data, dtype="int16") / 32768.0
        return x

    def is_event_call(self, x):
        return (
            (x.max() > THRESHOLD)
            and (self.consecutive_frames >= CONSECUTIVE_FRAMES_THRESHOLD)
            and (self.interval_frames >= INTERVAL_FRAMES_THRESHOLD)
        )

    def is_unlock_event(self, x):
        return ((x.max() > THRESHOLD) or self.is_retry) and self.is_phrase_authorized

    def post_api(self, is_file=False):
        if not is_file:
            response = requests.post(AUTO_UNLOCK_API_URL)
        else:
            files = {"file": ("test.wav", open("out/record.wav", "rb"), "audio/wav")}
            response = requests.post(AUTO_UNLOCK_API_URL, files=files)

        return json.loads(response.text)

    async def event(self, is_file=False):
        logger.info(f"Event detected. is_file: {is_file}")
        response = self.post_api(is_file)
        logger.info(response)

        if response["phrase_authorized"]:
            self.is_phrase_authorized = True
            self.is_retry = is_file
        else:
            self.is_phrase_authorized = False
            self.is_retry = False
            self.consecutive_frames = 0
            self.interval_frames = 0

    def __del__(self):
        logger.info("End AutoUnlockApp.")
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    async def recording(self, duration=3):
        """
        Records audio for a given duration and saves it as a WAV file.

        Parameters:
        duration (int): The duration of the recording in seconds. Default is 2 seconds.
        output_filename (str): The name of the output WAV file. Default is 'test.wav'.
        """
        logger.info("Start recording.")
        frames = []

        # 録音
        for _ in range(0, int(RATE / CHUNK * duration)):
            data = self.stream.read(CHUNK)
            frames.append(data)
            time.sleep(CHUNK / RATE)  # 適切な遅延を追加

        # 録音データをwaveファイルに保存
        output_dir = "./out"
        os.makedirs(output_dir, exist_ok=True)
        wf = wave.open(os.path.join(output_dir, "record.wav"), "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
        wf.close()

        logger.info("End recording.")


def main():
    set_logger()
    app = AutoUnlockApp()
    app()


if __name__ == "__main__":
    main()
