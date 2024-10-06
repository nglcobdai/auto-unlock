from app.src.manager import AutoUnlockAppManager


def auto_unlock_app(is_authenticating=True):
    manager = AutoUnlockAppManager(is_authenticating)
    manager()
