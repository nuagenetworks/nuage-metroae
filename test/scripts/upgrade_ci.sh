#!/bin/bash
set -e
USAGE="Usage: $0 version deployment mode (sa or ha)"

if [ $# -ne 4 ];
then
    echo "Requires exactly 4 arguments: upgrade_from_version, deployment mode (sa or ha), test_vmname (True or False) and upgrade_to_version"
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
# update vmname_test var
sed -i "s/vmname_test: False/vmname_test: $3/g" roles/ci-deploy/vars/main.yml
# Cut down reset build wait time from 30 sec to 1 sec
sed -i "s/reset_build_pause_secs: 30/reset_build_pause_secs: 1/g" roles/reset-build/vars/main.yml
# use heat to deploy the test VMs on OS
cp ./test/files/setup.yml.CI setup.yml
ansible-playbook setup.yml -vvvv
ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv

if [ $1 = 4.0.R4 ] || [ $1 = 3.2.R10 ];
then
    sed -i  '/- { hostname: {{ vrs_u16_target_server_name }},/,/ci_flavor: jenkins }/ d' test/files/build_vars.yml.all.j2
    sed -i '/- { vrs_os_type: u16.04,/,/standby_controller_ip: {{ network_address }}.215 }/d' test/files/build_vars.yml.all.j2
fi

./metro-ansible ci_predeploy.yml -vvvv
./metro-ansible ci_deploy.yml -vvvv

# setup and run the test itself
cp ./test/files/test_install.yml .
cp ./test/files/test_cleanup.yml .
# ci-deploy has updated the build_vars file for us. Now copy it and go...
cp ./test/files/build_vars_upgrade_all.yml roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml

#sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml
#sed -i "s/SERVER_TYPE/kvm/g" roles/reset-build/files/build_vars.yml

ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible test_install.yml -vvvv

# VCS deployment is finished. Now prepare the setup for upgrade
cp ./test/files/upgrade_vars.yml.all roles/reset-build/files/upgrade_vars.yml
cp ./test/files/user_creds_all.yml .
sed -i "s/install/upgrade/g" roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$4/g" roles/reset-build/files/upgrade_vars.yml
sed -i "s/UPGRADE_MAJOR_MINOR/major/g" roles/reset-build/files/upgrade_vars.yml
sed -i "s/UPGRADE_FROM/$1/g" roles/reset-build/files/upgrade_vars.yml
ansible-playbook reset_build.yml -vvvv

./metro-ansible build_upgrade.yml -vvv

# Upgrade workflow for SA deployments
if [$2 == sa]
then
    # Run health checks
    ./metro-ansible vsp_preupgrade_health.yml -vvv
    ./metro-ansible vstat_preupgrade_health.yml -vvv
    # Upgrade VSD
    ./metro-ansible vsd_sa_upgrade_database_backup.yml -vvv
    ./metro-ansible vsd_sa_upgrade_shutdown.yml -vvv
    ./metro-ansible vsd_predeploy.yml -vvv
    ./metro-ansible vsd_sa_upgrade_deploy.yml -vvv
    # Run vsc health checks
    ./metro-ansible vsc_sa_preupgrade_health.yml -vvv
    # Upgrade VSC
    ./metro-ansible vsc_sa_upgrade_backup_and_prep.yml -vvv
    ./metro-ansible vsc_sa_upgrade_deploy.yml -vvv
    # Run vstat health checks
    ./metro-ansible vstat_preupgrade_health.yml -vvv
    # Upgrade vstat
    ./metro-ansible vstat_upgrade_data_backup.yml -vvv
    ./metro-ansible vstat_destroy.yml -vvv
    ./metro-ansible vstat_predeploy.yml -vvv
    ./metro-ansible vstat_deploy.yml -vvv
    ./metro-ansible vstat_upgrade_data_migrate.yml -vvv
    # Finalize Upgrade
    ./metro-ansible vsp_ha_upgrade_wrapup.yml -vvv
    # Perfomr post upgrade health checks
    ./metro-ansible vsp_postupgrade_health.yml -vvv
fi

./metro-ansible test_cleanup.yml -vvvv

./metro-ansible ci_destroy.yml -vvvv
