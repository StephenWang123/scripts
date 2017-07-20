# ==============================================================================
# Manual Process for each release:
#   1. PROJECT is fixed for all Postman releases ("Postman")
#   2. PREFIX is first 5 chars of Project name (not including "demo_" if exists)
#   3. create a new TESTPLAN based on release name like "Postman_1_SP2"
#   4. Project and Prefix and Testplan are case sensitive
#
# Note: to direct results to demo server, make Project begin with "demo_"
# ==============================================================================
# Parameters ${release}"

project="Postman" # project is fixed
project="demo_Postman" # temporary hack; points to demo testlink

# This is where additional test suites need to be added
# this support is added to allow one or more testsuites to
# be executed within a VM/Docker container (the default being ALL)
ALL_TESTSUITES="operational bagjam calibration webconfig"

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

testplan=$1 # testplan is release name, something like "Postman_1_SP2"
product=$2
testsuites=$ALL_TESTSUITES  # to support backward compatibility

# Allow running of one or more test suites
if [[ $# -ge 3 ]] ; then
    shift 2
    if [[ $1 != "ALL" ]]; then
        testsuites="$*" # just the test suites that the user wants
    fi
fi

echo "Running regressions.sh with Parameters:"
echo "project=$project"
echo "testplan(release)=$testplan"
echo "product=$product"
echo "testsuites=$testsuites"

api_key="d32071b6f2783f13eb4ececfe91e0d8e"

# verify status of services; accepts a space-delimited string of service names
verify_services () {
    # get function parameter of service names
    svcs=$1

    # run service status
    echo "Verify eds services start"
    for svc in $svcs; do
        systemctl status $svc
    done
    echo "Verify eds services end"

    # verify services are in running state before starting tests
    ii=1
    for svc in $svcs; do
        result=$(systemctl status $svc | grep "Active: active (running)")
        # check return status
        if [ -z "$result" ]; then
            echo "FAILED Service: ${svc} failed"
            exit $ii
        fi
        ii=$(expr $ii + 1)
    done
}


if [[ $product == "RAIN" ]]; then
    # run test for eds-rain (mux server) and then exit script
    verify_services "cenprovider"
    framework.py --project=${project} --testplan=${testplan} --demoapikey=${api_key} run --init --pkg=fdr
    exit $?
fi


verify_services "systemcontrol sc-sim muxhost"


# ==================== SET APPLICATION LOGLEVEL PROPERTIES =====================
# control the file (creation deletion) here between framework calls or just
# once at the top.
# find the original files in /etc/eds/*properties
#
# make the regressions folder because it does not pre-exist.
# mkdir /home/mdi/regressions
# properties=/home/mdi/regressions/regressions.properties
# each override per line. samples here
# echo "log4cplus.logger.MC.SYS.HEX   =DEBUG" >> $properties
# echo "log4cplus.logger.MC.SYS.INS   =DEBUG" >> $properties
# echo "log4cplus.logger.MC.SYS.PWR   =DEBUG" >> $properties


# we keep accumulating the exit codes and return the code at the end.
code=0

# Run each test suite. The default (backward-compatible) mode would be to run all
# the tests
for mytest in $testsuites
do
    if [[ "$mytest" == "webconfig" ]]; then
        xvfb-run -a framework.py --project=${project} --testplan=${testplan} --demoapikey=${api_key} run --init --pkg=webconfig
    else
        framework.py --project=${project} --testplan=${testplan} --demoapikey=${api_key} run --init --pkg=$mytest
    fi
    code=$(($code + $?))
done

# IQBAG
#framework.py --project=${project} --testplan=${testplan} --demoapikey=${api_key} run --init --pkg=iqbag
code=$(($code +  $?))


# at last we send out exit code
exit $code


