#!/bin/sh
# from: 
# http://eng-scmsrv-01.morphodetection.com:8080/job/product-regressions/configure
#

REALPATH=$(realpath $0)
echo "REALPATH=${REALPATH}"
BASEDIR=$(dirname "$REALPATH")
echo "BASEDIR=${BASEDIR}"

if [[ $# -lt 2 ]] ; then
    echo "Usage: $0 <testplan> <product> [testsuites]"
    echo "testsuites is one or more of of: operational, bagjam, calibration, or webconfig"
    echo "For example:"
    echo "    $0 Postman_1_SP5 5800 operational bagjam"
    echo "Or,"
    echo "    $0 Postman_1_SP5 5800 'operational bagjam'"
    echo "A value of 'ALL' for testsuites can also be used to indicate all testsuites"
    echo "Would run both the operational and bagjam test suites"
    echo "(In the second example, the test suites are passed as a single, space-separated string)"
    echo "The complete list of test suites: $ALL_TESTSUITES"
    exit 1
fi

source ${BASEDIR}/getvmname.sh

Release_Name=$1
product=$2
VMName=$(getVMname $2 $3)
if [[ $# -eq 2 ]]; then
    testsuite="ALL"
else
    testsuite="$3"
fi
echo "ARGS = $*"
echo "Product=${product}"
echo "VMName=${VMName}"

echo "run Regressions ..."
# TODO: need to use geeds login so that sudo will work. Sudo is used to bounce services between tests
# need to make regressions__${product}
# ssh root@${product} "/net/eng-svnshare/svnshare/builds/br_scripts/regressions.sh ${Release_Name}"

sudo ssh geeds@${VMName} "${BASEDIR}/regressions.sh ${Release_Name} ${product} ${testsuite}"


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

