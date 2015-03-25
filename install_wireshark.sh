#!/bin/bash

# Should have super powers...
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Check for Fedora vs. Ubuntu
if [ -f "/etc/debian_version" ]; then
    IS_UBUNTU=1
else
    IS_FEDORA=1
fi


if [ "$IS_FEDORA" == "1" ]; then
    PKGS='wireshark xorg-x11-xauth xorg-x11-fonts-* xorg-x11-utils wireshark-gnome'
    yum install -q -y $PKGS
    # Link root’s .XAutority to vagrant's
    ln -sf /home/vagrant/.Xauthority /root/
else
    apt-get install -y wireshark
fi

