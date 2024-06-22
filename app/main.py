from app.utils import settings
from app.src import auto_unlock


def main():
    app = auto_unlock(settings.IS_AUTHENTICATING)
    app()


if __name__ == "__main__":
    main()
