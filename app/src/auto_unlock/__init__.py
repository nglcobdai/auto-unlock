from auto_unlock_app import AutoUnlockApp
from auto_unlock_app_w_auth import AutoUnlockAppWAuth


def auto_unlock_app(is_authenticating=True):
    if is_authenticating:
        return AutoUnlockAppWAuth()
    else:
        return AutoUnlockApp()
