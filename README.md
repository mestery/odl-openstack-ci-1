Overivew
--------
This is a Vagrant box designed to run the same set of tests the OpenDaylight
CI system runs for each commit made to both OpenStack Neutron and OpenDaylight
itself.

How to use this
---------------
Make sure you have Vagrant installed, and clone the repository. Next, go into
the directory and run:

  vagrant up

Wait a bit, and then reload the box:

  vagrant reload

After the box reloads, you can login to the box and execute the CI tests:

  vagrant ssh
  cd /vagrant
  ./odl-devstack-ci.sh

When it's complete, all saved logs will be found here inside the box:

  /home/vagrant/opendaylight-full-logs.tgz
