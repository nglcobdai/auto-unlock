from nglcobdai_utils import Settings, Slack, get_logger

settings = Settings()
logger = get_logger(name=settings.PROJECT_NAME)
slack = Slack(token=settings.SLACK_API_TOKEN, channel=settings.SLACK_CHANNEL)
