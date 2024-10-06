from app.src import auto_unlock_app
from app.utils import settings, logger


def main():
    logger.info("----------------------------------------")
    auto_unlock_app(settings.IS_AUTHENTICATION)
    logger.info("----------------------------------------")


if __name__ == "__main__":
    main()
