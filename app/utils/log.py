import logging
from logging import Formatter, StreamHandler, getLogger, DEBUG
import pytz
import os
from datetime import datetime

# 環境変数からログレベルを取得
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "DEBUG").upper()
numeric_level = getattr(logging, LOGGING_LEVEL, DEBUG)
logger = getLogger(__name__)

JST = pytz.timezone("Asia/Tokyo")


# タイムゾーンを日本時間に設定するためのカスタム関数
def jst_time():
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
