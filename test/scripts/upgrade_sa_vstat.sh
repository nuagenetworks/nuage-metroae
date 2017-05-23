#!/bin/bash
set -e

USAGE="Usage: $0 current version upgrade version"

if [ $# -ne 2 ];
then
    echo "Requires exactly 2 arguments: current and upgrade versions"
    echo $USAGE
    exit 1
fi

cp ./test/files/build_vars.yml.standalone_vsd_vstat roles/reset-build/files/build_vars.yml
cp ./test/files/upgrade_vars.yml.standalone_vsd roles/reset-build/files/upgrade_vars.yml
cp ./test/files/test_install.yml .
cp ./test/files/test_cleanup.yml .
cp ./test/files/user_creds.yml.standalone_vsd ./user_creds.yml

IPADDR=`/usr/sbin/ifconfig | grep netmask | grep broadcast | head -n 1 | awk '{print $2}'`

sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$2/g" roles/reset-build/files/upgrade_vars.yml
#update ansible.cfg
echo >> ansible.cfg
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
# add nfs shared folder to vstat vms
sed -i "s/TARGET_SERVER/$IPADDR/g" test/files/set_nfs_shared_folder.yml
./metro-ansible test/files/set_nfs_shared_folder.yml -vvvv
# reset the env before upgrade
./metro-ansible reset_build.yml -vvvv
# update vsd_operations to health
sed -i '0,/install/ s//health/' build_vars.yml
# create build vars required for upgrade
./metro-ansible build_upgrade.yml -vvvv
# run upgrade
# Upgrade vstat 
./metro-ansible vstat_upgrade.yml -vvvv
# clean up the whole setup
#./metro-ansible test_cleanup.yml -vvvv
