#!/bin/bash

# exit on non-zero return code
set -e

#
# Start script for Nuage Metro container
#

function show_usage() {
 echo "Copyright (C) 2017 Nuage Networks, all rights reserved. Version 1.0 2017-06-14"
 echo "Usage: docker run -it --rm -v \`pwd\`:/files nuage/metro" 
 echo "  add 'health' to check, 'destroy' to remove everything"
 echo "  tip: You can add '--dns:x.x.x.x' to specify a DNS server for the Ansible host (this container) to use"
 echo "  You may have to 'ssh-copy-id -i id_rsa user@target_server' to the target servers"
 echo "  To deploy a subset of servers, you can add '--limit=vstats' ( or vsds, vscs, etc. ) at the end"
 echo "  Also, you may use --tags xxxx to only execute certain tasks"
 
 exit 0
}

function copy_upgrade_vars() {
  if [ ! -e /files/upgrade_vars.yml ]; then
     cp nuage-metro/upgrade_vars.yml /files
     sed -i 's|nuage_upgrade_unzipped_files_dir=.*|nuage_upgrade_unzipped_files_dir=/files/nuage-unpacked|g' /files/upgrade_vars.yml
     sed -i 's|user_ssh_pub_key=.*|user_ssh_pub_key=/files/id_rsa.pub|g' /files/upgrade_vars.yml
     sed -i 's|user_ssh_priv_key=.*|user_ssh_priv_key=/files/id_rsa|g' /files/upgrade_vars.yml
     echo "Please edit the sample 'upgrade_vars.yml' and try again"
     exit 1
  fi
  cp /files/upgrade_vars.yml /files/nuage-metro/
}

if [ $# == 0 ] || [ ! -d /files ]; then
 show_usage
fi

# Always copy Ansible scripts, such that users can customize if needed
cp -Rn nuage-metro /files

# Copy sample to root dir, if not existing
cp -n nuage-metro/build_vars.yml /files

# Generate new host key if needed
mkdir -p --mode=700 ~/.ssh 
if [ ! -e /files/id_rsa ]; then
  ssh-keygen -h -f /files/id_rsa -N ''
fi

# Always re-copy, even if already done
# ssh-copy-id -i /files/id_rsa.pub root@127.0.0.1 || exit 1
cp /files/id_rsa* ~/.ssh/ && chmod 600 ~/.ssh/id_rsa*

# Run Ansible playbooks
export ANSIBLE_HOST_KEY_CHECKING=False
export PARAMIKO_HOST_KEY_AUTO_ADD=True
cp /files/build_vars.yml /files/nuage-metro/

if [ "$1" == "health" ]; then
  shift
  cd /files/nuage-metro && \
  ansible-playbook --key-file=/files/id_rsa build.yml && \
  ansible-playbook -i hosts --key-file=/files/id_rsa nuage_health.yml $@
  exit $?
fi
if [ "$1" == "upgrade-vsd" ]; then
  shift
  copy_upgrade_vars 
  cd /files/nuage-metro
  ansible-playbook --key-file=/files/id_rsa build_upgrade.yml -v
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsp_preupgrade_health.yml $@
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsd_ha_upgrade_database_backup_and_decouple.yml $@
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsd_ha_upgrade_shutdown_1_and_2.yml $@
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsd_ha_upgrade_predeploy_1_and_2.yml $@
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsd_ha_upgrade_deploy_1_and_2.yml $@
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsd_ha_upgrade_shutdown_3.yml $@
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsd_ha_upgrade_predeploy_3.yml $@
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsd_ha_upgrade_deploy_3.yml $@
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsd_upgrade_complete_flag.yml $@
  exit $?
fi
if [ "$1" == "upgrade-vsc" ]; then
  shift
  copy_upgrade_vars
  cd /files/nuage-metro && \
  ansible-playbook --key-file=/files/id_rsa build_upgrade.yml && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsc_health.yml -e report_filename=vsc_preupgrade_health.txt $@ && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsc_ha_upgrade_backup_and_prep_1.yml $@ && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsc_ha_upgrade_deploy_1.yml $@ && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsc_ha_upgrade_postdeploy_1.yml $@ && \
  read -p 'Now upgrade *all* VRSs (--limit=vrss)... press any key to continue' -n1 -s && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsc_ha_upgrade_backup_and_prep_2.yml $@ && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsc_ha_upgrade_deploy_2.yml $@ && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsc_ha_upgrade_postdeploy_2.yml $@
  exit $?
fi
if [ "$1" == "upgrade-es" ]; then
  shift
  copy_upgrade_vars
  cd /files/nuage-metro && \
  ansible-playbook --key-file=/files/id_rsa build_upgrade.yml && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vstat_health.yml -e report_filename=vstat_preupgrade_health.txt $@ && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vstat_upgrade_data_backup.yml $@ && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vstat_destroy.yml $@ && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vstat_predeploy.yml $@ && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vstat_deploy.yml $@ && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vstat_upgrade_data_migrate.yml $@ && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsp_upgrade_postdeploy.yml $@ && \
  ansible-playbook -i hosts --key-file=/files/id_rsa playbooks/vsp_postupgrade_health.yml $@
  exit $?
fi
if [ "$1" == "destroy" ]; then
  shift
  cd /files/nuage-metro && \
  ansible-playbook --key-file=/files/id_rsa build.yml && \
  ansible-playbook -i hosts --key-file=/files/id_rsa destroy_everything.yml $@
  exit $?
fi

if [ ! -d /files/nuage-unpacked ] || [ "$1" == "unpack" ]; then
ansible-playbook /files/nuage-metro/nuage_unzip.yml $@
fi

cd /files/nuage-metro && \
ansible-playbook --key-file=/files/id_rsa build.yml && \
ansible-playbook -i hosts --key-file=/files/id_rsa install_everything.yml $@

exit $?
