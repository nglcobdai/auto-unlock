from utils.config import settings
from src.auto_unlock import auto_unlock


def main():
    app = auto_unlock(settings.IS_AUTHENTICATING)
    app()


if __name__ == "__main__":
    main()
