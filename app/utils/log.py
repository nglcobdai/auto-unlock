import logging
from datetime import datetime
from logging import DEBUG, INFO, FileHandler, Formatter, StreamHandler
from logging.handlers import RotatingFileHandler
from pathlib import Path
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
        self.setLevel(DEBUG)

    def _jst_time(self, *args):
        """Get Japan Standard Time

        Returns:
            time.struct_time: JST
        """
        return datetime.now(self.jst).timetuple()

    def settting_logger(self, ch_info, fh_info, sh_info):
        """Set logger

        Args:
            ch_info (ConsoleHandlerInfo): Console handler information.
            fh_info (FileHandlerInfo | RotatingFileHandlerInfo | TimedRotatingFileHandlerInfo): \
                File handler information.
            sh_info (StringHandlerInfo): String handler information.
        """
        if ch_info.is_use:
            self._set_console_handler(ch_info)

        if fh_info.is_use:
            self._set_file_handler(fh_info)

        if sh_info.is_use:
            self._set_string_handler(sh_info)

    def _decode_handler_info(self, handler_info):
        """Decode handler information

        Args:
            handler_info (HandlerInfo): Handler information.

        Returns:
            numeric_level (int): Numeric level
            formatter (logging.Formatter): Formatter
        """
        numeric_level = getattr(logging, handler_info.log_level, INFO)

        formatter = Formatter(handler_info.format)
        formatter.converter = self._jst_time

        return numeric_level, formatter

    def _set_console_handler(self, handler_info):
        """Set console handler

        Args:
            handler_info (ConsoleHandlerInfo): Console handler information.
        """
        numeric_level, formatter = self._decode_handler_info(handler_info)

        console_handler = StreamHandler()
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

    def _set_file_handler(self, handler_info):
        """Set console handler

        Args:
            handler_info (FileHandlerInfo | RotatingFileHandlerInfo | TimedRotatingFileHandlerInfo): \
                File handler information.
        """
        numeric_level, formatter = self._decode_handler_info(handler_info)
        handler_info.filename.parent.mkdir(parents=True, exist_ok=True)

        if type(handler_info) is FileHandlerInfo:
            file_handler = FileHandler(**handler_info.get_param())
        elif type(handler_info) is RotatingFileHandlerInfo:
            file_handler = RotatingFileHandler(**handler_info.get_param())

        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

    def _set_string_handler(self, handler_info):
        """Set console handler

        Args:
            handler_info (StringHandlerInfo): String handler information.
        """
        numeric_level, formatter = self._decode_handler_info(handler_info)

        self.string_handler = StringLogHandler()
        self.string_handler.setLevel(numeric_level)
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


class HandlerInfo:
    def __init__(self, **data):
        """Handler information

        Args:
            is_use (bool): Whether to use the handler.
            log_level (str): Log level.
            format (str): Log format.
                (default: `"%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s"`)
        """
        self.is_use = data.get("is_use", True)
        self.log_level = data.get(
            "log_level", "INFO"
        )  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        self.format: str = data.get(
            "format",
            "%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s",
        )

    def get_param(self):
        """Get handler parameters

        Returns:
            Dict: Handler parameters
        """
        return (
            self._model_dump(exclude={"is_use", "log_level", "format"})
            if self.is_use
            else {}
        )

    def _model_dump(self, exclude):
        return {
            key: value for key, value in self.__dict__.items() if key not in exclude
        }


class ConsoleHandlerInfo(HandlerInfo):
    def __init__(self, **data):
        """Console handler information

        Args:
            format (str, optional): Log format. (default: `"%(asctime)s : %(levelname)s : %(filename)s - %(message)s"`)
        """
        super().__init__(**data)
        self.format = data.get(
            "format", "%(asctime)s : %(levelname)s : %(filename)s - %(message)s"
        )


class FileHandlerInfo(HandlerInfo):
    def __init__(self, **data):
        """File handler information

        Args:
            filename (str | pathlib.Path, optional): Path of the log file. (default: `"~/logs/test.log"`)
            encoding (str, optional): Encoding of the log file. (default: `"utf-8"`)
        """
        super().__init__(**data)
        self.filename = Path(data.get("filename", "~/logs/test.log")).expanduser()
        self.encoding = data.get("encoding", "utf-8")


class RotatingFileHandlerInfo(FileHandlerInfo):

    def __init__(self, **data):
        """Rotating file handler information

        Args:
            backupCount (int): Number of backup files. (default: `5`)
            maxGBytes (int): Maximum size of the log file. (default: `1`)
        """
        super().__init__(**data)
        self.backupCount = data.get("backupCount", 5)
        self.maxBytes = data.get("maxGBytes", 1) * 1024 * 1024 * 1024


class StringHandlerInfo(HandlerInfo):

    def __init__(self, **data):
        """String handler information"""
        super().__init__(**data)


def get_logger(
    name,
    ch_info=ConsoleHandlerInfo(is_use=False),
    fh_info=FileHandlerInfo(is_use=False),
    sh_info=StringHandlerInfo(is_use=False),
):
    """Retrieve a configured logger.

    Args:
        name (str): The name of the logger.
        ch_info (ConsoleHandlerInfo, optional): Console handler information (default: ConsoleHandlerInfo(is_use=False)).
        fh_info (RotatingFileHandlerInfo, optional): File handler information (default: FileHandlerInfo(is_use=False)).
        sh_info (StringHandlerInfo, optional): String handler information (default: StringHandlerInfo(is_use=False)).

    Example:
        >>> console_handler_info = ConsoleHandlerInfo(log_level="INFO")
        >>> file_handler_info = RotatingFileHandlerInfo(
        ...     filename="~/logs/test.log",
        ...     log_level="DEBUG",
        ...     backupCount=5,
        ...     maxGBytes=1,
        ...)
        >>> string_handler_info = StringHandlerInfo(log_level="DEBUG")
        >>> logger = get_logger(
        ...     name="test_logger",
        ...     ch_info=console_handler_info,
        ...     fh_info=file_handler_info,
        ...     sh_info=string_handler_info,
        ... )

    Returns:
        logging.Logger: The configured logger instance.
    """
    logging.setLoggerClass(CustomLogger)
    logger = logging.getLogger(name)
    logger.settting_logger(ch_info, fh_info, sh_info)
    return logger
