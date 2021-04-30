# -*- mode: ruby -*-
# vi: set ft=ruby :

ANSIBLE_GROUPS = {
  "kubernetes"   => ["k8s-0","k8s-1","k8s-2"],
  "microk8s"     => ["k8s-0","k8s-1","k8s-2"],
  "docker_swarm" => ["docker-swarm-0","docker-swarm-1","docker-swarm-2"],
  "docker_swarm_manager" => ["docker-swarm-0"],
  "docker_swarm_worker"  => ["docker-swarm-1","docker-swarm-2"]
}
ANSIBLE_HOST_VARS = {}

IS_WINDOWS = /mingw32/ =~ RUBY_PLATFORM

Vagrant.configure("2") do |config|
  # https://docs.vagrantup.com.
  config.vm.box = "ubuntu/focal64"
  config.vm.network "private_network", type: "dhcp"
  config.vm.synced_folder ".", "/vagrant"

  config.vm.provider "virtualbox" do |vb|
    vb.cpus = "2"
    vb.memory = "2048"
  end

  (0..2).each do |n|
    config.vm.define "docker-swarm-#{n}", autostart: false do |conf|
      conf.vm.hostname = "docker-swarm-#{n}"
    end
  end

  (0..2).each do |n|
    config.vm.define "k8s-#{n}", autostart: n==0?true:false, primary: n==0?true:false do |conf|
      conf.vm.hostname = "k8s-#{n}"
      if IS_WINDOWS && n==0
        conf.vm.provision "file", source: "files/ssh_config", destination: "/home/vagrant/.ssh/config"
        conf.vm.provision "file", source: "files/bash_aliases", destination: "/home/vagrant/.bash_aliases"
        conf.vm.provision "shell", inline: <<-SHELL
          #!/usr/bin/env bash
          set -x
          REQUIREMENTS_YML='/vagrant/requirements.yml'
          apt-get update
          apt-get -y install python3 python3-pip
          python3 -m pip install ansible
          if [ -f $REQUIREMENTS_YML ]; then
            su - vagrant -c "ansible-galaxy collection install -r $REQUIREMENTS_YML"
            su - vagrant -c "ansible-galaxy role install -r $REQUIREMENTS_YML"
          fi
        SHELL

        conf.vm.provision "ansible_local" do |ansible|
          ansible.groups = ANSIBLE_GROUPS
          ansible.host_vars = ANSIBLE_HOST_VARS
          ansible.playbook = "playbook-controller.yml"
          ansible.provisioning_path = "/vagrant"
          ansible.tmp_path = "/tmp/vagrant-ansible"

          ansible.install = false
          ansible.install_mode = "pip"
          ansible.pip_install_cmd = "sudo apt-get -y install python3 python3-pip && sudo ln -frs /usr/bin/pip3 /usr/bin/pip"
          ansible.version = "latest"
        end
      end
    end
  end

  config.vm.provision "shell", inline: <<-SHELL
    #!/usr/bin/env bash
    set -x
    # Enable mDNS on the private_network
    if ! [ -f /etc/systemd/resolved.conf.d/mDNS.conf ]; then
      [ -d /etc/systemd/resolved.conf.d ] || mkdir -p /etc/systemd/resolved.conf.d
      cat <<'EOT' >/etc/systemd/resolved.conf.d/mDNS.conf
[Resolve]
MulticastDNS=true
EOT
      systemctl restart systemd-resolved.service
    fi
    if ! [ -f /etc/systemd/network/10-netplan-enp0s8.network.d/mDNS.conf ]; then
      [ -d /etc/systemd/network/10-netplan-enp0s8.network.d ] || mkdir -p /etc/systemd/network/10-netplan-enp0s8.network.d
      cat <<'EOT' >/etc/systemd/network/10-netplan-enp0s8.network.d/mDNS.conf
[Network]
MulticastDNS=true
EOT
      systemctl restart systemd-networkd.service
    fi
    # Add local to Domain search path
    if ! [ -f /etc/netplan/55-vagrant-SHELL.yaml ]; then
      cat <<'EOT' >/etc/netplan/55-vagrant-SHELL.yaml
---
network:
  ethernets:
    enp0s8:
      nameservers:
        search: ["local"]
  version: 2
EOT
      netplan apply && sleep 5
    fi
  SHELL

  if not IS_WINDOWS
    config.vm.provision "ansible" do |ansible|
      ansible.groups = ANSIBLE_GROUPS
      ansible.host_vars = ANSIBLE_HOST_VARS
      ansible.playbook = "playbook.yml"
    end
  end
end
