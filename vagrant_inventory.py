#!/usr/bin/env python3
import configparser
import filecmp
import glob
import json
import os
import shutil
import sys, getopt

def main(argv):
    try:
        opts,args = getopt.getopt(argv, None, ["list","host="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        #print("whatever.py [--list|--host=HOSTNAME]")
        sys.exit(2)

    _list = None
    _host = None
    for o,a in opts:
        if o in ("-h","--help"):
            usage()
            sys.exit()
        elif o == "--host":
            _host = a

    config = configparser.ConfigParser(allow_no_value=True,delimiters=(' '))
    with open("/tmp/vagrant-ansible/inventory/vagrant_ansible_local_inventory") as stream:
        config.read_string("[all]\n" + stream.read())

    inventory = {
        "_meta": {
            "hostvars": {},
        },
        "all": {"hosts": [], "children": ["ungrouped"]},
        "ungrouped": {"children": []},
    }

    private_keys = list(glob.glob("/vagrant/.vagrant/machines/*/virtualbox/private_key"))

    for group in config.sections():
        if group != "all":
            inventory[group] = { "hosts": [] }
            inventory["all"]["children"].append(group)

        for (host,vars) in config.items(group):
            inventory[group]["hosts"].append(host)
            if host not in inventory["_meta"]["hostvars"]:
                inventory["_meta"]["hostvars"][host] = {}
                private_key_src = "/vagrant/.vagrant/machines/{}/virtualbox/private_key".format(host)
                if private_key_src in private_keys:
                    private_key = "{}/{}".format(os.path.expanduser("~"), os.path.relpath(private_key_src, "/vagrant"))
                    if not os.path.exists(private_key) or not filecmp.cmp(private_key_src, private_key):
                        dir = os.path.dirname(private_key)
                        if not os.path.exists(dir):
                            os.makedirs(dir)
                        shutil.copy(private_key_src, private_key)
                        os.chmod(private_key, 0o600)
                    inventory["_meta"]["hostvars"][host]["ansible_ssh_private_key_file"] = private_key
            inventory["_meta"]["hostvars"][host]["ansible_user"] = "vagrant"
            if vars:
                for var in vars.split(" "):
                    k,v = var.split("=")
                    inventory["_meta"]["hostvars"][host][k] = v

    if _host:
        try:
            print(json.dumps(inventory["_meta"]["hostvars"][_host]))
        except:
            print('{}')
    else:
        print(json.dumps(inventory))

if __name__ == "__main__":
    main(sys.argv[1:])
