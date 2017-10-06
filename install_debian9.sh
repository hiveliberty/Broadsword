#/bin/sh
#

apt update
apt install python3 python3-setuptools python3-lxml
apt install python3-wheel python3-pip --no-install-recommends

python3 -m pip -U discord.py
