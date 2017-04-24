#!/bin/bash
set -e

USAGE="Usage: $0 current version upgrade version"

if [ $# -ne 2 ];
then
    echo "Requires exactly 2 arguments: current and upgrade versions"
    echo $USAGE
    exit 1
fi

cp ./test/files/build_vars.yml.clustered_vsd roles/reset-build/files/build_vars.yml
cp ./test/files/upgrade_vars.yml.clustered_vsd roles/reset-build/files/upgrade_vars.yml
cp ./test/files/test_install.yml .
cp ./test/files/test_cleanup.yml .

sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$2/g" roles/reset-build/files/upgrade_vars.yml
#update ansible.cfg
echo "[ssh_connection]" >> ansible.cfg
echo "ssh_args = -o ControlMaster=auto -o ControlPersist=600s" >> ansible.cfg
echo "pipelining = True" >> ansible.cfg

# generate build vars for deployment
./metro-ansible reset_build.yml -vvvv
./metro-ansible build.yml -vvvv
# run the VSP deployment
./metro-ansible test_install.yml -vvvv
#delete any vsd backups and reports from previous jobs
rm -rf /tmp/backup
rm -rf ./reports/
# reset the env before upgrade
./metro-ansible reset_build.yml -vvvv
# create build vars required for upgrade
./metro-ansible build_upgrade.yml -vvvv
# run upgrade
# Upgrade vsd 1 and 3
./metro-ansible vsd_ha_node1_3_upgrade.yml -vvvv
# Upgrade VSC1
./metro-ansible vsc_ha_node1_upgrade.yml -vvvv
# Upgrade VSC2
./metro-ansible vsc_ha_node2_upgrade.yml -vvvv
# Upgrade VSD2
./metro-ansible vsd_ha_node2_upgrade.yml -vvvv
# clean up the whole setup
./metro-ansible test_cleanup.yml -vvvv
