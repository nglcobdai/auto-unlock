from app.src import auto_unlock_app
from app.utils import settings, logger


def main():
    auto_unlock_app(settings.IS_AUTHENTICATION)


if __name__ == "__main__":
    main()
