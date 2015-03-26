Overview
--------
This is a Vagrant box designed to run the same set of tests the OpenDaylight
CI system runs for each commit made to both OpenStack Neutron and OpenDaylight
itself. These run against either CentOS 7, Fedora 20 or Ubuntu 14.04, Vagrantfiles for
each of those operating systems are provided here.

How to use this
---------------
Make sure you have Vagrant installed, and clone the repository. Next, go into
the centos, fedora or ubuntu directory and run:

  vagrant up

Wait a bit, and then reload the box:

  vagrant reload

After the box reloads, you can login to the box and execute the CI tests:

    vagrant ssh
    cd /vagrant/odl-ci
    ./odl-devstack-ci.sh

When it's complete, all saved logs will be found here inside the box:

  /home/vagrant/opendaylight-full-logs.tgz

##### Manual Stack

If you are interested in doing the stacking and possibly running tempest tests
manually, edit odl-devstack-ci.sh and set STACK_AND_TEST to "no" before running
it. That will do all the needed install and config and stop. So you can also
adjust /home/vagrant/devstack/local.conf before calling ./stack.sh

##### Wireshark

If you are interested in capturing packets, use the '-X' param as shown below:

    vagrant ssh -- -X
    sudo wireshark

