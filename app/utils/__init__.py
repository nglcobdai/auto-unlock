from app.utils.config import Settings
from app.utils.log import Logger
from app.utils.slack import Slack

settings = Settings()
logger = Logger(settings.PROJECT_NAME).logger
slack = Slack(settings.SLACK_API_TOKEN)
