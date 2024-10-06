from app.utils.config import Settings
from app.utils.log import (
    ConsoleHandlerInfo,
    RotatingFileHandlerInfo,
    StringHandlerInfo,
    get_logger,
)
from app.utils.slack import Slack

settings = Settings()
logger = get_logger(
    settings.PROJECT_NAME,
    ch_info=ConsoleHandlerInfo(log_level=settings.LOGGING_LEVEL),
    sh_info=StringHandlerInfo(),
    fh_info=RotatingFileHandlerInfo(
        log_level=settings.LOGGING_LEVEL,
        filename="log/application.log",
        backupCount=settings.LOGGING_BACKUP_COUNT,
        maxGBytes=settings.LOGFILE_SIZE_GB,
    ),
)
slack = Slack(settings.SLACK_API_TOKEN)
