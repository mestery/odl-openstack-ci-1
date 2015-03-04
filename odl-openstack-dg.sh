#!/bin/bash

# NOTE: This file takes two jobs from the OpenStack infra and
#       puts them here. See here:
#
# https://github.com/openstack-infra/project-config/blob/master/jenkins/jobs/networking-odl.yaml

# *SIGH*. This is required to get lsb_release
sudo yum -y install redhat-lsb-core indent python-virtualenv

# Add the Jenkins user
JENKGRP=$(sudo grep jenkins /etc/group)
JENKUSR=$(sudo grep jenkins /etc/passwd)
if [ "$JENKGRP" == "" ]; then
    sudo groupadd jenkins
fi
if [ "$JENKUSR" == "" ]; then
    sudo adduser -g jenkins jenkins
fi

# Run the script as the jenkins user
sudo -u jenkins -H sh -c "./odl-openstack-dg-run.sh"
