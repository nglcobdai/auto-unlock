from app.src.auto_unlock import auto_unlock_app
from app.utils import settings, logger, slack


def main():
    app = auto_unlock_app(settings.IS_AUTHENTICATION)
    try:
        app()
    except Exception as e:
        logger.error(e)
        slack.post_text(channel=settings.SLACK_CHANNEL, text=logger.get_log_message())

        app()


if __name__ == "__main__":
    main()
