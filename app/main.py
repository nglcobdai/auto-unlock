from app.src.auto_unlock import auto_unlock_app
from app.utils import settings


def main():
    app = auto_unlock_app(settings.IS_AUTHENTICATION)
    app()


if __name__ == "__main__":
    main()
