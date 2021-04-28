# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # https://docs.vagrantup.com.
  config.vm.box = "ubuntu/focal64"
  config.vm.network "private_network", type: "dhcp"
  config.vm.synced_folder ".", "/vagrant"

  config.vm.provider "virtualbox" do |vb|
    vb.cpus = "2"
    vb.memory = "1024"
  end

  (0..2).each do |n|
    config.vm.define "docker-swarm-#{n}", autostart: false do |conf|
      conf.vm.hostname = "docker-swarm-#{n}"
    end
  end

  (0..2).each do |n|
    config.vm.define "k8s-#{n}", autostart: n==0?true:false do |conf|
      conf.vm.hostname = "k8s-#{n}"
    end
  end

  config.vm.provision "ansible" do |ansible|
    ansible.groups = {
      "kubernetes" => ["k8s-*"],
      "docker_swarm" => ["docker-swarm-*"],
      "docker_swarm_manager" => ["docker-swarm-0"],
      "docker_swarm_worker" => ["docker-swarm-*"]
    }
    ansible.host_vars = {}
    ansible.playbook = "playbook.yml"
  end
end
