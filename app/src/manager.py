from app.src.auto_unlock import AutoUnlockApp, AutoUnlockAppWAuth
from app.utils import logger, settings, slack


class AutoUnlockAppManager:
    def __init__(self, is_authenticating=True):
        logger.info("Start AutoUnlockApp.")
        slack.post_text(channel=settings.SLACK_CHANNEL, text=logger.get_log_message())
        if is_authenticating:
            self.app = AutoUnlockAppWAuth()
        else:
            self.app = AutoUnlockApp()

    def __call__(self):
        try:
            self.app()
        except Exception:
            logger.warning("Restart AutoUnlockApp.")
            slack.post_text(
                channel=settings.SLACK_CHANNEL, text=logger.get_log_message()
            )
            self.__call__()
        finally:
            self.__del__()

    def __del__(self):
        self.app.__del__()

        logger.warning("End AutoUnlockApp.")
        slack.post_text(channel=settings.SLACK_CHANNEL, text=logger.get_log_message())
