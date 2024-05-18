# auto-unlock-app

## Devices

This repository can be run on the following environment:

- Raspberry Pi Zero W
- OS: Raspbian GNU/Linux 12 (bookworm)
- Kernel: Linux 6.6.28+rpt-rpi-v6
- Architecture: armv6l

## Getting Started

### 1. Clone & Prepare .env

```sh
$ git clone git@github.com:nglcobdai/auto-unlock-app.git
$ cd auto-unlock-app
```

### 2. Create .env

- Copy .env.example to .env

```sh
$ cp .env{.example,}
```

### 3. Install Dependencies

```sh
$ pip install -r requirements.txt
```

### 4. Install Required Libraries

```sh
$ sudo apt-get install libopenjp2-7
$ sudo apt-get install libtiff5
$ sudo apt-get install libatlas-base-dev
$ sudo apt-get install libjasper-dev
$ sudo apt-get install libqtgui4
$ sudo apt-get install libqt4-test
```

