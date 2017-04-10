# Metro: Automated Upgrade of Nuage Software

## Current support for upgrade

1. As of this writing only VSD and VSC upgrade are supported
2. Supported upgrade paths
   1. 3.2.R10 to 4.0.R7
   1. 4.0.R4 to 4.0.R7
   1. Other upgrades should be tried in a test environment before production
3. Only clustered VSD upgrade is supported   

## Overview

These are the following playbooks/roles supported by metro for upgrade.

1. vsd_health.yml
2. vsd_decluster.yml
3. vsd_upgrade.yml
4. vsc_health.yml
5. vsc_backup.yml
6. vsc_upgrade.yml
7. vsp_upgrade.yml

The recommended workflow for an upgrade is to 
1. generate necessary data for the ansible playbooks to run by executing build_upgrade playbook. This require both build_vars.yml and upgrade_vars.yml to be populated according to the environment.
2. run vsp_upgrade playbook for an end to end upgrade that covers clustered VSDs and dual VSCs.
3. Individual upgrades for VSDs and VSc are possible with some tweaking of ansible inventory hosts.
4. VSD and VSC health checks can be run anytime irrespective of upgrade process

## Details

### vsd_health.yml

This playbook/role is used to gather network and monit information of vsd(s) prior/post upgrade process. A report file with network and monit information is created (filename can be configured inside the vsd_health.yml playbook) inside reports folder. 

### vsd_decluster.yml

This playbook is a collection three individual playbooks/roles that help in making database backup, decoupling existing vsd cluster setup and gracefully stopping vsd processes. The user is expected to mount the migration scritps in respective vsd(s).

a. vsd_dbbackup.yml: This playbook/role makes vsd database backup and stores it on ansible deployment host, which is later used for spinning up new vsd(s)
b. vsd_decouple.yml: This playbook/role executes decouple script and checks for client connections
c. vsd_services_stop.yml: This playbook/role stops all vsd services on vsd(s) gracefully

### vsd_upgrade.yml

This playbook/role destroys the exsitng vsd vm(s) and boots a new vsd vm(s) with backup database. It is recommended for user to take snapshot of the old vsd vm(s) before the upgrade as they are destroyed. Current VSD upgrade supports only clustered setup.

The playbook can be configured with interested vsd(s).
e.g. 
If user is interested in upgrading vsd node1, hosts can be defined as below
- hosts: vsd_ha_node1
If user is interested in upgrading vsd node1 and node3, hosts can be defined as below
- hosts: vsd_ha_node1:vsd_ha_node3
To upgrade all vsd nodes
- hosts: vsds

### vsc_health.yml

This  playbook/role is used to gather operational information of vsc(s) prior/post upgrade process. A report file with the operational output is created (filename can be configured inside the vsc_health.yml playbook) inside reports folder.

VSC health can check the health of a VSC against preconfigured expected values such as number of bgp peers and expected number of vswitches which is the number of VRSs under the VSC control.If run outside of the upgrade playbooks, VSC health checks can be invoked with the following manner.

ansible-playbook vsc_health.yml -i hosts -e "expected_num_bgp_peers=1 expected_num_vswitches=2"

### vsc_backup.yml

This playbook/role is used to make backup of exsiting vsc configuration, bof configuration and .tim file and copy them to ansible deployment host. These are used in case a rollback is needed.

### vsc_upgrade.yml

This playbook/role is used to upgrade vsc to new versions by copying new .tim file to the existing vsc(s) and rebooting them.

The playbook can be configured with interested vsc(s)
e.g. 
If user is interested in upgrading vsc node1, hosts can be defined as below
- hosts: vsc_ha_node1
If user is interested in upgrading vsc node1 and node2, hosts can be defined as below
- hosts: vsc_ha_node1:vsc_ha_node2
To upgrade all vsc nodes
- hosts: vscs

### vsp_upgrade.yml

All the above playbooks are captured inside a single playbook `vsp_upgrade.yml`. This playbook follows the instructions and the order of upgrading nuage components as specified in VCS install guide.

## build and reset-build playbooks

The build_upgrade playbook (`build_upgrade.yml`) is used to automatically populate a number of Ansible variable files for the operation of the metro playbooks. Running `./metro-ansible build_upgrade.yml` will use the variables defined in `build_vars.yml` and `upgrade_vars.yml` to create a `hosts` file, populate a `host_vars` directory, populate a `group_vars` directory, and make a few additional variable changes as required. The `build_upgrade.yml` playbook will do all the work for you.

Refer `BUILD.md` reset-build playbooks section for more details
