from app.utils import settings
from app.src.auto_unlock import auto_unlock_app


def main():
    app = auto_unlock_app(settings.IS_AUTHENTICATION)
    app()


if __name__ == "__main__":
    main()
