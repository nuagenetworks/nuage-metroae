# Metro: Automated Upgrade of Nuage Software

## Current support for upgrade

1. As of this writing only VSD and VSC upgrades are supported
2. Supported upgrade paths
   1. 3.2.R10 to 4.0.R7
   2. 4.0.R4 to 4.0.R7
   3. Other upgrades should be tried in a test environment before production
3. Standalone and clustered VSD upgrade is supported   

## Overview

These are the playbooks/roles supported by metro for upgrade covering different VCS components.

1. vsd_health.yml
2. vsd_sa_upgrade.yml
3. vsd_ha_node1_3_upgrade.yml
4. vsd_ha_node2_upgrade.yml
5. vsc_health.yml
6. vsc_ha_node1_upgrade.yml
7. vsc_ha_node2_upgrade.yml

### Metro workflow for an upgrade
Following steps are recommended to be executed for an upgrade using metro playbooks

1. Generate necessary data for the ansible playbooks to run by executing build_upgrade playbook. This requires both build_vars.yml and upgrade_vars.yml to be populated according to the environment.

```
./metro-ansible build.yml -vvvv

./metro-ansible build_upgrade.yml -vvvv
```

2. ### e.g. workflow for clustered vsp upgrade

The following is the workflow to acheive clustered vsp upgrade using above set of playbooks

```
./metro-ansible vsd_ha_node1_3_upgrade.yml
./metro-ansible vsc_ha_node1_upgrade.yml
Upgrade vrs(s) manually
./metro-ansible vsc_ha_node2.yml
./metro-ansible vsd_ha_node2_upgrade.yml
```

3. ### e.g. workflow for standalone vsp upgrade

The following is the workflow to acheive standalone vsp upgrade using above set of playbooks

```
./metro-ansible vsd_sa_upgrade.yml
./metro-ansible vsc_ha_node1_upgrade.yml
Upgrade vrs(s) manually
./metro-ansible vsc_ha_node2.yml
```

4. Individual upgrades for VSDs and VSCs are possible
5. VSD and VSC health checks can be run anytime irrespective of upgrade process

## Details

### vsd_health.yml

This playbook/role is used to gather network and monit information of vsd(s) prior/post upgrade process. A report file with network and monit information is created (filename can be configured inside the vsd_health.yml playbook) inside reports folder. 

### vsd_decluster.yml

This playbook is a collection three individual playbooks/roles that help in making database backup, decoupling existing vsd cluster setup and gracefully stopping vsd processes.

a. vsd_dbbackup.yml: This playbook/role makes vsd database backup and stores it on ansible deployment host, which is later used for spinning up new vsd(s)
b. vsd_decouple.yml: This playbook/role executes decouple script and checks for client connections
c. vsd_services_stop.yml: This playbook/role stops all vsd services on vsd(s) gracefully

### vsd_sa_upgrade.yml

This playbook/role helps to execute standalone upgrade for VSD. It is recommended for user to take snapshot of the old vsd vm(s) before the upgrade as they are destroyed.

### vsd_ha_node1_3_upgrade.yml and vsd_ha_node2_upgrade.yml

These playbooks together help to execute cluster upgrade for VSD. It is recommended for user to take snapshot of the old vsd vm(s) before the upgrade as they are destroyed.
The playbook can be configured with interested vsd(s).`

### vsc_health.yml

This playbook/role is used to gather operational information of vsc(s) prior/post upgrade process. A report file with the operational output is created (filename can be configured inside the vsc_health.yml playbook) inside reports folder.

VSC health can check the health of a VSC against preconfigured expected values such as number of bgp peers and expected number of vswitches which is the number of VRSs under the VSC control.If run outside of the upgrade playbooks, VSC health checks can be invoked with the following manner.

```
ansible-playbook vsc_health.yml -i hosts -e "expected_num_bgp_peers=1 expected_num_vswitches=2"
```

### vsc_backup.yml

This playbook/role is used to make backup of exsiting vsc configuration, bof configuration and .tim file and copy them to ansible deployment host. These are used in case a rollback is needed.

### vsc_node1_upgrade.yml and vsc_node2_upgrade.yml

These playbooks are used to upgrade vsc(s) to new versions by copying new .tim file to the existing vsc(s) and rebooting them.


## build and reset-build playbooks

The build_upgrade playbook (`build_upgrade.yml`) is used to automatically populate a number of Ansible variable files for the operation of the metro playbooks. Running `./metro-ansible build_upgrade.yml` will use the variables defined in `build_vars.yml` and `upgrade_vars.yml` to create a `hosts` file, populate a `host_vars` directory, populate a `group_vars` directory, and make a few additional variable changes as required. The `build_upgrade.yml` playbook will do all the work for you.

Refer `BUILD.md` reset-build playbooks section for more details
