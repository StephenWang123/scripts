#!/usr/bin/env python

import sys
import subprocess
import re
import argparse

def get_rpm_reversedeps(pkg_name):
    rpms = subprocess.check_output(['repoquery', '--whatrequires', pkg_name, '--enablerepo=eds-rawhide', '--qf', "%{name} %{version}"])
    rpms = rpms.split('\n')

    ver_dict = dict()
    for r in [x.split() for x in rpms if len(x.split()) == 2]:
        if re.match('[0-9]+\.[0-9]+\.[0-9]+', r[1]) and '-devel' not in r[0]:
            if r[0] not in ver_dict.keys():
                ver_dict[r[0]] = [r[1]]
            else:
                if r[1] not in ver_dict[r[0]]:
                    ver_dict[r[0]].append(r[1])
                    ver_dict[r[0]].sort()

    #for k,v in ver_dict.items():
    #    print k, v[-1]
    return ver_dict

def get_jenkins_names(name, version):
    # Simple string concat here
    # But first we need to replace the last number with an 'x'
    version = version.split(".")
    version[-1] = 'x'
    version = ".".join(version)
    return "-".join([name, version, 'build-setup'])

def get_args():
    parser = argparse.ArgumentParser("python depsolver")
    parser.add_argument('pkg_name', help='name of package to query')
    return parser.parse_args()

def main():
    args = get_args()
    vers = get_rpm_reversedeps(args.pkg_name)
    for k, v in vers.items():
        print get_jenkins_names(k, v[-1])

if __name__ == '__main__':
    main()
