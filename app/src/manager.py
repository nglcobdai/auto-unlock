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
        while True:
            try:
                self.app()
                break  # 正常終了したらループを抜ける
            except Exception:
                logger.warning("Restart AutoUnlockApp.")
                slack.post_text(
                    channel=settings.SLACK_CHANNEL, text=logger.get_log_message()
                )
            finally:
                self.cleanup()

    def cleanup(self):
        if hasattr(self, "app"):
            self.app.__del__()
        logger.warning("End AutoUnlockApp.")
        slack.post_text(channel=settings.SLACK_CHANNEL, text=logger.get_log_message())

    def __del__(self):
        self.cleanup()
