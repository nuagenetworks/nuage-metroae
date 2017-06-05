#!/bin/bash
set -e
USAGE="Usage: $0 version deployment mode (sa or ha)"

if [ $# -ne 2 ];
then
    echo "Requires exactly 2 arguments: version and deployment mode (sa or ha)"
    echo $USAGE
    exit 1
fi

if [ $2 == ha ]
then
    sed -i 's/ci_flavor: jenkins/ci_flavor: jenkins-ha/g' test/files/build_vars.yml.CI.j2
fi

if [ $1 = 4.0.R4 ] || [ $1 = 3.2.R10 ];
then
    sed -i  '/- { hostname: {{ vrs_u16_host_name }},/,/ci_flavor: m1.medium }/d' test/files/build_vars.yml.CI.j2
fi

IPADDR=`/usr/sbin/ifconfig | grep netmask | grep broadcast | head -n 1 | awk '{print $2}'`

# update deployment mode in ci-deploy
sed -i "s/deployment_mode: sa/deployment_mode: $2/g" roles/ci-deploy/vars/main.yml
# Cut down rest build wait time from 30 sec to 1 sec
sed -i "s/eset_build_pause_secs: 30/eset_build_pause_secs: 1/g" roles/reset-build/vars/main.yml
# use heat to deploy the test VMs on OS
cp ./test/files/setup.yml.CI setup.yml
ansible-playbook setup.yml -vvvv
ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv

if [ $1 = 4.0.R4 ] || [ $1 = 3.2.R10 ];
then
    sed -i  '/- { hostname: {{ vrs_u16_target_server_name }},/,/ci_flavor: jenkins }/ d' test/files/build_vars.yml.all.j2
    sed -i '/- { vrs_os_type: u16.04,/,/standby_controller_ip: {{ network_address }}.213 }/d' test/files/build_vars.yml.all.j2
fi

./metro-ansible ci_predeploy.yml -vvvv
./metro-ansible ci_deploy.yml -vvvv

# setup and run the test itself
cp ./test/files/test_install.yml .
cp ./test/files/test_cleanup.yml .
# ci-deploy has updated the build_vars file for us. Now copy it and go...
cp ./test/files/build_vars_all.yml roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml

ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible test_install.yml -vvvv
./metro-ansible test_cleanup.yml -vvvv

./metro-ansible ci_destroy.yml -vvvv
