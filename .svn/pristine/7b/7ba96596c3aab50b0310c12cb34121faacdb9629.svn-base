#!/bin/bash
# From:
#   http://eng-scmsrv-01.morphodetection.com:8080/job/daily_eds_regressions/configure
# Usage: $0 ${Repo_Source} ${Release_Name} ${product} ${iso_dir} 
# Example: rawhide|release Postman_1_SP5 5800 \
#          /net/eng-svnshare/svnshare/builds/collabnet/REGRESSIONS bagjam
# CUSTOMIZED FOR DAILY REGRESSIONS BUILD

set -e

BASEDIR=$(dirname "$0")

REALPATH=$(realpath $0)
echo "REALPATH=${REALPATH}"
BASEDIR=$(dirname "$REALPATH")
echo "BASEDIR=${BASEDIR}"

if [[ $# -lt 4 ]]; then
    echo "Usage: $0 <Repo_Source> <Release_Name> <product> <iso_dir>"
    echo "For example,"
    echo "$0 rawhide Postman_1_SP5 5800 /net/eng-svnshare/svnshare/builds/collabnet/REGRESSIONS"
    echo "Or,"
    echo "$0 release Postman_1_SP5 5800 /net/eng-svnshare/svnshare/builds/collabnet/REGRESSIONS"
    exit 1
fi
REPO_DIR=/net/eng-svnshare/repo/fedora-20

Repo_Source=$1
Release_Name=$2
product=$3
iso_dir=$4


if [ "${Repo_Source}" == "rawhide" ]
then
  repopt='--rawhide'
  yumopt='--enablerepo=eds-rawhide'
  sudo yum-config-manager --enable eds-rawhide
else
  repopt=''
  yumopt=''
fi

#enabling eds-rawhide before calling 'yum clean all' & 'yum makecache' and
#disableing it afterwards to fix weird yum issue were cache doesn't update correctly if only yumopt is used.
sudo yum clean all 
sudo yum makecache 

if [ "${Repo_Source}" == "rawhide" ]
then
  sudo yum-config-manager --disable eds-rawhide
fi

# HACK 
sudo rpm -e --nodeps doc-common || true

# Install edscommon/-devel in case it is missing
sudo yum install -y edscommon edscommon-devel $yumopt

cd ${WORKSPACE}
svn upgrade .

REGRESSIONS=/net/eng-svnshare/svnshare/builds/collabnet/REGRESSIONS
RELDIR=${WORKSPACE}/EDS/
RELPKGDIR=${WORKSPACE}/build/
mkdir -p ${RELDIR}
mkdir -p ${RELPKGDIR}
# Hm... Should ignoring version mismatch be default behavior?
# Lame as hell, but run it as root. 
sudo ./relmgr --ignore-package-version-mismatch ${repopt} build ${Release_Name} ${RELDIR} ${RELPKGDIR}


# tsid=$(ls ${RELDIR}/*.iso | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)
tsid=$(basename -s .iso ${RELDIR}/*.iso)

#make reldir on repo
ssh ctxswbld@edsrepo.morphodetection.com "mkdir -p ${REGRESSIONS}/${tsid}"

scp ${RELDIR}/*.iso ctxswbld@edsrepo.morphodetection.com:${REGRESSIONS}/${tsid}/

# Let's generate some release notes!
echo "Generating release notes..."
cd release_notes
rel_no_space=`echo ${Release_Name} | sed 's/_//g'`
./milkyway_release_notes.py cdlan ${clan_pass} Milky-Way ${rel_no_space}
scp ${rel_no_space}_Release_Notes.rtf ctxswbld@edsrepo.morphodetection.com:${REGRESSIONS}/${tsid}/

echo "Uploaded to ${REGRESSIONS}/${tsid}"

# clan 2/10/16 Note: I removed create-vm-matrix from the post-build steps to cut down on cruft
