#!/bin/bash

# Check for Fedora vs. Ubuntu
if [ -f "/etc/debian_version" ]; then
    IS_UBUNTU=1
else
    IS_FEDORA=1
fi

# Add the jenkins user, and setup passwordless sudo
groupadd jenkins
adduser -g jenkins jenkins
echo "jenkins ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

if [ "$IS_FEDORA" == "1" ]; then
    yum install -q -y deltarpm
    yum install -q -y gcc git python python-crypto python-devel \
                      python-lxml python-setuptools yum-utils \
                      libxml2-devel libxslt-devel libffi-devel
    yum group install -q -y "Development Tools"
    if [ ! -f /etc/udev/rules.d/80-net-setup-link.rules ]; then
        ln -s /dev/null /etc/udev/rules.d/80-net-setup-link.rules
    fi
else
    apt-get update -y
    apt-get install -y git python python-setuptools libxslt1-dev \
                       libxml2-dev libffi-dev python-lxml python-crypto \
                       python-dev git
fi

echo "***************************************************"
echo "*   PLEASE RELOAD THIS VAGRANT BOX BEFORE USE     *"
echo "***************************************************"
