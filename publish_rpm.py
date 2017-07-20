#!/usr/bin/env python

'''
publish rpm files to repo
'''

from __future__ import print_function
import sys, os
import argparse
import glob
import subprocess
import publish_utils
import re
import fnmatch

def get_args(args):
    parser = argparse.ArgumentParser(description="RPM publishing script")
    parser.add_argument('svnrev', help="SVN revision of RPM to publish")
    parser.add_argument('rpmname', help="Name of RPM to publish")
    parser.add_argument('--ver', help="Explicit version number", default='*')
    parser.add_argument('--repo', choices=['release', 'rawhide', ''],
                        default='',
                        help="Repository to publish to")
    parser.add_argument('--osver', help="OS version to release to if not F20",
                        default="20")
    return parser.parse_args(args)


def main():
    '''main code'''
    exit_code = 0
    args = get_args(sys.argv[1:])
    repo_str = os.path.join(publish_utils.REPO_BASE, args.repo,
                            "fedora-%s/" %args.osver)

    # glob all the files
    rpm_files = []
    for rpmd in publish_utils.RPM_DIRS:
        sys.stderr.write("Walking %s for files matching %s-*-%s.fc%s.*.rpm\n" %(rpmd, args.rpmname, args.svnrev, args.osver))
        for root, dirs, files in os.walk(rpmd):
            for filename in fnmatch.filter(files, '%s-%s-%s.fc%s.*.rpm' %(args.rpmname, args.ver, args.svnrev, args.osver)):
                rpm_files.append(os.path.join(root, filename))
    sys.stderr.write("Found {} RPMS: {}\n".format(len(rpm_files),rpm_files))

    for rpmf in rpm_files:
        sys.stderr.write("SCP {} to {}\n".format(rpmf,repo_str))
        cmd = ["scp", rpmf, "ctxswbld@edsrepo.morphodetection.com:%s" %repo_str]
        subprocess.check_call(cmd)
    if len(rpm_files) == 0:
        exit_code = 1
        # No point in executing createrepo if we didn't add any new files
        sys.stderr.write("WARNING: Did not find any RPM files matching the string: %s-%s-%s.fc%s.*.rpm\n"
              %(args.rpmname, args.ver, args.svnrev, args.osver))
        sys.exit(exit_code)

    try:
        publish_utils.update_repo(repo_str)
        sys.stderr.write("Moved %s rpm file(s) to %s\n" % (args.rpmname, repo_str))
    except Exception as e:
        exit_code = 1
        sys.stderr.write(e.__str__())

    if args.ver == '*':
        # We need to extract a version out of the list somehow
        # We will just use the first entry we find - it should be good enough.
        res = re.search("[0-9]+\.[0-9]+\.[0-9]+", rpm_files[0])
        if res is None:
            sys.stderr.write("No version found! No downstream builds will be triggered.\n")
            sys.exit(0) # Exit with zero so builds don't fail..
        sys.stdout.write("{}".format(res.group(0)))
    else:
        sys.stdout.write("{}".format(args.ver))

    sys.exit(exit_code)

if __name__ == "__main__":
    main()

