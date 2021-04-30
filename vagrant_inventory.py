#!/usr/bin/env python3
import configparser
import json
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

    for group in config.sections():
        if group != "all":
            inventory[group] = { "hosts": [] }
            inventory["all"]["children"].append(group)

        for (host,vars) in config.items(group):
            inventory[group]["hosts"].append(host)
            if host not in inventory["_meta"]["hostvars"]:
                inventory["_meta"]["hostvars"][host] = {}
            inventory["_meta"]["hostvars"][host]["ansible_user"] = "vagrant"
            if vars:
                inventory["_meta"]["hostvars"][host]["ansible_connection"] = "local"

    if _host:
        try:
            print(json.dumps(inventory["_meta"]["hostvars"][_host]))
        except:
            print('{}')
    else:
        print(json.dumps(inventory))

if __name__ == "__main__":
    main(sys.argv[1:])
