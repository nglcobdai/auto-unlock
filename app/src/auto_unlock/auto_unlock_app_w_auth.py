#!/usr/bin/env python

import asyncio
import json
import os
import time
import wave

import numpy as np
import requests

from app.src.auto_unlock import AutoUnlockApp
from app.utils import logger, settings, slack


class AutoUnlockAppWAuth(AutoUnlockApp):
    def __init__(self):
        logger.info("Start AutoUnlockAppWAuth.")
        super(AutoUnlockAppWAuth, self).__init__()

        self.auto_unlock_api_url = settings.AUTO_UNLOCK_API_URL

        self.rate = settings.RATE
        self.format = settings.FORMAT
        self.channels = settings.CHANNELS
        self.duration = settings.DURATION
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
                elif x.max() > self.threshold:
                    self.consecutive_frames += 1
                else:
                    self.consecutive_frames = 0
                self.interval_frames += 1
            except KeyboardInterrupt:
                logger.warning("KeyboardInterrupt.")
                slack.post_text(
                    channel=settings.SLACK_CHANNEL, text=logger.get_log_message()
                )
                break
        self.__del__()

    def fetch_audio_data(self):
        data = self.stream.read(self.chunk)
        x = np.frombuffer(data, dtype="int16") / 32768.0
        return x

    def is_event_call(self, x):
        return (
            (x.max() > self.threshold)
            and (self.consecutive_frames >= self.consecutive_frames_threshold)
            and (self.interval_frames >= self.interval_frames_threshold)
        )

    def is_unlock_event(self, x):
        return (
            (x.max() > self.threshold) or self.is_retry
        ) and self.is_phrase_authorized

    def post_api(self, is_file=False):
        if not is_file:
            response = requests.post(self.auto_unlock_api_url)
        else:
            files = {"file": ("test.wav", open("out/record.wav", "rb"), "audio/wav")}
            response = requests.post(self.auto_unlock_api_url, files=files)

        return json.loads(response.text)

    async def event(self, is_file=False):
        logger.info(f"Event detected. is_file: {is_file}")
        response = self.post_api(is_file)

        if response["phrase_authorized"]:
            self.is_phrase_authorized = True
            self.is_retry = is_file
            logger.info("Auto Unlock API response: Success Call available.")
        else:
            self.is_phrase_authorized = False
            self.is_retry = False
            self.consecutive_frames = 0
            self.interval_frames = 0
            logger.info("Auto Unlock API response: Success Auto Unlock.")

    async def recording(self):
        """
        Records audio for a given duration and saves it as a WAV file.

        Parameters:
        duration (int): The duration of the recording in seconds. Default is 2 seconds.
        output_filename (str): The name of the output WAV file. Default is 'test.wav'.
        """
        logger.info("Start recording to file.")
        frames = []

        # 録音
        for _ in range(0, int(self.rate / self.chunk * self.duration)):
            data = self.stream.read(self.chunk)
            frames.append(data)
            time.sleep(self.chunk / self.rate)  # 適切な遅延を追加

        # 録音データをwaveファイルに保存
        output_dir = "./out"
        os.makedirs(output_dir, exist_ok=True)
        wf = wave.open(os.path.join(output_dir, "record.wav"), "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b"".join(frames))
        wf.close()

        logger.info("End recording to file.")

    def __del__(self):
        super(AutoUnlockAppWAuth, self).__del__()
        logger.info("Stop AutoUnlockAppWAuth.")
