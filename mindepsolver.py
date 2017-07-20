#!/usr/bin/env python

import argparse
import subprocess
from collections import defaultdict

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('depfile')
    return parser.parse_args()

args = get_args()

install_dict = defaultdict(str)

orig_deps = subprocess.check_output(['dep_parser.py', args.depfile, 'yum'])

for dep in orig_deps.strip().split():
    o_val = install_dict[dep.rsplit('-',1)[0]]
    install_dict[dep.rsplit('-',1)[0]] = max(o_val, 0 if len(dep.rsplit('-',1)) < 2 else dep.rsplit('-',1)[1])

for rpm in orig_deps.strip().split():
    ds = subprocess.check_output(["repoquery", "--requires", rpm, "--enablerepo=eds-rawhide", '--qf=%{vendor}:%{name} %{version}'])
    for l in ds.split('\n'):
        l = [x.strip() for x in l.split('>=')]
        if len(l) == 2:
            if "Morpho" in subprocess.check_output(["repoquery", "-".join([x.strip() for x in l]), '--qf=%{vendor}']):
                o_val = install_dict[l[0]]
                install_dict[l[0]] = max(o_val, l[1])

#for key, val in sorted(install_dict.items()):
print " ".join(["{}-{}".format(key,val) for key,val in sorted(install_dict.items())])

