import base64
import hashlib
import hmac
import json
import time

import requests
from requests.exceptions import RequestException

from app.utils import logger, settings


class SwitchBot:
    SWITCH_BOT_API_URL = "https://api.switch-bot.com"
    VERSION = "v1.1"

    def __init__(self):
        self.switch_bot_token = settings.SWITCH_BOT_TOKEN
        self.switch_bot_secret = settings.SWITCH_BOT_SECRET

    def __init_headers(self):
        nonce = ""
        t = int(round(time.time() * 1000))
        string_to_sign = "{}{}{}".format(self.switch_bot_token, t, nonce)

        string_to_sign = bytes(string_to_sign, "utf-8")
        secret = bytes(self.switch_bot_secret, "utf-8")

        sign = base64.b64encode(
            hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest(),
        )

        return {
            "Authorization": self.switch_bot_token,
            "sign": sign,
            "t": str(t),
            "nonce": nonce,
            "Content-Type": "application/json; charset=utf8",
        }

    def _get_request(self, url, headers):
        try:
            res = requests.get(url, headers=headers)
            data = res.json()
            logger.info(f"Response: {data}")
            if data["message"] == "success":
                return data
            else:
                return {}
        except RequestException as e:
            logger.warning(str(e))
            raise e

    def _post_request(self, url, params, headers):
        logger.debug(f"POST request to {url}, params: {params}")

        try:
            res = requests.post(url, data=json.dumps(params), headers=headers)
            data = res.json()
            logger.info(f"Response: {data}")
            return data
        except RequestException as e:
            logger.warning(str(e))
            raise e

    def get_device_list(self):
        headers = self.__init_headers()
        url = f"{self.SWITCH_BOT_API_URL}/{self.VERSION}/devices"

        res = self._get_request(url, headers)["body"]
        return res

    def control_device(self, deviceId, command):
        headers = self.__init_headers()
        url = f"{self.SWITCH_BOT_API_URL}/{self.VERSION}/devices/{deviceId}/commands"
        params = {
            "command": command,
            "parameter": "",
            "commandType": "command",
        }
        return self._post_request(url, params, headers)


def main():
    switch_bot = SwitchBot()
    print(switch_bot.get_device_list())


if __name__ == "__main__":
    main()
