#!/bin/bash

cd "$(dirname "$0")"

export PATH=$PATH:/bin:/sbin:/usr/sbin
export IFACE_NAME='enp0s8'

# If we are running in vagrant, inject some helpful env vars
if [ "$USER" == "vagrant" ]; then
    source vagrantopts
fi

export WORKSPACE=/home/vagrant/devstack
export BUILD_TAG=
export DEVSTACKDIR=$WORKSPACE/$BUILD_TAG
export TEMPEST_RUN_LOG=/tmp/odl_tempest_test_list.txt

source functions

# Archive logs on exit
trap archive-logs EXIT

check-env
prepare-environment
configure-firewall
install-packages
install-pip
install-tempest
install-devstack
# Workaround for bug:
# https://bugs.launchpad.net/devstack/+bug/1276297
sudo rm -rf /usr/lib/python2.7/site-packages/oslo*
stack
run-tempest
