#!/bin/bash
set -e
USAGE="Usage: $0 version"

if [ $# -ne 1 ];
then
    echo "Requires exactly 1 argument"
    echo $USAGE
    exit 1
fi

USAGE="Usage: $0 version"

if [ $# -ne 1 ];
then
    echo "Requires exactly 1 argument"
    echo $USAGE
    exit 1
fi

if [ $1 = 4.0R4 ] || [ $1 = 3.2R10 ];
then
    sed -i  '/- { hostname: {{ vrs_u16_host_name }},/,/ci_flavor: m1.medium }/d' test/files/build_vars.yml.CI.j2
fi

cp ./test/files/setup.yml.CI setup.yml
ansible-playbook setup.yml -vvvv
ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
if [ $1 = 4.0R4 ] || [ $1 = 3.2R10 ];
then
    sed -i  '/- { hostname: {{ vrs_u16_target_server_name }},/,/ci_flavor: jenkins }/ d' test/files/build_vars.yml.all.j2
    sed -i '/- { vrs_os_type: u16.04,/,/standby_controller_ip: {{ network_address }}.213 }/d' test/files/build_vars.yml.all.j2
fi
./metro-ansible ci_predeploy.yml -vvvv
./metro-ansible ci_deploy.yml -vvvv

cp ./test/files/build_vars.yml.all roles/reset-build/files/build_vars.yml
cp ./test/files/test_install.yml .
cp ./test/files/test_cleanup.yml .
sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml

ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible test_install.yml -vvvv
./metro-ansible test_cleanup.yml -vvvv

./metro-ansible ci_destroy.yml -vvvv
