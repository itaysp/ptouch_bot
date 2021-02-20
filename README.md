# P-Touch Telegram bot

I wanted to make my Brother 2430PC accessible to all house users without using a computer.  
I used a Raspberry Pi Zero W with Raspberry Pi OS Lite for this job.  

## Dependencies

Needed packages that were missing from the Pi Zero:

```console
libusb-1.0-0-dev libgd-dev autopoint autoconf git gawk
```

## Get a utility to print from a linux machine

```console
cd ~
git clone https://mockmoon-cybernetics.ch/cgi/cgit/linux/ptouch-print.git/
cd ptouch-print
```

We need to fix some error in the source files

```
src/libptouch.c line 180: change from %ld to %u
```

build and install

```console
./autogen.sh
./configure --prefix=/usr
make
sudo make install
```

finally make the usb bus accessible without using `sudo`

```console
sudo chmod -R 777 /dev/bus/usb
```

##Telegram Bot for Python

Install `python-telegram-bot`

```console
cd ~
sudo apt-get install python3-pip
git clone https://github.com/python-telegram-bot/python-telegram-bot.git
cd python-telegram-bot
git submodule update --init --recursive
python3 setup.py install
```

Add your bot token and allowed user IDs to `print_consts.py`  

## Run the Bot

run the bot:

```console
python3 ptouch_bot.py
```

## Install systemd startup script

Create this script file under `/etc/systemd/system/ptouch_bot.service`

```console
[Unit]
Description=P-Touch Bot

[Service]
ExecStartPre=sudo chmod -R 777 /dev/bus/usb/
ExecStart=python3 /home/pi/ptouch_bot/ptouch_bot.py

[Install]
WantedBy=multi-user.target
```

Enable the service 

```console
sudo systemctl enable ptouch_bot.service
```

