#!/bin/sh
set -e
USAGE="Usage: $0 version"

if [ $# -ne 1 ];
then
    echo "Requires exactly 1 argument"
    echo $USAGE
    exit 1
fi

if [ $1 = 4.0.R4 ] || [ $1 = 3.2.R10 ];
then
    sed -i  '/- { hostname: {{ vrs_u16_host_name }},/,/ci_flavor: m1.medium }/d' test/files/build_vars.yml.CI.j2
fi

# Use heat to deploy VMs on OpenStack
cp ./test/files/setup.yml.CI setup.yml
ansible-playbook setup.yml -vvvv
ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible ci_predeploy.yml -vvvv
./metro-ansible ci_deploy.yml -vvvv

# Setup and run
cp ./test/files/test_install.yml .
cp ./test/files/test_cleanup.yml .

IPADDR=`/usr/sbin/ifconfig | grep netmask | grep broadcast | head -n 1 | awk '{print $2}'`

# ci-deploy has fixed up the build_vars files for us.
cp ./test/files/build_vars_vsdonly.yml roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml

ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible test_install.yml -vvvv

cp ./test/files/build_vars_vsconly.yml roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml
ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible test_install.yml -vvvv

cp ./test/files/build_vars_vstatonly.yml roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml
ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible test_install.yml -vvvv

cp ./test/files/build_vars_vrsonly.yml roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml
ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible test_install.yml -vvvv

cp ./test/files/build_vars_vnsonly.yml roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml
ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible test_cleanup.yml -vvvv

cp ./test/files/build_vars_vnsonlywithvsc.yml roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml
ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible install_vns.yml -vvvv

cp ./test/files/build_vars_all.yml roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml
ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible test_cleanup.yml -vvvv

./metro-ansible ci_destroy.yml -vvvv

