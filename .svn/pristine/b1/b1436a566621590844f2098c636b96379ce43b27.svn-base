#!/bin/bash

# Get VM name from product and test suite 
# This helper function is sourced by several other scripts
getVMname() {
    testsuite_names="operational bagjam calibration webconfig"
    prod=$1
    tname=$2
    local tsuite="${prod}-f20"
    if [ -z $tname ] || [ $tname == "ALL" ] ; then
        tsuite="${prod}-f20"
    else
        for myname in $testsuite_names
        do
            if [ $myname == $tname ] ; then
                tsuite="${prod}-${tname}-f20"
                break
            fi
        done
    fi
    echo $tsuite
}

