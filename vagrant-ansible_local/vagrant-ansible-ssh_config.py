#!/usr/bin/env python3
import filecmp
import glob
import os
import re
import shutil

def sync_private_keys(private_keys):
    for private_key_src in private_keys:
        host = private_key_src.split('/')[4]
        private_key = "{}/{}".format(os.path.expanduser("~"), os.path.relpath(private_key_src, "/vagrant"))

        if not os.path.exists(private_key) or not filecmp.cmp(private_key_src, private_key):
            dir = os.path.dirname(private_key)
            if not os.path.exists(dir):
                os.makedirs(dir)
            shutil.copy(private_key_src, private_key)
            os.chmod(private_key, 0o600)

def generate_ssh_config(private_keys):
    HOME = os.path.expanduser("~")
    ssh_config = "{}/{}".format(HOME,'/.ssh/config')

    re_Host = re.compile('^\s*Host\s+(.*)$', re.IGNORECASE)
    re_IdentityFile = re.compile('\s*IdentityFile\s+(.*)$', re.IGNORECASE)

    _ssh_config = {}
    try:
        with open(ssh_config, "r") as f:
            for line in f:
                line = line.strip()
                _Host = re_Host.match(line)
                if _Host:
                    Host = _Host.groups()[0]
                _IdentityFile = re_IdentityFile.match(line)
                if _IdentityFile:
                    _ssh_config[Host] = _IdentityFile.groups()[0]
    except:
        pass

    new_config = {}
    for private_key_src in private_keys:
         _Host = private_key_src.split('/')[4]
         if _Host not in _ssh_config:
             _private_key = "{}/{}".format(HOME, os.path.relpath(private_key_src, "/vagrant"))
             new_config[_Host] = _private_key

    if new_config:
        with open(ssh_config, 'w+') as f:
            content = f.read()
            f.seek(0, 0)
            for _Host in new_config:
                f.write('Host '+ _Host +'\n IdentityFile '+ new_config[_Host] +'\n'+ content)


def main():
    private_keys = list(glob.glob("/vagrant/.vagrant/machines/*/virtualbox/private_key"))

    sync_private_keys(private_keys)
    generate_ssh_config(private_keys)

if __name__ == "__main__":
    main()
