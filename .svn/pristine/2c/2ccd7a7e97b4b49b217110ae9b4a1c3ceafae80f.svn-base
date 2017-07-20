#!/usr/bin/env python

import os
import sys
import subprocess
import signal
import time
from lockfile import LockFile, lockfile_ext

BASEDIR, _ = os.path.split(os.path.realpath(sys.argv[0]))

# LockFile objects require an existing path to lock.
PATH_TO_LOCK = BASEDIR + os.path.sep + "lockfile.py"
LOCK_FILE = "%s%s" % (PATH_TO_LOCK, lockfile_ext())
REPO_BASE = "/net/eng-svnshare/repo/"
RPM_DIRS = [
    os.path.join(os.path.expanduser("~"), "rpmbuild", "RPMS"),
    './build/'
    ]
NPM_DIRS = [
    '.'
]
SIGNALS = {
    signal.SIGABRT: 'SIGABRT',
    signal.SIGILL: 'SIGILL',
    signal.SIGINT: 'SIGINT',
    signal.SIGSEGV: 'SIGSEGV',
    signal.SIGTERM: 'SIGTERM',
    }

def waitforlock(timeout):
    ''' function to wait for a lockfile to not exist '''
    counter = 0
    while counter <= timeout:
        if not os.path.exists(LOCK_FILE):
            return True
        sys.stderr.write("Waiting for lock...\n")
        sys.stderr.flush()
        time.sleep(1)
        counter = counter + 1
    # One more check
    if os.path.exists(LOCK_FILE):
        raise Exception('Unable to acquire lock\n')

def update_repo(repo_str, timeout=600):
    ''' update repo '''
    # Default timeout of 10 minutes
    def sig_handler(signum, frame):
        ''' signal handler '''
        err = "RPM Update Halted. Caught signal %d, %s.\n" % (signum, SIGNALS[signum])
        raise Exception(err)

    for sig in SIGNALS.keys():
        signal.signal(sig, sig_handler)

    sys.stderr.write("Executing createrepo\n")
    # We only want one process to call createrepo at a time
    waitforlock(timeout)

    with LockFile(PATH_TO_LOCK) as lockfile:
        subprocess.check_call(["sudo", "createrepo", repo_str,
                               "-c", repo_str + "/repocache", "--update",
                               "--workers", "10", '--verbose'],
                              stdout=sys.stderr)

def main():
    ''' main function '''
    # Test
    print(LOCK_FILE)

if __name__ == '__main__':
    main()
