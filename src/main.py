#!/usr/bin/env python

import pyaudio
import dotenv
import os
import numpy as np
from datetime import datetime
import requests
import logging
from logging import Formatter, StreamHandler, getLogger, DEBUG
import pytz

dotenv.load_dotenv()

# 環境変数からログレベルを取得
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "DEBUG").upper()
numeric_level = getattr(logging, LOGGING_LEVEL, DEBUG)
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

# PyAudioオブジェクトを初期化
audio = pyaudio.PyAudio()
stream = audio.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)

logger.info("Start recording...")

consecutive_frames = 0
interval_frames = INTERVAL_FRAMES_THRESHOLD

while stream.is_active():
    try:
        data = stream.read(CHUNK)
        x = np.frombuffer(data, dtype="int16") / 32768.0
        # print(x.max())
        if (
            (x.max() > THRESHOLD)
            and (consecutive_frames >= CONSECUTIVE_FRAMES_THRESHOLD)
            and (interval_frames >= INTERVAL_FRAMES_THRESHOLD)
        ):
            res = requests.post(AUTO_UNLOCK_API_URL)
            logger.info(res.text)
            consecutive_frames = 0
            interval_frames = 0
        elif x.max() > THRESHOLD:
            consecutive_frames += 1
        else:
            consecutive_frames = 0
        interval_frames += 1
    except KeyboardInterrupt:
        break

logger.info("Stop recording...")

# ストリームを停止して閉じる
stream.stop_stream()
stream.close()
audio.terminate()
