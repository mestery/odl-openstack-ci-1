#!/bin/bash

cd "$(dirname "$0")"

STACK_AND_TEST="yes"

# Check for Fedora vs. Ubuntu
if [ -f "/etc/debian_version" ]; then
    export IS_UBUNTU=1
else
    export IS_FEDORA=1
    if grep -qi centos /etc/redhat-release; then
	export IS_CENTOS=1
    fi
fi

export PATH=$PATH:/bin:/sbin:/usr/sbin

# If we are running in vagrant, inject some helpful env vars
if [ "$USER" == "vagrant" ]; then
    source vagrantopts
fi

export DEVSTACKDIR=$WORKSPACE/$BUILD_TAG
export TEMPEST_RUN_LOG=/tmp/odl_tempest_test_list.txt

source functions

if [ "$STACK_AND_TEST" == "yes" ]; then
    # Archive logs on exit
    trap archive-logs EXIT
fi

test-branch
check-env
prepare-environment
configure-firewall
install-packages
install-pip
#install-tempest
install-devstack
install-workarounds
if [ "$STACK_AND_TEST" == "yes" ]; then
    stack
    run-tempest
fi

