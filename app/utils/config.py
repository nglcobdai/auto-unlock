import pyaudio
import os

import dotenv

dotenv.load_dotenv()


class Settings:
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

    SWITCH_BOT_TOKEN = os.getenv("SWITCH_BOT_TOKEN")
    SWITCH_BOT_SECRET = os.getenv("SWITCH_BOT_SECRET")
    UNLOCK_BOT_ID = os.getenv("UNLOCK_BOT_ID")


settings = Settings()
