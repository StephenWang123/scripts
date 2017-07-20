#!/usr/bin/python
'''publish eds top level rpms to repo'''

import sys, os
import glob
import shutil
import subprocess
import argparse
import publish_utils

F20_REPO = "/net/eng-svnshare/repo/fedora-20/"
ISO_DIR = '/net/eng-svnshare/svnshare/builds/collabnet/EDS'
MOUNT = "/mnt/iso"
UMOUNT = "sudo umount %s" % MOUNT
CREATEREPO = "sudo createrepo --update %s -c %s/repocache" %(F20_REPO, F20_REPO)

def get_args():
    parser = argparse.ArgumentParser("ISO publisher")
    parser.add_argument("iso_basename", help="base name of ISO file to publish")
    parser.add_argument('--repo', choices=['release', 'rawhide', ''],
                        default='',
                        help="Repository to publish to")
    parser.add_argument('--osver', help="OS version to release to if not F20",
                        default="20")
    args = parser.parse_args()
    return args


def main():
    '''main code'''
    exit_code = 0
    args = get_args()
    repo_str = os.path.join(publish_utils.REPO_BASE, args.repo,
                            "fedora-%s/" %args.osver)

    if not os.path.exists(MOUNT):
        os.system("sudo mkdir %s  >/dev/null 2>&1" %  MOUNT)

    files = "%s/%s_*-*_*/*.iso"  % (ISO_DIR, args.iso_basename)
    newest = max(glob.iglob(files), key=os.path.getctime)
    print "Found ISO(s):", newest
    os.system("sudo mount %s %s -o user" % (newest, MOUNT))
    eds_rpm = glob.glob("/mnt/iso/eds-*.fc20.noarch.rpm")
    print "Found top-level RPMs:", eds_rpm
    if len(eds_rpm) == 0:
        print "WARNING: Did not find any RPMs matching the string: /mnt/iso/eds-*.fc20.noarch.rpm"
        os.system(UMOUNT)
        sys.exit(1)

    for file_name in eds_rpm:
        try:
            subprocess.check_call(["scp", file_name, "ctxswbld@edsrepo.morphodetection.com:%s" %repo_str])
        except Exception, e:
            print "Failed to scp", file_name
            os.system(UMOUNT)
            sys.exit(1)
    os.system(UMOUNT)

    try:
        publish_utils.update_repo(repo_str)
        print "Moved %d files to %s" %(len(eds_rpm), repo_str)
    except Exception, e:
        exit_code = 1
        print e
    sys.exit(exit_code)

if __name__ == "__main__":
    main()



