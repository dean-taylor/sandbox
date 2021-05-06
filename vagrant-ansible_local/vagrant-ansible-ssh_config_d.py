#!/usr/bin/env python3
import glob
import os

host_setting = """ User vagrant
 UserKnownHostsFile /dev/null
 StrictHostKeyChecking no
 PasswordAuthentication no
 LogLevel FATAL"""

machines_path = "/vagrant/.vagrant/machines"

def main():
    machines = list(os.path.relpath(s, machines_path) for s in list(glob.glob("/vagrant/.vagrant/machines/*")))
    print('Host '+ ' '.join(machines) +'\n'+ host_setting)

if __name__ == "__main__":
    main()
