#!/usr/bin/env python

import argparse
import subprocess
import re
import trigger_build

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('rpmname')
    parser.add_argument('rpmver')
    return parser.parse_args()

args = get_args()

rebuild_list = set()

ds = subprocess.check_output(["repoquery", "--whatrequires", "-".join([args.rpmname, args.rpmver]), "--enablerepo=eds-rawhide", '--qf=%{vendor}:%{name}-%{version}', "--quiet"])
for l in ds.split('\n'):
    l = l.split(':')
    if 'Morpho' in l[0]:
        rebuild_list.add(l[1])

rebuild_list2 = set()

for rpm in [x for x in rebuild_list if args.rpmname not in x]:
    ot = subprocess.check_output(["repoquery", "--requires", rpm, "--enablerepo=eds-rawhide", "--quiet"])
    rpml = []
    for l in ot.split('\n'):
        l = l.split('>=')
        if len(l) == 2:
            rpml.append( "-".join([x.strip() for x in l]) )
    if "-".join([args.rpmname, args.rpmver]) in rpml:
        rebuild_list2.add(rpm)

rebuild_list2 = [x for x in rebuild_list2 if re.search('[0-9]+\.[0-9]+\.[0-9]+', x) is not None]

rebuild_list2 = sorted(set([re.sub("[0-9+]+$", "x", x)+"-build-setup" for x in rebuild_list2]))

print "Found jobs to rebuild: {}".format(rebuild_list2)

for job in rebuild_list2:
    print "Triggering build: {}".format(job)
    trigger_build.trigger_build(job)
