# -*- mode: ruby -*-
# vi: set ft=ruby :

IS_WINDOWS = /mingw32/ =~ RUBY_PLATFORM

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

  if IS_WINDOWS
    config.vm.provision "shell", inline: <<-SHELL
      #!/usr/bin/env bash
      REQUIREMENTS_YML='/vagrant/requirements.yml'
      apt-get update
      apt-get -y install \
        python3 \
        python3-pip
      python3 -m pip install ansible
      if [ -f $REQUIREMENTS_YML ]; then
        su - vagrant -c "ansible-galaxy collection install -r $REQUIREMENTS_YML"
        su - vagrant -c "ansible-galaxy role install -r $REQUIREMENTS_YML"
      fi
    SHELL
  end
  config.vm.provision (IS_WINDOWS)?"ansible_local":"ansible" do |ansible|
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
