import time

from app.src.auto_unlock import AutoUnlockApp, AutoUnlockAppWAuth
from app.utils import logger, settings, slack


class AutoUnlockAppManager:
    def __init__(self, is_authenticating=True):
        try:
            logger.info("Start AutoUnlockApp.")
            slack.post_text(
                channel=settings.SLACK_CHANNEL, text=logger.get_log_message()
            )
        except Exception as e:
            logger.error(str(e))
            slack.post_text(
                channel=settings.SLACK_CHANNEL, text=logger.get_log_message()
            )
        if is_authenticating:
            self.app = AutoUnlockAppWAuth()
        else:
            self.app = AutoUnlockApp()

    def __call__(self):
        self._auto_unlock()
        self._cleanup()

    def _auto_unlock(self):
        try:
            self.app()
        except Exception:
            time.sleep(10)
            logger.warning("Restart AutoUnlockApp.")
            slack.post_text(
                channel=settings.SLACK_CHANNEL,
                text=logger.get_log_message(),
            )
            self._auto_unlock()

    def _cleanup(self):
        self.app._cleanup()

        logger.warning("End AutoUnlockApp.")
        slack.post_text(channel=settings.SLACK_CHANNEL, text=logger.get_log_message())
