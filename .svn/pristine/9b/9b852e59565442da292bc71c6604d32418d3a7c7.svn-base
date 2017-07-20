#!/bin/bash
# From:
#   http://eng-scmsrv-01:8080/job/create-vm/configure

# set -x

REALPATH=$(realpath $0)
echo "REALPATH=${REALPATH}"
BASEDIR=$(dirname "$REALPATH")
echo "BASEDIR=${BASEDIR}"

source ${BASEDIR}/getvmname.sh

product=$1
VMName=$(getVMname $1 $2)

echo "product=$product"
echo "VMName = ${VMName}"

echo "remove the VM if it exist ..."
ssh -A -t ctxswbld@eng-vmhost09 "sudo virsh list | grep ${VMName}"

retcode=$?
echo ${retcode}

if [ $retcode -eq 0 ]
then
  echo "found ${VMName}"
  ssh -A -t ctxswbld@eng-vmhost09 "sudo eru f20-regressions ${VMName} shutdown"
  sleep 30
  ssh -A -t ctxswbld@eng-vmhost09 "sudo eru f20-regressions ${VMName} destroy"
  sleep 60
fi

echo "create the VM, wait for up to 40 mins ..."
ssh -A -t ctxswbld@eng-vmhost09 "sudo eru f20-regressions ${VMName} create"

echo "start the VM, wait for up to 40 sec ..."
ssh -A -t ctxswbld@eng-vmhost09 "sudo eru f20-regressions ${VMName} start"
sleep 40

# remove key from .ssh/known_hosts
ssh-keygen -R ${VMName}

