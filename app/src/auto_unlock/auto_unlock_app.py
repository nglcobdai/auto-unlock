#!/usr/bin/env python

import numpy as np
import pyaudio

from app.src.switch_bot.switch_bot import SwitchBot
from app.utils import logger, settings, slack


class AutoUnlockApp:
    def __init__(self):
        try:
            logger.info("Initialize AutoUnlockApp.")
        except Exception as e:
            logger.error(e)
            slack.post_text(
                channel=settings.SLACK_CHANNEL, text=logger.get_log_message()
            )
            raise Exception
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=settings.FORMAT,
            channels=settings.CHANNELS,
            rate=settings.RATE,
            input=True,
            frames_per_buffer=settings.CHUNK,
        )
        self.chunk = settings.CHUNK
        self.threshold = settings.THRESHOLD
        self.consecutive_frames_threshold = settings.CONSECUTIVE_FRAMES_THRESHOLD
        self.interval_frames_threshold = settings.INTERVAL_FRAMES_THRESHOLD
        self.unlock_bot_id = settings.UNLOCK_BOT_ID
        self.consecutive_frames = 0
        self.interval_frames = settings.INTERVAL_FRAMES_THRESHOLD

    def __call__(self):
        logger.info("Start recording...")
        switch_bot = SwitchBot()

        while self.stream.is_active():
            try:
                data = self.stream.read(self.chunk)
                x = np.frombuffer(data, dtype="int16") / 32768.0
                if (
                    (x.max() > self.threshold)
                    and (self.consecutive_frames >= self.consecutive_frames_threshold)
                    and (self.interval_frames >= self.interval_frames_threshold)
                ):
                    logger.info("Unlock event detected.")
                    switch_bot.control_device(self.unlock_bot_id, "turnOn")
                    self.consecutive_frames = 0
                    self.interval_frames = 0
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
            except Exception as e:
                logger.warning(str(e))
                slack.post_text(
                    channel=settings.SLACK_CHANNEL, text=logger.get_log_message()
                )
                logger.info("Stop recording...")
                raise Exception

        logger.info("Stop recording...")

    def _cleanup(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        logger.info("Stop AutoUnlockApp.")
