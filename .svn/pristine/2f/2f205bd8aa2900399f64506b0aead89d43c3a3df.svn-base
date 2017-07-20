#!/usr/bin/env python

from __future__ import print_function
import argparse
import shutil
import os
import glob
import sys
import platform

def get_args(args):
    parser = argparse.ArgumentParser("Recon library pusher")
    parser.add_argument("ver", help="Recon version to publish")
    parser.add_argument("svnrev", help="SVN revision")
    parser.add_argument("job", help="Jenkins job name")
    parser.add_argument("osver", help="Operating system version")
    return parser.parse_args(args)

def main():
    args = get_args(sys.argv[1:])
    print("OS version: ", args.osver)
    print("SVN revision: ", args.svnrev)
    print("Job name: ", args.job)
    lib_dir = "/net/eng-svnshare/svnshare/builds/collabnet/LIB/%s_%s-f%s-%s" %(args.job, args.ver, args.osver, args.svnrev)
    if not os.path.exists(lib_dir):
        os.makedirs(lib_dir)

    libroot = "./build/"

    libs = []
    with open("version.txt") as verfile:
        for line in verfile.readlines():
            pair = line.split('=')
            print("Processing version info:", pair)
            libs = libs + glob.glob(libroot + ("lib%s*%s.so" %(pair[0].lower(), pair[1].strip())))

    for lib in libs:
        print("Copying", lib, "into", lib_dir)
        shutil.copy(lib, lib_dir)

if __name__ == "__main__":
    main()
