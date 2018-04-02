# Upgrading Nuage Networks Components with MetroAG
## Prerequisites / Requirements
Before upgrading any components, you must have previously [set up your Nuage MetroAG Ansible environment](SETUP.md) and [customized the upgrade environment for your target platform](BUILD_UPGRADE.md).

## Use of MetroAG Tool
MetroAG can perform a workflow using the command-line tool as follows:

    ./metroag <workflow> [deployment] [options]

* `workflow`: Name of the workflow to perform.  Supported workflows can be listed with --list option.
* `deployment`: Name of the deployment directory containing configuration files.  See [customization](Documentation/CUSTOMIZATION.md)
* `options`: Other options for the tool.  These can be shown using --help.  Also, any options not directed to the metroag tool are passed to Ansible.

The following are some examples:

    ./metroag install_everything

Installs all components described in deployments/default/.

    ./metroag vsd_destroy east_network -vvv

Takes down only the VSD components described by deployments/east_network/vsds.yml.  Additional output will be displayed with 3 levels of verbosity.

## VSD, VSC, & VSTAT (elasticsearch) HA/Cluster upgrade at a glance

A sample workflow for 5.0.2 to 5.1.1 upgrade. For more detailed workflow refer [Sample HA Metro workflow for an upgrade](#sample-ha-metro-workflow-for-an-upgrade)

After all [Prerequisites](#prerequisites) are met, run the following set of playbooks in the order specified to upgrade vsd,vsc,vstat deployed in HA/Cluster mode.
1. ./metroag vsp_preupgrade_health -vvvv
2. ./metroag vsd_ha_upgrade_database_backup_and_decouple -vvvv
3. ./metroag vsd_ha_upgrade_shutdown_1_and_2 -vvvv
4. ./metroag vsd_ha_upgrade_predeploy_1_and_2 -vvvv
5. ./metroag vsd_ha_upgrade_deploy_1_and_2 -vvvv
6. ./metroag vsd_ha_upgrade_shutdown_3 -vvvv
7. ./metroag vsd_ha_upgrade_predeploy_3 -vvvv
8. ./metroag vsd_ha_upgrade_deploy_3 -vvvv
9. ./metroag vsd_upgrade_complete_flag -vvv
10. ./metroag vsc_health -e report_filename=vsc_preupgrade_health.txt -vvvv
11. ./metroag vsc_ha_upgrade_backup_and_prep_1 -vvvv
12. ./metroag vsc_ha_upgrade_deploy_1 -vvvv
13. ./metroag vsc_ha_upgrade_postdeploy_1 -vvvv

** DO NOT PROCEED UNTILL VRS(s) ARE UPGRADED **

14. ./metroag vsc_ha_upgrade_backup_and_prep_2 -vvvv
15. ./metroag vsc_ha_upgrade_deploy_2 -vvvv
16. ./metroag vsc_ha_upgrade_postdeploy_2 -vvvv
17. ./metroag vstat_health -e report_filename=vstat_preupgrade_health.txt -vvvv
18. ./metroag vstat_upgrade_data_backup -vvvv
19. ./metroag vstat_destroy -vvvv
20. ./metroag vstat_predeploy -vvvv
21. ./metroag vstat_deploy -vvvv
22. ./metroag vstat_upgrade_data_migrate -vvvv

** FINALIZE UPGRADE **

23. ./metroag vsp_upgrade_postdeploy -vvvv
24. ./metroag vsp_postupgrade_health -vvvv


## VSD, VSC, & VSTAT (elasticsearch ) SA/Standalone upgrade at a glance

A sample workflow for 5.0.2 to 5.1.1 upgrade. For detailed workflow refer [Sample Metro workflow for standalone upgrade](#sample-metro-workflow-for-standalone-upgrade)

After all [Prerequisites](#prerequisites) are met, run the following set of playbooks in the order specified to upgrade vsd,vsc,vstat deployed in SA/Standalone mode.
1. ./metroag vsp_preupgrade_health -vvvv
2. ./metroag vsd_sa_upgrade_database_backup -vvvv
3. ./metroag vsd_sa_upgrade_shutdown -vvvv
4. ./metroag vsd_predeploy -vvvv
5. ./metroag vsd_sa_upgrade_deploy -vvvv
6. ./metroag vsd_upgrade_complete_flag -vvvv
7. ./metroag vsc_health -e report_filename=vsc_preupgrade_health.txt -vvvv
8. ./metroag vsc_sa_upgrade_backup_and_prep -vvvv
9. ./metroag vsc_sa_upgrade_deploy -vvvv
10. ./metroag vsc_sa_upgrade_postdeploy -vvvv

** DO NOT PROCEED UNTILL VRS(s) ARE UPGRADED **

11. ./metroag vstat_health -e report_filename=vstat_preupgrade_health.txt -vvvv
12. ./metroag vstat_upgrade_data_backup -vvvv
13. ./metroag vstat_destroy -vvvv
14. ./metroag vstat_predeploy -vvvv
15. ./metroag vstat_deploy -vvvv
16. ./metroag vstat_upgrade_data_migrate -vvvv

** FINALIZE UPGRADE **

17 ./metroag vsp_upgrade_postdeploy -vvvv
18 ./metroag vsp_postupgrade_health -vvvv


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
./metroag build_upgrade -vvvv
```

2. Run a pre-upgrade health checks on the platform

```
./metroag vsp_preupgrade_health -vvvv
```

The health reports and any reported error should carefully be checked before proceeding with the next steps.
These health checks can be run at any time of the upgrade process.

3. Database Backup and decouple the VSD cluster

```
./metroag vsd_ha_upgrade_database_backup_and_decouple -vvvv
```

At this point, vsd_node3 has been decoupled from the cluster and is running in SA mode. If you experience a failure in the previous step, recovery depends on the state of vsd_node3. If it’s still in the cluster, you can simply retry. If not, you will need to redeploy vsd_node3 from a backup(user is expected to have the vm backup ready before the upgrade procedure) or otherwise recover.

4. Power off vsd_node1 and vsd_node2

```
./metroag vsd_ha_upgrade_shutdown_1_and_2 -vvvv
```

At this point, vsd_node1 and vsd_node2 are shut down, but not deleted. The new nodes will be brought up with new VM names. Note that this step may be done manually if the user chooses. If you experience a failure running the Metro playbook for this step, a retry is advised. Or you can power off the VMs manually.

5. Predeploy new vsd_node1 and vsd_node2

```
./metroag vsd_ha_upgrade_predeploy_1_and_2 -vvvv
```

At this point, the new vsd_node1 and vsd_node2 are up and running, but they have not yet been configured. If you experience a failure in this step, execute the playbook vsd_ha_upgrade_destroy_1_and_2.yml to delete the new nodes. Then retry the step.

6. Deploy new vsd_node1 and vsd_node2

```
./metroag vsd_ha_upgrade_deploy_1_and_2 -vvvv
```

At this point, two VSD nodes have been upgraded. If you experience a failure before the VSD install script runs, retry playbook vsd_ha_upgrade_deploy_1_and_2.yml. If that fails again or the failure comes after the VSD install script runs, destroy the VMs manually or use vsd_ha_upgrade_destroy_1_and_2.yml, then retry starting at step 5.

7. Power off vsd_node3

```
./metroag vsd_ha_upgrade_shutdown_3 -vvvv
```

At this point, vsd_node3 is shut down, but not deleted. The new node will be brought up with a new VM name. Note that this step may be done manually if the user chooses. If you experience a failure running the Metro playbook for this step, a retry is advised. Or you can power off the VM manually.

8. Run predeploy on vsd_node3

```
./metroag vsd_ha_upgrade_predeploy_3 -vvvv
```

At this point, the new vsd_node3 is up and running, but it has not yet been configured. If you experience a failure in this step, execute the playbook vsd_ha_upgrade_destroy_3.yml to delete the new node. Then retry the step.

9. Run deploy on vsd_node3

```
./metroag vsd_ha_upgrade_deploy_3 -vvvv
```

At this point, all 3 VSD nodes have been upgraded. If you experience a failure before the VSD install script runs, retry playbook vsd_ha_upgrade_deploy_3.yml. If that fails again or the failure comes after the VSD install script runs, destroy the VMs manually or use vsd_ha_upgrade_destroy_3.yml, then retry starting at step 8.

10. Set the VSD upgrade complete flag

```
./metroag vsd_upgrade_complete_flag -vvvv
```

After all the VSDs are upgraded, this step sets the upgrade flag to complete. It can be re-run in case of failure. It would be good time to login to VSD and verify the new version.

11. Run VSC health checks

```
./metroag vsc_health -e report_filename=vsc_preupgrade_health.txt -vvvv
```

This step is already done in step 2. You can skip it here if you wish. It is good practice to re-run at this point in order to inspect the report to make sure the VSD upgrade work has not caused problems.

12.  Run VSC backup and prep on vsc_node1

```
./metroag vsc_ha_upgrade_backup_and_prep_1 -vvvv
```

If this fails, retry.

13. Run VSC deploy on vsc_node1

```
./metroag vsc_ha_upgrade_deploy_1 -vvvv
```

If the step fails, you can retry. Backup plan is to manually copy a valid .tim file to the VSC to affect either the deployment (new version of tim file) or a rollback. (old version of tim file). If rollback fails, you will need to deploy a new VSC using the old version--or recover the VM from a backup. You can use Metro for the deployment (vsc_predeploy, vsc_deploy, vsc_postdeploy...).

14. Run VSC postdeploy on vsc_node1

```
./metroag vsc_ha_upgrade_postdeploy_1 -vvvv
```

At this point, you have one VSC running the old version, one running the new. It is time for you to leave this procedure to execute an upgrade of your VRSs, NSGs, and so on.

If this step fails, the recovery is much like that of the previous step: Manually update the tim file or a complete deploy of the old VSC followed by a retry.

*Upgrade VRS here!*

14.  Run VSC backup and prep on vsc_node2

```
./metroag vsc_ha_upgrade_backup_and_prep_2 -vvvv
```

If this fails, retry.

15. Run VSC deploy on vsc_node2

```
./metroag vsc_ha_upgrade_deploy_2 -vvvv
```

If the step fails, you can retry. Backup plan is to manually copy a valid .tim file to the VSC to affect either the deployment (new version of tim file) or a rollback. (old version of tim file). If rollback fails, you will need to deploy a new VSC using the old version--or recover the VM from a backup. You can use Metro for the deployment (vsc_predeploy, vsc_deploy, vsc_postdeploy...).

16. Run VSC postdeploy on vsc_node2

```
./metroag vsc_ha_upgrade_postdeploy_2 -vvvv
```

At this point, you have both VSCs running the new version. It is time for you to upgrade the final VSD.

If this step fails, the recovery is much like that of the previous step: Manually update the tim file or a complete deploy of the old VSC followed by a retry.


*If VSTAT nodes exist upgrade them using following procedure, if not skip to step 23 to finalize VSP upgrade*

17. Run VSTAT health checks

```
./metroag vstat_health -e report_filename=vstat_preupgrade_health.txt -vvvv
```

This step is already done in step 2. You can skip it here if you wish. It is good practice to re-run at this point in orfder to inspect the report to make sure the VSD upgrade work has not caused problems.

18. Run vstat_upgrade_data_backup

```
./metroag vstat_upgrade_data_backup -vvvv
```

At this point the data from the vstat nodes is backed in the NFS shared folder. If you experience a failure in the previous step, you can simply retry.

19. Power off all vstats

```
./metroag vstat_destroy -vvvv
```

At this point, all vstat nodes are shut down, but not deleted. The new nodes will be brought up with new VM names. Note that this step may be done manually if the user chooses. If you experience a failure running the Metro playbook for this step, a retry is advised. Or you can power off the VMs manually.

20. Predeploy new vstat nodes

```
./metroag vstat_predeploy -vvvv
```

At this point, the new vstat nodes are up and running, but they have not yet been configured. If you experience a failure in this step, execute the playbook vstat_upgrade_destroy.yml to delete the new nodes. Then retry the step.

21. Deploy new vstat nodes

```
./metroag vstat_deploy -vvvv
```

At this point, new vstat nodes have been deployed and configured to talk with VSD(s). If you experience a failure, retry playbook vstat_deploy.yml. If that fails again, destroy the VMs manually or use vstat_upgrade_destroy.yml, then retry starting at step 20.

22. Run vstat_upgrade_data_migrate

```
./metroag vstat_upgrade_data_migrate -vvvv
```

At this point the data from the old vstat nodes is migrated to the new VSTAT nodes from the NFS shared folder. If you experience a failure in the previous step, you can simply retry.


23. Run VSP upgrade postdeploy to finalize settings

```
./metroag vsp_upgrade_postdeploy -vvvv
```

This will execute the final steps of the upgrade. It can be rerun if there is a failure.

24. Run VSP post-upgrade heath

```
./metroag vsp_postupgrade_health -vvvv
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
./metroag build_upgrade -vvvv
```

2. Run health checks on VSD,VSC and VSTAT

```
./metroag vsp_preupgrade_health -vvvv
```
The health reports and any reported error should carefully be checked before proceeding with the next steps.

These health checks can be run at any time of the upgrade process.

3. Databse Backup of standalone VSD

```
./metroag vsd_sa_upgrade_database_backup -vvvv
```
At this point, vsd node database backup is completed. If you experience a failure in the previous step, you can simply retry.

4. Power off vsd

```
./metroag vsd_sa_upgrade_shutdown -vvvv
```

At this point, vsd is shut down, but not deleted. The new node will be brought up with new VM name. Note that this step may be done manually if the user chooses. If you experience a failure running the Metro playbook for this step, a retry is advised. Or you can power off the VM manually.

5. Predeploy new vsd node

```
./metroag vsd_predeploy -vvvv
```

At this point, the new vsd node is up and running, but it has not yet been configured. If you experience a failure in this step, execute the playbook vsd_sa_upgrade_destroy.yml to delete the new node. Then retry the step.

6. Deploy new vsd node

```
./metroag vsd_sa_upgrade_deploy -vvvv
```

At this point, VSD node is upgraded. If you experience a failure before the VSD install script runs, retry playbook vsd_sa_upgrade_deploy.yml. If that fails again or the failure comes after the VSD install script runs, destroy the VMs manually or use vsd_destroy.yml, then retry starting at step 5.

7. Set the VSD upgrade complete flag

```
./metroag vsd_upgrade_complete_flag -vvvv
```

After all the VSDs are upgraded, this step sets the upgrade flag to complete. It can be re-run in case of failure. It would be good time to login to VSD and v
erify the new version.

8. Run VSC health checks

```
./metroag vsc_health -e report_filename=vsc_preupgrade_health.txt -vvvv
```

This step is already done in step 2. You can skip it here if you wish. It is good practice to re-run at this point in order to inspect the report to make sure the VSD upgrade work has not caused problems.

9.  Run VSC backup and prep on vsc

```
./metroag vsc_sa_upgrade_backup_and_prep -vvvv
```

10. Run VSC deploy on vsc

```
./metroag vsc_sa_upgrade_deploy -vvvv
```

If the step fails, you can retry. Backup plan is to manually copy a valid .tim file to the VSC to affect either the deployment (new version of tim file) or a rollback. (old version of tim file). If rollback fails, you will need to deploy a new VSC using the old version--or recover the VM from a backup. You can use Metro for the deployment (vsc_predeploy, vsc_deploy, vsc_postdeploy...).

11. Run VSC postdeploy on vsc

```
./metroag vsc_sa_upgrade_postdeploy -vvvv
```

At this point, you have VSC upgrade is complete.

If this step fails, the recovery is much like that of the previous step: Manually update the tim file or a complete deploy of the old VSC followed by a retry.

*Upgrade VRS here!*

*If VSTAT node exist upgrade it using steps 17-22 in HA upgrade workflow mentioned in above section, if not skip to step 11 to finalize VSP upgrade*

12. Run VSP upgrade postdeploy to finalize settings

```
./metroag vsp_upgrade_postdeploy -vvvv
```

This will execute the final steps of the upgrade. It can be rerun if there is a failure.

13. Run VSP post-upgrade heath

```
./metroag vsp_postupgrade_health -vvvv
```

Writes out new health reports that can be compared to those produced in step one. Any errors or discrepancies should be investigated carefully.
