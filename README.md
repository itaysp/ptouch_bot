# P-Touch Telegram bot

I wanted to make my Brother 2430PC accessible to all house users without using a computer.  
I used a Raspberry Pi Zero W with Raspberry Pi OS Lite for this job.  

## Dependencies

Needed packages that were missing from the Pi Zero:

```console
sudo apt-get update
sudo apt-get install libusb-1.0-0-dev libgd-dev git cmake gettext python3 python3-pip
```

## Printing from Linux

We need to build this utility in oder to print from a linux machine

```console
git clone https://git.familie-radermacher.ch/linux/ptouch-print.git/
```

Build and Install

```console
cd ptouch-print
./build.sh
cp build/ptouch-print /usr/bin
```

Finally make the USB bus accessible without using `sudo`

```console
sudo chmod -R 777 /dev/bus/usb
```

## Telegram Bot

I used python-telegram-bot for this job.

```console
pip install -r requirements.txt
```

Add your bot token and allowed user IDs to `print_consts.py`  

## Running the Bot

```console
python3 ptouch_bot.py
```

## Startup Service

Create a service file under `/etc/systemd/system/ptouch_bot.service`:

```console
[Unit]
Description=P-Touch Bot
After=network-online.target
Wants=network-online.target

[Service]
Restart=always
RestartSec=3
ExecStartPre=sudo chmod -R 777 /dev/bus/usb/
ExecStart=python3 /home/pi/ptouch_bot/ptouch_bot.py

[Install]
WantedBy=multi-user.target
```

Enable the service

```console
sudo systemctl enable ptouch_bot.service
```

