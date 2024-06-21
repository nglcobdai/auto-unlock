#!/usr/bin/env python

import pyaudio
import numpy as np

# import requests
from utils.log import logger

from utils.config import settings
from src.switch_bot import SwitchBot

# PyAudioオブジェクトを初期化
audio = pyaudio.PyAudio()
stream = audio.open(
    format=settings.FORMAT,
    channels=settings.CHANNELS,
    rate=settings.RATE,
    input=True,
    frames_per_buffer=settings.CHUNK,
)

logger.info("Start recording...")

consecutive_frames = 0
interval_frames = settings.INTERVAL_FRAMES_THRESHOLD

switch_bot = SwitchBot()

while stream.is_active():
    try:
        data = stream.read(settings.CHUNK)
        x = np.frombuffer(data, dtype="int16") / 32768.0
        # print(x.max())
        if (
            (x.max() > settings.THRESHOLD)
            and (consecutive_frames >= settings.CONSECUTIVE_FRAMES_THRESHOLD)
            and (interval_frames >= settings.INTERVAL_FRAMES_THRESHOLD)
        ):
            # res = requests.post(settings.AUTO_UNLOCK_API_URL)
            res = switch_bot.control_device(settings.UNLOCK_BOT_ID, "turnOn")
            logger.info(res.text)
            consecutive_frames = 0
            interval_frames = 0
        elif x.max() > settings.THRESHOLD:
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
