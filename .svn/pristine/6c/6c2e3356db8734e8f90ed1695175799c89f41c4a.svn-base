#!/bin/bash

REALPATH=$(realpath $0)
echo "REALPATH=${REALPATH}"
BASEDIR=$(dirname "$REALPATH")
echo "BASEDIR=${BASEDIR}"

source ${BASEDIR}/getvmname.sh

product=$1
VMName=$(getVMname $1 $2)

echo "Run ansible on the VM, ${VMName}"
ssh geeds@f20-puppet "cd vm_setup/ansible; sudo ansible-playbook -i hosts -l ${VMName}  regressions-setup.yml"
