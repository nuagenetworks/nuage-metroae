# Metro: Automated Upgrade of Nuage Software

## Current support for upgrade

1. As of this writing only VSD and VSC upgrades are supported
1. Supported upgrade paths
   1. 3.2.R8 to 4.0.Rn
   1. 3.2.R10 to 4.0.Rn
   1. 4.0.Rn to 4.0.Rn+
   1. Other upgrades should be tried in a test environment before production
1. Standalone and clustered VSD upgrade are supported

## Overview

Metro provides a set of playbooks and roles to automate the upgrade of a full Nuage VSP installation. They are basically implementing the sequence as described in the VSP Insallation Guide. While the overall upgrade can be execued by a single instruction, the different playbooks allow for a modular or staged execution to allow for manual checks in the middle.

### Metro workflow for an upgrade
Following steps are recommended to be executed for an upgrade using metro playbooks

1. Generate necessary data for the ansible playbooks to run by executing `build_upgrade` playbook. This requires `build_vars.yml`,  `upgrade_vars.yml`, and `user_creds.yml` to be populated according to the environment. It must contain VSD and VSC credentials as shown in the example file `examples\user_creds.yml` .

```
./metro-ansible build_upgrade.yml
```

2. Run health checks on VSD and VSC
```
./metro-ansible vsd_health.yml
./metro-ansible vsc_health.yml
```
Any reported error should carefully be checed before proceeding with the next steps.

These health checks can be ran at any time of the upgrade process.

3. Workflow for VSP upgrade with clustered VSD

The following is the workflow to acheive clustered vsp upgrade using above set of playbooks

```
./metro-ansible vsd_ha_node1_3_upgrade.yml
./metro-ansible vsc_ha_node1_upgrade.yml
```
Upgrade vrs(s) manually

```
./metro-ansible vsc_ha_node2_upgrade.yml
./metro-ansible vsd_ha_node2_upgrade.yml
```

4. Workflow for VSP upgrade with standalone VSD

The following is the workflow to upgrade a full Nuage Networks VSP installation with standalone VSD 

```
./metro-ansible vsd_sa_upgrade.yml
./metro-ansible vsc_ha_node1_upgrade.yml
```
Upgrade vrs(s) manually
```
./metro-ansible vsc_ha_node2_upgrade.yml
```

5. Run health checks on VSD and VSC post upgrade
```
./metro-ansible vsd_health.yml
./metro-ansible vsc_health.yml
```

## Details

### Checking health of VSD (`vsd_health.yml`)

This playbook/role is used to gather network and monit information of vsd(s) prior/post upgrade process. A report file with network and monit information is created (filename can be configured inside the `vsd_health.yml` playbook) inside `reports` folder. 

### Backup and decouple VSD node from cluster (`vsd_decluster.yml`)

This playbook is a collection three individual playbooks/roles that help in making database backup, decoupling existing vsd cluster setup and gracefully stopping vsd processes.

a. `vsd_dbbackup.yml`: This playbook/role makes vsd database backup and stores it on ansible deployment host, which is later used for spinning up new vsd(s)
b. `vsd_decouple.yml`: This playbook/role executes decouple script and checks for client connections
c. `vsd_services_stop.yml`: This playbook/role stops all vsd services on vsd(s) gracefully

### Upgrading standalone VSD (`vsd_sa_upgrade.yml`)

This playbook/role helps to execute standalone upgrade for VSD. It is recommended for user to take snapshot of the old vsd vm(s) before the upgrade as they are destroyed.

### Upgrade majority of VSD cluster (`vsd_ha_node1_3_upgrade.yml` and `vsd_ha_node2_upgrade.yml`)

These playbooks together help to execute cluster upgrade for VSD. It is recommended for user to take snapshot of the old vsd vm(s) before the upgrade as they are destroyed.
The playbook can be configured with interested vsd(s).

### Checking health of VSC (`vsc_health.yml`)

This playbook/role is used to gather operational information of vsc(s) prior/post upgrade process. A report file with the operational output is created (filename can be configured inside the `vsc_health.yml` playbook) inside reports folder.

VSC health can check the health of a VSC against preconfigured expected values such as number of bgp peers and expected number of vswitches which is the number of VRSs under the VSC control.If run outside of the upgrade playbooks, VSC health checks can be invoked with the following manner.

```
./metro-ansible vsc_health.yml -i hosts -e "expected_num_bgp_peers=1 expected_num_vswitches=2"
```

### Backup of VSC (`vsc_backup.yml`)

This playbook/role is used to make backup of exsiting vsc configuration, bof configuration and .tim file and copy them to ansible deployment host. These are used in case a rollback is needed.

### Upgrade of VSC (`vsc_node1_upgrade.yml` and `vsc_node2_upgrade.yml`)

These playbooks are used to upgrade vsc(s) to new versions by copying new .tim file to the existing vsc(s) and rebooting them.


## `build` and `reset-build` playbooks

The build_upgrade playbook (`build_upgrade.yml`) is used to automatically populate a number of Ansible variable files for the operation of the metro playbooks. Running `./metro-ansible build_upgrade.yml` will use the variables defined in `build_vars.yml` and `upgrade_vars.yml` to create a `hosts` file, populate a `host_vars` directory, populate a `group_vars` directory, and make a few additional variable changes as required. The `build_upgrade.yml` playbook will do all the work for you.

Refer `BUILD.md` reset-build playbooks section for more details
