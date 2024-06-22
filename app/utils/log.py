import logging
from logging import Formatter, StreamHandler, getLogger, DEBUG
import pytz
import os
from datetime import datetime


class Logger:
    def __init__(self, name):
        self.logger = getLogger(name)

        log_level = os.getenv("LOGGING_LEVEL", "DEBUG").upper()
        numeric_level = getattr(logging, log_level, DEBUG)

        self.jst = pytz.timezone("Asia/Tokyo")
        self.set_logger(numeric_level)

    # タイムゾーンを日本時間に設定するためのカスタム関数
    def jst_time(self):
        return datetime.now(self.jst).timetuple()

    def set_logger(self, numeric_level):
        self.logger.setLevel(numeric_level)

        # コンソール出力のためのハンドラを設定
        console_handler = StreamHandler()
        formatter = Formatter(
            "%(asctime)s : %(levelname)s : %(filename)s - %(message)s"
        )
        formatter.converter = self.jst_time  # 日本時間を使用するように設定
        console_handler.setFormatter(formatter)

        # ロガーにコンソールハンドラを追加
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)
