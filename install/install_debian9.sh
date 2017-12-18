#/bin/sh
#

apt update

apt install git curl
apt install apache2 libapache2-mpm-itk
apt install php php-curl php-cli

apt install mariadb-server

apt install python3-setuptools python3-lxml
apt install python3-wheel python3-pip --no-install-recommends

python3 -m pip -U discord.py
