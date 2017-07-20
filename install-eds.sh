#!/bin/bash
#
# From:
#   http://eng-scmsrv-01:8080/job/install-eds/configure
# Usage: $0 ${Release_Name} ${product} ${iso_dir} [${testsuite}]
# Example: $0 Postman_1_SP5 5800 \
#          /net/eng-svnshare/svnshare/builds/collabnet/REGRESSIONS bagjam
#
echo "ctx sw installation ..."

if [[ $# -lt 3 ]]; then
    echo "Usage: $0 <Release_Name> <product> <iso_dir> [${testsuite}]"
    echo "For example,"
    echo "$0 Postman_1_SP5 5800 /net/eng-svnshare/svnshare/builds/collabnet/REGRESSIONS"
    echo "Or,"
    echo "$0 Postman_1_SP5 5800 /net/eng-svnshare/svnshare/builds/collabnet/REGRESSIONS bagjam"
    exit 1
fi

REALPATH=$(realpath $0)
echo "REALPATH=${REALPATH}"
BASEDIR=$(dirname "$REALPATH")
echo "BASEDIR=${BASEDIR}"

source ${BASEDIR}/getvmname.sh

Release_Name=$1
product=$2
iso_dir=$3
VMName=$(getVMname $2 $4)

echo "${Release_Name}, ${product}, ${iso_dir}, ${VMName}"

# on ${VMName}
ssh root@${VMName} "python  ${BASEDIR}/auto_install.py -i ${Release_Name} -p ${product} -s ${iso_dir}"

MPATH=/net/eng-svnshare/repo/fedora-20/

#echo "install insp ..."
# This will always throw an error because the hostname is set to 'product-f20'
# but the add_insp_enum DB call only accepts 'host'
#if [ ${insp_name} != '' ]
#then
#  ssh root@${product}-f20 "sudo yum install -y ${MPATH}${insp_name}.fc20.x86_64.rpm"
#fi

echo "Some setup ..."
ssh root@${VMName} "${BASEDIR}/setup_vm.sh ${product} ${Release_Name}"

echo "run Regressions ..."
ssh geeds@${VMName} "${BASEDIR}/regressions.sh ${Release_Name} ${product}"

# Jenkins test result information
echo "======================================"
# first clean up workspace before we pull results; old files make jenkins fail
echo "remove old workspace files"
rm -f ${WORKSPACE}/jenkins-*.xml

echo "Collect Jenkins Junit result files ..."
ssh root@${VMName} ls -l /home/mdi/regressions/jenkins-*.xml
echo "scp root@${VMName}:/home/mdi/regressions/jenkins-*.xml ${WORKSPACE}/."
scp root@${VMName}:/home/mdi/regressions/jenkins-*.xml ${WORKSPACE}/.

echo "Current VM Hostname=$hostname"
echo "Jenkins Workspace=$WORKSPACE"
ls $WORKSPACE
echo "======================================"


