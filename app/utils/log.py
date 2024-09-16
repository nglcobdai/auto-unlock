import logging
from datetime import datetime
from logging import INFO, FileHandler, Formatter, StreamHandler

import pytz


class CustomLogger(logging.Logger):
    def __init__(self, name):
        """Constructor of CustomLogger

        Args:
            name (str): Name of the logger.
        """
        super().__init__(name)
        self.jst = pytz.timezone("Asia/Tokyo")
        self.string_handler = None

    def _jst_time(self, *args):
        """Get Japan Standard Time

        Returns:
            time.struct_time: JST
        """
        return datetime.now(self.jst).timetuple()

    def set_logger(self, log_level="INFO", log_file=None, is_stream=True):
        """Set logger

        Args:
            log_file (str): File name of the log.
        """
        numeric_level = getattr(logging, log_level, INFO)
        self.setLevel(numeric_level)

        _format = "%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s"
        formatter = Formatter(_format)
        formatter.converter = self._jst_time  # Translate UTC to JST

        # If the console handler has already been added, check and add it
        if not any(isinstance(h, StreamHandler) for h in self.handlers) and is_stream:
            self._set_console_handler(formatter)

        # If the file handler has already been added, check and add it
        if not any(isinstance(h, FileHandler) for h in self.handlers) and log_file:
            self._set_file_handler(formatter, log_file)

        # If the string handler has already been added, check and add it
        if not any(isinstance(h, StringLogHandler) for h in self.handlers):
            self._set_string_handler(formatter)

    def _set_console_handler(self, formatter):
        """Set console handler

        Args:
            formatter (logging.Formatter): Formatter
        """
        console_handler = StreamHandler()
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

    def _set_file_handler(self, formatter, log_file):
        """Set file handler

        Args:
            formatter (logging.Formatter): Formatter
            log_file (str): File name of the log.
        """
        file_handler = FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

    def _set_string_handler(self, formatter):
        """Set string handler

        Args:
            formatter (logging.Formatter): Formatter
        """
        self.string_handler = StringLogHandler()
        self.string_handler.setFormatter(formatter)
        self.addHandler(self.string_handler)

    def get_log_message(self):
        """Get last log message"""
        if not self.string_handler:
            self.warning("String handler is not set.")
            return ""

        return self.string_handler.get_log_message()


class StringLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.message = ""

    def emit(self, record):
        """Emit log

        Args:
            record (logging.LogRecord): Log record
        """
        self.message = self.format(record)

    def get_log_message(self):
        """Get last log message"""
        return self.message


def get_logger(name, log_level="INFO", log_file=None, is_stream=True):
    """Get logger

    Args:
        name (str): Name of the logger.
        log_file (str, optional): File name of the log (None).

    Returns:
        logging.Logger: Logger
    """
    logging.setLoggerClass(CustomLogger)
    logger = logging.getLogger(name)
    logger.set_logger(log_level, log_file, is_stream)
    return logger
