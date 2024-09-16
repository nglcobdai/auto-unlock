# auto-unlock-app

This is a script for unlocking the auto-lock of an apartment using [Switch Bot's Bot](https://www.switchbot.jp/products/switchbot-bot). \
It triggers when the room's intercom sounds, performs pass-phrase authentication, and presses the unlock button. \
It is intended to be used in combination with [Auto Unlock Server](https://github.com/nglcobdai/auto-unlock-server).

|                 |                                                                                                                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **License**     | ![LICENSE](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)                                                                                                                          |
| **Environment** | ![Raspberry Pi](https://img.shields.io/badge/-Raspberry_Pi_Zero_W-C51A4A.svg?logo=Raspberry-Pi&style=flat) ![Python](https://img.shields.io/badge/-Python_3.10-F9DC3E.svg?logo=python&style=flat) |
| **Technology**  | ![SwitchBot API](https://img.shields.io/badge/-SwitchBot_API_v1.1-fc6203.svg?logo=SwitchBot&style=flat) ![Slack SDK](https://img.shields.io/badge/-Slack_SDK-4A154B.svg?logo=slack&style=flat)    |
|                 |                                                                                                                                                                                                   |

## Devices

This repository can be run on the following environment:

- `Raspberry Pi Zero W`
- OS: `Raspbian GNU/Linux 12 (bookworm)`
- Kernel: `Linux 6.6.28+rpt-rpi-v6`
- Architecture: `armv6l`

## Getting Started

### 1. Clone & Set PYTHONPATH

```sh
$ git clone -b v0.2.0 https://github.com/nglcobdai/auto-unlock-app.git
$ cd auto-unlock-app
$ export PYTHONPATH=$PWD
```

### 2. Create .env

Copy .env.example to .env

```sh
$ cp .env{.example,}
```

You need to edit the following items

| Key                   | Description              | Reference                                                                                                                                           |
| --------------------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AUTO_UNLOCK_API_URL` | Auto Unlock API URL      | API endpoint by [Auto Unlock Server](https://github.com/nglcobdai/auto-unlock-server)                                                               |
| `SWITCH_BOT_TOKEN`    | Switch Bot Token         | [Switch Bot](https://support.switch-bot.com/hc/ja/articles/12822710195351-トークンの取得方法)                                                       |
| `SWITCH_BOT_SECRET`   | Switch Bot Secret        | [Switch Bot](https://support.switch-bot.com/hc/ja/articles/12822710195351-トークンの取得方法)                                                       |
| `UNLOCK_BOT_ID`       | Bot ID for Unlock button | Refer to the output of `python app/src/switch_bot.py`                                                                                               |
| `SLACK_API_TOKEN`     | Slack API Token          | Refer to the [How to setup Slack APP](https://github.com/nglcobdai/nglcobdai-utils/blob/dev/doc/how_to_setup_slack_app.md#how-to-setup-a-slack-app) |
| `SLACK_CHANNEL`       | Slack Channel            | Slack channel name                                                                                                                                  |

### 3. Install Required Libraries

```sh
$ sudo apt-get install jackd2
$ sudo apt-get install libopenjp2-7
$ sudo apt-get install libtiff5
$ sudo apt-get install libatlas-base-dev
$ sudo apt-get install libjasper-dev
$ sudo apt-get install libqtgui4
$ sudo apt-get install libqt4-test
```

### 4. Install Dependencies

```sh
$ pip install -r requirements.txt
```

### 6. Run

```sh
$ python app/main.py
```
