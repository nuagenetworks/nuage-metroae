# Metro: Automated Upgrade of Nuage Software

## Current support for upgrade on KVM and vmWARE

1. Nuage Networks components supported
   1. VSD - HA and SA deployments
   1. VSC - HA and SA deployments
   1. VSTAT (ElasticSearch) - HA and SA deployments
   1. VCIN
Following ugrade path is tested with metro for HA and SA deployments
   1. 5.0.2 to 5.1.1
   1. For other supported upgrade paths, refer to official NuageNetworks Documentation 
   1. All upgrades should be tested in a lab environment before running at a customer site

## Pre-Requisites

Metro provides a set of playbooks and roles to automate the upgrade of significant parts of a Nuage Networks VSP installation. The upgrade process is composed of executing a series of modular playbooks with defined stopping points.

The playbook `build_upgrade.yml` relies on build_vars.yml, upgrade_vars.yml and user_creds.yml to automatically populate a number of Ansible variable files for the operation of the metro playbooks.

1. `build_upgrade.yml` requirements
Upgrading VSD and VSTAT nodes require following changes to `build_vars.yml` file.
- Users must define a value for `upgrade_vmname` for each VSD and VSTAT being upgraded. The values of `upgrade_vmname` must be different from the VM name currently being used by the VMs that are running. `upgrade_vmname` is required because the upgrade process will simply power down the old VMs, not delete them. We keep the old VMs around in case a rollback is required. For example:

```
myvsds:

- { hostname: nl-gv-pbl-a1-sdn-nvd01.sdn-acc.kpn.com,
    upgrade_vmname: nl-gv-plb-a1-sdn-upg01,
    target_server_type: "kvm",
    target_server: 10.242.103.55,
    mgmt_ip: 10.242.103.30,
    mgmt_gateway: 10.242.103.1,
    mgmt_netmask: 255.255.255.0 }
```
2. `upgrade_vars.yml` requirements
Upgrading VSTAT nodes require following changes to `upgrade_vars.yml` file.
- Users must define a value for `vstats_nfs_server_with_folder` that will be mounted on the VSTAT VM. It will be used as the backup and restore location for ES files during the upgrade and rollback. The value must be of the form `host_or_ip:/nfs/exported/folder`. For example:

```
vstat_nfs_server_with_folder: 135.227.181.233:/tmp/vstat/
```
The folder listed must be NFS exported by the server prior to running the upgrade.

3. `VSD and VSTAT path requirements` 
Upgrading VSD and VSTAT nodes require following changes when user decides not to run nuage_unzip.yml
- Users should define additional paths apart from the ones that were mentioned in nuage_unzip.yml section of BUILD.md file. Discussed below are these additional paths.

```
<yourpath>/vsd/migration/
```
As part of VSD upgrade, migration scripts are provided as seperate package (Nuage-VSD-migration-scripts-version-ISO.tar.gz) that perform database backup and decluster existing VSD cluster. This package should be placed inside the `migration` folder of vsd path as shown above.

```
<yourpath>/vstat/backup/
```
As part of VSTAT upgrade, backup scripts are provided as seperate package (Nuage-elastic-backup-version-.tar.gz) that perform backup of existing indices of ElasticSearch node. This package should be placed inside the `backup` folder of vstat path as shown above.

4. `VSC path requirements`
Upgrading VSC requires <.tim> file that needs to be present in VSC path <yourpath>/vsc/

Generate necessary data for the ansible playbooks to run by executing `build_upgrade` playbook. This requires `build_vars.yml`,  `upgrade_vars.yml`, and `user_creds.yml` to be populated according to the environment. The `user_creds.yml` file must contain VSD and VSC credentials as shown in the example file `examples\user_creds.yml` 

5. Run `./metro-ansible build_upgrade.yml -vvvv` to generate variables and files nedded for upgrade


## VSD, VSC, & VSTAT (elasticsearch ) HA/Cluster upgrade at a glance

A sample workflow for 5.0.2 to 5.1.1 upgrade. For more detailed workflow refer [Sample HA Metro workflow for an upgrade]

After all [Pre-Requisites] are met, run the following set of playbooks in the order specified to upgrade vsd,vsc,vstat deployed in HA/Cluster mode.
1. ./metro-ansible vsp_preupgrade_health.yml -vvvv
2. ./metro-ansible vsd_ha_upgrade_database_backup_and_decouple.yml -vvvv
3. ./metro-ansible vsd_ha_upgrade_shutdown_1_and_2.yml -vvvv
4. ./metro-ansible vsd_ha_upgrade_predeploy_1_and_2.yml -vvvv
5. ./metro-ansible vsd_ha_upgrade_deploy_1_and_2.yml -vvvv
6. ./metro-ansible vsd_ha_upgrade_shutdown_3.yml -vvvv
7. ./metro-ansible vsd_ha_upgrade_predeploy_3.yml -vvvv
8 ./metro-ansible vsd_ha_upgrade_deploy_3.yml -vvvv
9 ./metro-ansible vsd_upgrade_complete_flag.yml -vvv
10 ./metro-ansible vsc_health.yml -e report_filename=vsc_preupgrade_health.txt -vvvv
11 ./metro-ansible vsc_ha_upgrade_backup_and_prep_1.yml -vvvv
12 ./metro-ansible vsc_ha_upgrade_deploy_1.yml -vvvv
13 ./metro-ansible vsc_ha_upgrade_postdeploy_1.yml -vvvv

** DO NOT PROCEED UNTILL VRS(s) ARE UPGRADED **

14 ./metro-ansible vsc_ha_upgrade_backup_and_prep_2.yml -vvvv
15 ./metro-ansible vsc_ha_upgrade_deploy_2.yml -vvvv
16 ./metro-ansible vsc_ha_upgrade_postdeploy_2.yml -vvvv
17 ./metro-ansible vstat_health.yml -e report_filename=vstat_preupgrade_health.txt -vvvv
18 ./metro-ansible vstat_upgrade_data_backup.yml -vvvv
19 ./metro-ansible vstat_destroy.yml -vvvv
20 ./metro-ansible vstat_predeploy.yml -vvvv
21 ./metro-ansible vstat_deploy.yml -vvvv
22 ./metro-ansible vstat_upgrade_data_migrate.yml -vvvv

** FINALIZE UPGRADE **
23 ./metro-ansible vsp_upgrade_postdeploy.yml -vvvv
24 ./metro-ansible vsp_postupgrade_health.yml -vvvv
 

## VSD, VSC, & VSTAT (elasticsearch ) SA/Standalone upgrade at a glance

A sample workflow for 5.0.2 to 5.1.1 upgrade. For detailed workflow refer [Sample Metro workflow for standalone upgrade]

After all [Pre-Requisites] are met, run the following set of playbooks in the order specified to upgrade vsd,vsc,vstat deployed in SA/Standalone mode.
1 ./metro-ansible vsp_preupgrade_health.yml -vvvv
2 ./metro-ansible vsd_sa_upgrade_database_backup.yml -vvvv
3 ./metro-ansible vsd_sa_upgrade_shutdown.yml -vvvv
4 ./metro-ansible vsd_predeploy.yml -vvvv
5 ./metro-ansible vsd_sa_upgrade_deploy.yml -vvvv
6 ./metro-ansible vsd_upgrade_complete_flag.yml -vvvv
7 ./metro-ansible vsc_health.yml -e report_filename=vsc_preupgrade_health.txt -vvvv
8 ./metro-ansible vsc_sa_upgrade_backup_and_prep.yml -vvvv
9 ./metro-ansible vsc_sa_upgrade_deploy.yml -vvvv
10 ./metro-ansible vsc_sa_upgrade_postdeploy.yml -vvvv

** DO NOT PROCEED UNTILL VRS(s) ARE UPGRADED **

11 ./metro-ansible vstat_health.yml -e report_filename=vstat_preupgrade_health.txt -vvvv
12 ./metro-ansible vstat_upgrade_data_backup.yml -vvvv
13 ./metro-ansible vstat_destroy.yml -vvvv
14 ./metro-ansible vstat_predeploy.yml -vvvv
15 ./metro-ansible vstat_deploy.yml -vvvv
16 ./metro-ansible vstat_upgrade_data_migrate.yml -vvvv

** FINALIZE UPGRADE **
17 ./metro-ansible vsp_upgrade_postdeploy.yml -vvvv
18 ./metro-ansible vsp_postupgrade_health.yml -vvvv 


## Sample HA Metro workflow for an upgrade

For the purposes of this sample, an HA deployment is one that consists 3 VSD nodes in a cluster, two VSC nodes, a single VSTAT node, and a number of deployed VRS instances. Nuage-Metro supports upgrades to both HA and SA deployments as well as 3-node VSTAT clusters on KVM and VMware. This document will describe the specific procedure for the upgrade of an HA deployment defined above. Slight modifications to this procedure will enable Metro to support other possible upgrades, e.g. one VSD, one VSC, one VSTAT.

1. Generate necessary data for the ansible playbooks to run by executing `build_upgrade` playbook. This requires `build_vars.yml`,  `upgrade_vars.yml`, and `user_creds.yml` to be populated according to the environment. The `user_creds.yml` file must contain VSD and VSC credentials as shown in the example file `examples\user_creds.yml`. This example assumes the following:
  - vsd_sa_or_ha will be set to ha
  - There will be exactly 3 VSD definitions
  - The VSD definitions will be ordered such that the third VSD definition will be that of the VSD node to be decoupled during the upgrade. This VSD will be tagged as ‘vsd_node3’ and will be decoupled. The other two VSDs will be tagged as ‘vsd_node1’ and vsd_node2’, respectively. Make sure that you define the VSD node that you want to decouple last in the build_vars.yml file.
  - There will be exactly 2 VSC definitions.
  - The VSC definitions will be ordered such that the first VSC will be that of the first VSC node to be upgraded. The other VSC will be upgraded second. The first VSC will be tagged as ‘vsc_node1’. The second VSC will be tagged as ‘vsc_node2’.
  - There will be exactly 3 VSTAT definitions

Edit the files listed above, then run:

```
./metro-ansible build_upgrade.yml -vvvv
```

2. Run a pre-upgrade health checks on the platform

```
./metro-ansible vsp_preupgrade_health.yml -vvvv
```

The health reports and any reported error should carefully be checked before proceeding with the next steps.
These health checks can be run at any time of the upgrade process.

3. Database Backup and decouple the VSD cluster

```
./metro-ansible vsd_ha_upgrade_database_backup_and_decouple.yml -vvvv
```

At this point, vsd_node3 has been decoupled from the cluster and is running in SA mode. If you experience a failure in the previous step, recovery depends on the state of vsd_node3. If it’s still in the cluster, you can simply retry. If not, you will need to redeploy vsd_node3 from a backup(user is expected to have the vm backup ready before the upgrade procedure) or otherwise recover.

4. Power off vsd_node1 and vsd_node2

```
./metro-ansible vsd_ha_upgrade_shutdown_1_and_2.yml -vvvv
```

At this point, vsd_node1 and vsd_node2 are shut down, but not deleted. The new nodes will be brought up with new VM names. Note that this step may be done manually if the user chooses. If you experience a failure running the Metro playbook for this step, a retry is advised. Or you can power off the VMs manually.

5. Predeploy new vsd_node1 and vsd_node2

```
./metro-ansible vsd_ha_upgrade_predeploy_1_and_2.yml -vvvv
```

At this point, the new vsd_node1 and vsd_node2 are up and running, but they have not yet been configured. If you experience a failure in this step, execute the playbook vsd_ha_upgrade_destroy_1_and_2.yml to delete the new nodes. Then retry the step.

6. Deploy new vsd_node1 and vsd_node2

```
./metro-ansible vsd_ha_upgrade_deploy_1_and_2.yml -vvvv
```

At this point, two VSD nodes have been upgraded. You are ready to move on to the first VSC. If you experience a failure before the VSD install script runs, retry playbook vsd_ha_upgrade_deploy_1_and_2.yml. If that fails again or the failure comes after the VSD install script runs, destroy the VMs manually or use vsd_ha_upgrade_destroy_1_and_2.yml, then retry starting at step 5.

7. Run VSC health checks

```
./metro-ansible vsc_health.yml -e report_filename=vsc_preupgrade_health.txt -vvvv
```

This step is already done in step 2. You can skip it here if you wish. It is good practice to re-run at this point in order to inspect the report to make sure the VSD upgrade work has not caused problems.

8.  Run VSC backup and prep on vsc_node1

```
./metro-ansible vsc_ha_upgrade_backup_and_prep_1.yml -vvvv
```

If this fails, retry.

9. Run VSC deploy on vsc_node1

```
./metro-ansible vsc_ha_upgrade_deploy_1.yml -vvvv
```

If the step fails, you can retry. Backup plan is to manually copy a valid .tim file to the VSC to affect either the deployment (new version of tim file) or a rollback. (old version of tim file). If rollback fails, you will need to deploy a new VSC using the old version--or recover the VM from a backup. You can use Metro for the deployment (vsc_predeploy, vsc_deploy, vsc_postdeploy...).

10. Run VSC postdeploy on vsc_node1

```
./metro-ansible vsc_ha_upgrade_postdeploy_1.yml -vvvv
```

At this point, you have one VSC running the old version, one running the new. It is time for you to leave this procedure to execute an upgrade of your VRSs, NSGs, and so on.

If this step fails, the recovery is much like that of the previous step: Manually update the tim file or a complete deploy of the old VSC followed by a retry.

*Upgrade VRS here!*

11.  Run VSC backup and prep on vsc_node2

```
./metro-ansible vsc_ha_upgrade_backup_and_prep_2.yml -vvvv
```

If this fails, retry.

12. Run VSC deploy on vsc_node2

```
./metro-ansible vsc_ha_upgrade_deploy_2.yml -vvvv
```

If the step fails, you can retry. Backup plan is to manually copy a valid .tim file to the VSC to affect either the deployment (new version of tim file) or a rollback. (old version of tim file). If rollback fails, you will need to deploy a new VSC using the old version--or recover the VM from a backup. You can use Metro for the deployment (vsc_predeploy, vsc_deploy, vsc_postdeploy...).

13. Run VSC postdeploy on vsc_node2

```
./metro-ansible vsc_ha_upgrade_postdeploy_2.yml -vvvv
```

At this point, you have both VSCs running the new version. It is time for you to upgrade the final VSD.

If this step fails, the recovery is much like that of the previous step: Manually update the tim file or a complete deploy of the old VSC followed by a retry.

14. Power off vsd_node3

```
./metro-ansible vsd_ha_upgrade_shutdown_3.yml -vvvv
```

At this point, vsd_node2 is shut down, but not deleted. The new node will be brought up with a new VM name. Note that this step may be done manually if the user chooses. If you experience a failure running the Metro playbook for this step, a retry is advised. Or you can power off the VM manually.

15. Run predeploy on vsd_node3

```
./metro-ansible vsd_ha_upgrade_predeploy_3.yml -vvvv
```

At this point, the new vsd_node3 is up and running, but t has not yet been configured. If you experience a failure in this step, execute the playbook vsd_ha_upgrade_destroy_3.yml to delete the new node. Then retry the step.

16. Run deploy on vsd_node3

```
./metro-ansible vsd_ha_upgrade_deploy_3.yml -vvvv
```

At this point, all 3 VSD nodes have been upgraded. If you experience a failure before the VSD install script runs, retry playbook vsd_ha_upgrade_deploy_3.yml. If that fails again or the failure comes after the VSD install script runs, destroy the VMs manually or use vsd_ha_upgrade_destroy_3.yml, then retry starting at step 15.

*If VSTAT nodes exist upgrade them using following procedure, if not skip to step 23 to finalize VSP upgrade*

17. Run VSTAT health checks

```
./metro-ansible vstat_health.yml -e report_filename=vstat_preupgrade_health.txt -vvvv
```

This step is already done in step 2. You can skip it here if you wish. It is good practice to re-run at this point in orfder to inspect the report to make sure the VSD upgrade work has not caused problems.

18. Run vstat_upgrade_data_backup

```
./metro-ansible vstat_upgrade_data_backup.yml -vvvv
```

At this point the data from the vstat nodes is backed in the NFS shared folder. If you experience a failure in the previous step, you can simply retry.

19. Power off all vstats

```
./metro-ansible vstat_destroy.yml -vvvv
```

At this point, all vstat nodes are shut down, but not deleted. The new nodes will be brought up with new VM names. Note that this step may be done manually if the user chooses. If you experience a failure running the Metro playbook for this step, a retry is advised. Or you can power off the VMs manually.

20. Predeploy new vstat nodes

```
./metro-ansible vstat_predeploy.yml -vvvv
```

At this point, the new vstat nodes are up and running, but they have not yet been configured. If you experience a failure in this step, execute the playbook vstat_upgrade_destroy.yml to delete the new nodes. Then retry the step.

21. Deploy new vstat nodes

```
./metro-ansible vstat_deploy.yml -vvvv
```

At this point, new vstat nodes have been deployed and configured to talk with VSD(s). If you experience a failure, retry playbook vstat_deploy.yml. If that fails again, destroy the VMs manually or use vstat_upgrade_destroy.yml, then retry starting at step 20.

22. Run vstat_upgrade_data_migrate

```
./metro-ansible vstat_upgrade_data_migrate.yml -vvvv
```

At this point the data from the old vstat nodes is migrated to the new VSTAT nodes from the NFS shared folder. If you experience a failure in the previous step, you can simply retry.


23. Run VSP upgrade wrapup to finalize settings

```
./metro-ansible vsp_ha_upgrade_wrapup.yml -vvvv
```

This will execute the final steps of the upgrade. It can be rerun if there is a failure.

24. Run VSP post-upgrade heath

```
./metro-ansible vsp_postupgrade_health.yml -vvvv
```

Writes out new health reports that can be compared to those produced in step one. Any errors or discrepancies should be investigated carefully.


## Sample Metro workflow for standalone upgrade

For the purpose of this sample, a Standalone deployment is one that consists exactly one VSD node, one VSC node, a single VSTAT node, and a number of deployed VRS instances. Note that if you have 2 VSCs, after the VSD upgrade is complete, follow the VSC upgrade instructions from the HA procedure, above.

1. Generate necessary data for the ansible playbooks to run by executing `build_upgrade` playbook. This requires `build_vars.yml`,  `upgrade_vars.yml`, and `user_creds.yml` to be populated according to the environment. The `user_creds.yml` file must contain VSD and VSC credentials as shown in the example file `examples\user_creds.yml`. This example assumes the following:
  - vsd_sa_or_ha will be set to sa
  - There will be exactly 1 VSD definition
  - There will be exactly 1 VSC definition
  - There will be exactly 1 VSTAT definition

Edit the files listed above, then run:

```
./metro-ansible build_upgrade.yml -vvvv
```

2. Run health checks on VSD,VSC and VSTAT

```
./metro-ansible vsp_preupgrade_health.yml -vvvv
```
The health reports and any reported error should carefully be checked before proceeding with the next steps.

These health checks can be run at any time of the upgrade process.

3. Databse Backup of standalone VSD

```
./metro-ansible vsd_sa_upgrade_database_backup.yml -vvvv
```
At this point, vsd node database backup is completed. If you experience a failure in the previous step, you can simply retry.

4. Power off vsd

```
./metro-ansible vsd_sa_upgrade_shutdown.yml -vvvv
```

At this point, vsd is shut down, but not deleted. The new node will be brought up with new VM name. Note that this step may be done manually if the user chooses. If you experience a failure running the Metro playbook for this step, a retry is advised. Or you can power off the VM manually.

5. Predeploy new vsd node

```
./metro-ansible vsd_predeploy.yml -vvvv
```

At this point, the new vsd node is up and running, but it has not yet been configured. If you experience a failure in this step, execute the playbook vsd_sa_upgrade_destroy.yml to delete the new node. Then retry the step.

6. Deploy new vsd node

```
./metro-ansible vsd_sa_upgrade_deploy.yml -vvvv
```

At this point, VSD node is upgraded. You are ready to move on to the VSC node. If you experience a failure before the VSD install script runs, retry playbook vsd_sa_upgrade_deploy.yml. If that fails again or the failure comes after the VSD install script runs, destroy the VMs manually or use vsd_destroy.yml, then retry starting at step 5.

7. Run VSC health checks

```
./metro-ansible vsc_health.yml -e report_filename=vsc_preupgrade_health.txt -vvvv
```

This step is already done in step 2. You can skip it here if you wish. It is good practice to re-run at this point in order to inspect the report to make sure the VSD upgrade work has not caused problems.

8.  Run VSC backup and prep on vsc

```
./metro-ansible vsc_sa_upgrade_backup_and_prep.yml -vvvv
```

9. Run VSC deploy on vsc

```
./metro-ansible vsc_sa_upgrade_deploy.yml -vvvv
```

If the step fails, you can retry. Backup plan is to manually copy a valid .tim file to the VSC to affect either the deployment (new version of tim file) or a rollback. (old version of tim file). If rollback fails, you will need to deploy a new VSC using the old version--or recover the VM from a backup. You can use Metro for the deployment (vsc_predeploy, vsc_deploy, vsc_postdeploy...).

10. Run VSC postdeploy on vsc

```
./metro-ansible vsc_sa_upgrade_postdeploy.yml -vvvv
```

At this point, you have VSC upgrade is complete.

If this step fails, the recovery is much like that of the previous step: Manually update the tim file or a complete deploy of the old VSC followed by a retry.

*Upgrade VRS here!*

*If VSTAT node exist upgrade it using steps 17-22 in HA upgrade workflow mentioned in above section, if not skip to step 11 to finalize VSP upgrade*

11. Run VSP upgrade wrapup to finalize settings

```
./metro-ansible vsp_sa_upgrade_wrapup.yml -vvvv
```

This will execute the final steps of the upgrade. It can be rerun if there is a failure.

12. Run VSP post-upgrade heath

```
./metro-ansible vsp_postupgrade_health.yml -vvvv
```

Writes out new health reports that can be compared to those produced in step one. Any errors or discrepancies should be investigated carefully.
