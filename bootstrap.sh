#!/bin/bash

yum install -q -y deltarpm git python python-crypto python-devel python-lxml python-setuptools @development-tools libxml2-devel libxslt-devel libffi-devel

if [ ! -f /etc/udev/rules.d/80-net-setup-link.rules ]; then
    ln -s /dev/null /etc/udev/rules.d/80-net-setup-link.rules
fi

echo "***************************************************"
echo "*   PLEASE RELOAD THIS VAGRANT BOX BEFORE USE     *"
echo "***************************************************"
