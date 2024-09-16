from app.utils.config import Settings
from app.utils.log import get_logger
from app.utils.slack import Slack

settings = Settings()
logger = get_logger(settings.PROJECT_NAME)
slack = Slack(settings.SLACK_API_TOKEN)
