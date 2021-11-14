# SET VARIABLES
ISO = "bento/ubuntu-20.04"
NET = "10.0.2."
DOMAIN = ".netology"
HOST_PREFIX = "server"
#INVENTORY_PATH = "../ansible/inventory"
servers = [
{
:hostname => HOST_PREFIX + "4" + DOMAIN,
:ip => NET + "111",
:ssh_host => "20011",
:ssh_vm => "22",
:ram => 1024,
:core => 1
}
]



# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
    config.vm.synced_folder "c:/data", "/vagrant_data"
    config.vbguest.auto_update = false

    servers.each do |machine|
      config.vm.define machine[:hostname] do |node|
        node.vm.box = ISO
        node.vm.hostname = machine[:hostname]
        node.vm.network "private_network", ip: machine[:ip]
        node.vm.network :forwarded_port, guest: machine[:ssh_vm],
        host: machine[:ssh_host]
	node.vm.network "public_network", use_dhcp_assigned_default_route: true
        node.vm.provider "virtualbox" do |vb|
          vb.customize ["modifyvm", :id, "--memory", machine[:ram]]
          vb.customize ["modifyvm", :id, "--cpus", machine[:core]]
          vb.name = machine[:hostname]
        end

	node.vm.provision "shell", inline: <<-SHELL
	  apt install software-properties-common -y
	  add-apt-repository --yes --update ppa:ansible/ansible
	  apt install ansible --yes
	  apt install mc --yes
          locale-gen ru_RU
          locale-gen ru_RU.UTF-8
          update-locale
          ansible-playbook /vagrant_data/ansible/provision.yml
	SHELL

#	node.vm.provision "ansible" do |setup|
#	  setup.inventory_path = INVENTORY_PATH
#	  setup.playbook = "../data/ansible/provision.yml"
#	  setup.become = true
#	  setup.extra_vars = { ansible_user: 'vagrant' }
#	end
      end
    end
end
