# ==============================================================================
# Debuggin on product vm's? example for 5800
# 1. ssh root@eng-scmsrv-01
# 2. ssh geeds@5800-f20
#
# When ssh into new product vm you will get error because product vm ip changes:
#
#          ... Offending ECDSA key in /root/.ssh/known_hosts:17
# 
# just remove offending keys in /root/.ssh/known_hosts
# re-login
# failed service? 
# journalctl -alb -u <name>.service
#
# ==============================================================================
# From Todd:
# 9800HS CB DMA
# Insp 9800 HS CB ECAC 3.0.5 /  Post-Proc 9800HS DMA CB SC 8.0.0
# Insp 9800 HS CB ECDMD 3.0.5 / Post-Proc 9800HS DMA CB SC  8.0.0
# Insp 9800 HS CB ECDMD 3.0.5 / Post-Proc 9800HS DMA CB SC TUB  8.0.0
# I think Hal only uses one of these, but technically all three certified. The 8.0.0 recon is part of the host software.
# 5800 DMA
# Insp 5800 HDE SB 2.18.8 / Recon 3.1.2
# We are adding 2.17.7 ECAC and 2.17.21 KOM with SP4.
# ==============================================================================

# Exit as soon as any command fails
set -e

# Parameters ${product} ${release}"

product=$1
release=$2
REALPATH=$(realpath $0)
echo "REALPATH=${REALPATH}"
BASEDIR=$(dirname "$REALPATH")
echo "BASEDIR=${BASEDIR}"

echo "Running setup_vm.sh with Parameters:"
echo "product=$product"
echo "release=$release"


if [[ $product == *"_EC"* ]]
then
  echo "product=$product"
  echo "****** Eclipse not supported... skipping ******"
  exit 1
fi

if [[ $product == "RAIN" ]]
then
  echo "product=$product"
  echo "****** setup not needed for RAIN ******"
  exit 0
fi

# define edsname based on product
if [[ $product == "5800"* ]]
then
  edsname="X101"
fi

if [[ $product == "9800"* ]]
then
  edsname="K101"
fi

echo "edsname=$edsname"


# set value and default for edsname; 
# benefit: resetting defaults will not break systemcontrol by erasing the the edsname.
sqlite3 /var/eds/edsconfigs.db "update eds_configs set value='${edsname}', factory_default='${edsname}' where config_id_str='edsname'"

# define edsmodel; should come from database which is implemented but need to update afterwards if it does not work
#edsmodel=$(sqlite3 /var/eds/edsconfigs.db "select value from eds_configs where config_id_str='edsmodel'";)
#echo "database edsmodel=$edsmodel"


# ==============================================================================
# install_sim.sh takes a Product argument which must match config files
#5800
#9800SC
#9800SEIO_HS
#9800SEIO_MS
#9800SEIO_CB_HS

#configs_5800CB_Sim.txt
#configs_5800_Sim.txt
#configs_9800SC_Sim.txt
#configs_9800SEIO_CB_HS_Sim.txt
#configs_9800SEIO_HS_Sim.txt
#configs_9800SEIO_MS_Sim.txt
# ==============================================================================

# Only Postman_1* versions require install_sim script.
if [[ "$release" =~ ^Postman_1.* ]]; then
    # use product2 to give as parameter to install_sim.sh
    product2=$product
    if [[ $product2 == "5800_CB" ]]
    then
      product2="5800CB"
    fi

    # install_sim.sh goes away when we move to systemcontrol 4.3.x
    echo "Remove sudo from install_sim.sh because script is run by root"
    sed -i 's/sudo //' /usr/bin/install_sim.sh
    install_sim.sh ${product2}
    echo "Finished install_sim.sh"
else
    echo "install_sim.sh not required"
fi


systemctl restart muxhost
systemctl restart systemcontrol
systemctl restart sc-sim

sleep 10

# INSTALL INSPECTIONS - 
echo "Install Inspections for product=$product"
# for each product create handler that uninstalls and reinstalls
# this is to support local job running against same vm
# The rpms gets pulled from here: http://eds-repo/repos/fedora-20/?C=M;O=D

# install to enable edsrepo
rpm -i ${BASEDIR}/rpms/edsrepo-nwk-1.1.0-64.fc22.x86_64.rpm

if [[ $product == "5800" ]]
then
  # HACK using -262.fc20 to force the right rpm selection
  # this is failing because strange fake rpm version 12345  
  yum erase -y insp_KOM_SB_2.17.21_recon_3.1.2-2.17.21
  yum install -y insp_KOM_SB_2.17.21_recon_3.1.2-2.17.21-262.fc20 --enablerepo=eds

  yum erase -y insp_ECAC_SB_2.17.7_recon_3.1.2-2.17.7
  yum install -y insp_ECAC_SB_2.17.7_recon_3.1.2-2.17.7-262.fc20 --enablerepo=eds

  yum erase -y insp_HDE_SB_2.18.8_recon_3.1.2-2.18.8
  yum install -y insp_HDE_SB_2.18.8_recon_3.1.2-2.18.8-262.fc20 --enablerepo=eds
fi


if [[ $product == "9800SC" ]]
then
  yum erase -y insp-phx-9800MS-NOCB-HDE-3.0.0
  yum install -y insp-phx-9800MS-NOCB-HDE-3.0.0 --enablerepo=eds
fi


if [[ $product == "9800SEIO_HS" ]]
then
  yum erase -y insp-phx-9800HS-NOCB-HDE-3.0.1
  yum install -y insp-phx-9800HS-NOCB-HDE-3.0.1 --enablerepo=eds
fi


if [[ $product == "9800SEIO_MS" ]]
then
  yum erase -y insp-phx-9800MS-NOCB-HDE-3.0.0
  yum install -y insp-phx-9800MS-NOCB-HDE-3.0.0 --enablerepo=eds
fi


# DUAL ENERGY
if [[ $product == "9800SEIO_CB_HS" ]]
then
  yum erase -y insp-phx-9800HS-CB-DMA-ECDMD-3.0.5_POSTPROC_8.0.0
  yum install -y insp-phx-9800HS-CB-DMA-ECDMD-3.0.5_POSTPROC_8.0.0 --enablerepo=eds

  yum erase -y insp-phx-9800HS-CB-DMA-ECAC-3.0.5_POSTPROC_8.0.0
  yum install -y insp-phx-9800HS-CB-DMA-ECAC-3.0.5_POSTPROC_8.0.0 --enablerepo=eds
fi

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


verify_services "systemcontrol sc-sim muxhost"

