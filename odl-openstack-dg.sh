#!/bin/bash

# NOTE: This file takes two jobs from the OpenStack infra and
#       puts them here. See here:
#
# https://github.com/openstack-infra/project-config/blob/master/jenkins/jobs/networking-odl.yaml

# Check for Fedora vs. Ubuntu
if [ -f "/etc/debian_version" ]; then
    IS_UBUNTU=1
else
    IS_FEDORA=1
fi

if [ "$IS_FEDORA" == "1" ]; then
    # *SIGH*. This is required to get lsb_release
    sudo yum -y install redhat-lsb-core indent
fi

# Add the Jenkins user
JENKGRP=$(sudo grep jenkins /etc/group)
JENKUSR=$(sudo grep jenkins /etc/passwd)
if [ "$JENKGRP" == "" ]; then
    sudo groupadd jenkins
fi
if [ "$JENKUSR" == "" ]; then
    if [ "$IS_FEDORA" == "1" ]; then
        sudo adduser -g jenkins jenkins
    else
        JGID=$(cat /etc/group|grep jenkins| cut -d ":" -f 3)
        sudo adduser --quiet --gid $JGID jenkins
    fi
fi

# Run the script as the jenkins user
sudo -u jenkins -H sh -c "./odl-openstack-dg-run.sh"
