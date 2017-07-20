#!/usr/bin/env python

'''
publish npm files to repo
'''

from __future__ import print_function
import sys, os
import argparse
import glob
import subprocess
import publish_utils
import re
import fnmatch

def main():
    '''main code'''
    exit_code = 0

    # glob all the files
    npm_dirs = []
    for npmd in publish_utils.NPM_DIRS:
        sys.stderr.write("Walking %s for files matching package.json\n" %(npmd))
        for root, dirs, files in os.walk(npmd):
            for filename in fnmatch.filter(files, 'package.json'):
                npm_dirs.append(root)
    sys.stderr.write("Found {} packages: {}\n".format(len(npm_dirs),npm_dirs))

    for npmd in npm_dirs:
        sys.stderr.write("publishing {}\n".format(npmd))
        cmd = ["npm", "publish", npmd, "--force"]
        subprocess.check_call(cmd)
    if len(npm_dirs) == 0:
        exit_code = 1
        # Error & exit immediately if we didn't add any new files
        sys.stderr.write("WARNING: Did not find any files matching the string: package.json\n")
        sys.exit(exit_code)

    sys.exit(exit_code)

if __name__ == "__main__":
    main()

