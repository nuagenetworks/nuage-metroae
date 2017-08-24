#!/bin/bash
set -e

USAGE="Usage: $0 current version upgrade version"

if [ $# -ne 2 ];
then
    echo "Requires exactly 2 arguments: current and upgrade versions"
    echo $USAGE
    exit 1
fi

IPADDR=`/usr/sbin/ifconfig | grep netmask | grep broadcast | head -n 1 | awk '{print $2}'`

cp ./test/files/build_vars.yml.standalone_vsd roles/reset-build/files/build_vars.yml
sed -i "s/TARGET_SERVER/$IPADDR/g" test/files/upgrade_vars.yml.vcs
cp ./test/files/upgrade_vars.yml.vcs roles/reset-build/files/upgrade_vars.yml
cp ./test/files/test_install.yml .
cp ./test/files/test_cleanup.yml .
cp ./test/files/user_creds.yml.standalone_vsd ./user_creds.yml

sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$2/g" roles/reset-build/files/upgrade_vars.yml
#update ansible.cfg
echo >> ansible.cfg
echo "[ssh_connection]" >> ansible.cfg
echo "ssh_args = -o ControlMaster=auto -o ControlPersist=600s" >> ansible.cfg
echo "pipelining = True" >> ansible.cfg

# generate build vars for deployment
./metro-ansible reset_build.yml --extra-vars "test_run=True" -vvvv
./metro-ansible build.yml --extra-vars "test_run=True" -vvvv
# run the VSP deployment
./metro-ansible test_install.yml -vvvv
#delete any vsd backups and reports from previous jobs
rm -rf /tmp/backup
rm -rf ./reports/
# reset the env before upgrade
./metro-ansible reset_build.yml --extra-vars "test_run=True" -vvvv
# create build vars required for upgrade
./metro-ansible build_upgrade.yml -vvvv
# run upgrade
# Upgrade vsd 1
./metro-ansible vsd_sa_upgrade.yml -vvvv
# Upgrade VSC1
./metro-ansible vsc_node1_upgrade.yml -vvvv
# Upgrade VSC2
./metro-ansible vsc_ha_node2_upgrade.yml -vvvv
# Upgrade vstat
./metro-ansible vstat_upgrade.yml -vvvv
# clean up the whole setup
#./metro-ansible test_cleanup.yml -vvvv
