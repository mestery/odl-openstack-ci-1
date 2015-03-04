# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Uncomment the below two lines to use Fedora 20 instead of CentOS 7
  #config.vm.box = "fedora20x64"
  #config.vm.box_url = "http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_fedora-20_chef-provisionerless.box"
  config.vm.box = "chef/centos-7.0"

  config.vm.network "private_network", ip: "192.168.56.80"

  config.vm.provider "virtualbox" do |vb|
      vb.cpus = 4
      vb.memory = 6144
  end

  config.vm.provision "shell", path: "bootstrap.sh"

end
