#!/usr/bin/python
'''
    This script is called from eds-install jenkins job for each product.
    Manages uninstall and new install of product software
    auto_install.py -i <Release_name> -p <Product>
    auto_install.py -i Postman_1_SP1 -p 9800SEIO_CB_HS
    -s iso_dir optional, defaults to EDS dir.
    A local copy of the ISO is also retained in /home/mdi/eds_repo
'''
from __future__ import print_function
import os
import sys
import glob
import argparse


PARSER = argparse.ArgumentParser()
PARSER.add_argument('-i', action='store', dest='release_name',
                    required=True,
                    help='The name of the iso file to be mounted.')
PARSER.add_argument('-p', action='store', dest='product',
                    required=True,
                    help='EDS type name.')
PARSER.add_argument('-s', action='store', dest='iso_dir',
                    help='directory to search for target iso')
PARSER.add_argument('-c', action='store', dest='site',
                    default='TSA',
                    help='site customization, default is TSA')


ARGS = PARSER.parse_args()

# resolve iso directory
ISO_DIR = ARGS.iso_dir or '/net/eng-svnshare/svnshare/builds/collabnet/EDS'

print('ISO Release Name: ', ARGS.release_name)
print('EDS Product Name: ', ARGS.product)
print('Iso Dir: ', ISO_DIR)
print('Site Customization: ', ARGS.site)

MOUNT = '/mnt/iso'
# Now get the base directory of where this script
# (the one being invoked) resides and then get the
# yum repo template
SOURCE = os.path.split(os.path.realpath(sys.argv[0]))[0]
SOURCE = os.path.join(SOURCE, 'iso.repo')

DEST = '/etc/yum.repos.d/localeds.repo'
# note: dash in format string avoids picking up additional files.
RELEASE_WILDCARD = '{}/EDS_Software*/*{}-*.iso'.format(ISO_DIR,
                                                       ARGS.release_name)
print('Release Wildcard:', RELEASE_WILDCARD)
PRODUCT = ARGS.product
LOCAL_REPO = '/home/mdi/eds_repo'

RAIN = ARGS and 'RAIN' in ARGS.product

# sed replacements for the iso.repo file's contents
SED_REPL = (r"sed -e 's/baseurl=.*/baseurl=file:\/\/\/home\/mdi\/eds_repo\//' "
            r" -e 's/^name=ISO Repo/name=Local EDS Repo/' "
            r" -e 's/\[ISO-Install\]/\[localeds\]/' {} > {}")

# Some info from: http://yum.baseurl.org/wiki/RepoCreate


def get_latest_release():
    ''' get latest release iso by release name '''
    print('Looking for Latest Release for {}'.format(ARGS.release_name))
    latest = max(glob.iglob(RELEASE_WILDCARD), key=os.path.getctime)
    print('Found Latest Version {}'.format(latest))
    return latest


def execute(desc, command):
    ''' print and execute command '''
    print('SCRIPT auto_install.py,', desc, ':', command)
    rcode = os.system(command)
    memo = 'Non-zero exit code: {}, on cmd:{}'.format(rcode, command)
    assert rcode == 0, memo


def make_local_repo():
    ''' Makes a local copy of the RPMs from the mounted ISO '''

    if os.path.exists(LOCAL_REPO):
        cmd = 'rm -rf {}'.format(LOCAL_REPO)
        execute('Removing preexisting local repo directory: {}'.format(
            LOCAL_REPO), cmd)

    execute('Create local repo directory: {}'.format(LOCAL_REPO),
            'mkdir -p {}'.format(LOCAL_REPO))

    cmd = 'cp -R {}/* {}'.format(MOUNT, LOCAL_REPO)
    execute('Copy eds software to local repo directory', cmd)

    cmd = 'createrepo {}'.format(LOCAL_REPO)
    execute('Creating repo for local directory {}'.format(LOCAL_REPO), cmd)


def customize():
    ''' install site customization '''
    if RAIN:
        conf = 'yum -y install eds-conf-{}-other'.format(ARGS.site)
        execute('RAIN customization install', conf)
    else:
        conf = 'yum -y install eds-conf-{}-host'.format(ARGS.site)
        execute('Eds customization install', conf)


def install():
    ''' manage uninstall and installation of product software '''
    print('Starting Installation of {} and {}'.format(ARGS.release_name,
                                                      ARGS.product))
    if not os.path.exists(MOUNT):
        execute('Create Mount point', 'mkdir -p {}'.format(MOUNT))

    fix = "sh -c 'echo \'testuser:x:1001:testuser\' >> /etc/group'"
    execute('Fix /etc/group', fix)

    # create repo file in /etc/yum.repos.d/
    execute('Create Yum Repo file', SED_REPL.format(SOURCE, DEST))

    execute('Mount Release', 'mount {} {}'.format(get_latest_release(), MOUNT))

    # Removal is necessary for testing on same vm
    # During production run the vm's auto-generated each time
    execute('Remove Regressions', 'yum -y remove regressions-*')

    execute('Remove MUX demo', 'yum -y remove mux-demo')
    execute('Remove Sim', 'yum -y remove systemcontrol-sim*')

    # display hosts file in case something strange is going on
    execute('Display Hosts File', 'cat /etc/hosts')

    execute('Remove Product', 'yum -y remove edscommon*')

    make_local_repo()

    product = 'yum -y install eds-{}-*'.format(PRODUCT)
    execute('Yum Install', product)

    if RAIN:
        execute('MUX demo apps install', 'yum -y install mux-demo')
    else:
        execute('Sim Install', 'yum -y install systemcontrol-sim*')

    customize()

    execute('Display Hosts File', 'cat /etc/hosts')

    execute('Unmount Release', 'umount {}'.format(MOUNT))


def main():
    ''' main '''
    # sudo python auto_install2.py -i Postman_1_SP1
    install()


if __name__ == "__main__":
    main()
