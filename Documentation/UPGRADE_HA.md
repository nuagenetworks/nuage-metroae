# Upgrading a Clustered Deployment with  Metro&#198;
## Prerequisites / Requirements / Notes
Before upgrading any components, you must have previously [set up your MetroÆ environment](SETUP.md) and [customized the upgrade environment for your target platform](CUSTOMIZE.md).

Ensure that you have specified `upgrade_from_version` and `upgrade_to_version`. MetroÆ uses these values to determine whether it is to perform a major upgrade or a minor upgrade. Failure to populate these variables could cause a minor upgrade to be treated as a major upgrade which results in the task being stuck in turn-on-api (which should not be executed for minor upgrades).

By default, the special enterprise called Shared Infrastructure is created on the VSD. When putting domains in maintenance mode prior to an upgrade, MetroÆ skips Shared Infrastructure domains because they cannot be modified.


## Example Deployment
For this example, our clustered (HA) deployment consists of:
* three VSD nodes in a cluster
* two VSC nodes
* VRS instance(s)
* one VSTAT (Elasticsearch) node


## Preupgrade Preparations
1. Run health checks on VSD, VSC and VSTAT.

     `./metro-ansible vsp_preupgrade_health -vvvv`

     Check the health reports carefully for any reported errors before proceeding. You can run health checks at any time during the upgrade process.

2. Backup the database and decouple the VSD cluster.

     `./metro-ansible vsd_ha_upgrade_database_backup_and_decouple -vvvv`

    `vsd_node1` has been decoupled from the cluster and is running in standalone (SA) mode.
    
    **Troubleshooting**: If you experience a failure, recovery depends on the state of `vsd_node1`. If it is still in the cluster, you can re-execute the command. If not, you must redeploy `vsd_node1` from a backup or otherwise recover.

## Upgrade VSD

1. Power off VSD nodes two and three.

     `./metro-ansible vsd_ha_upgrade_shutdown_2_and_3 -vvvv`

     `vsd_node2` and `vsd_node3` are shut down; they are not deleted. (The new nodes are brought up with the upgrade vmnames you previously specified. You have the option of powering down VSDs manually instead. 
     
     **Troubleshooting**: If you experience a failure you can re-execute the command or power off the VM manually.

2. Predeploy new VSD nodes two and three.

     `./metro-ansible vsd_ha_upgrade_predeploy_2_and_3 -vvvv`

     The new `vsd_node2` and `vsd_node3` are now up and running; they are not yet configured.
     
     **Troubleshooting**: If you experience a failure, delete the newly-created nodes by executing the command `./metro-ansible vsd_ha_upgrade_destroy_2_and_3`, then re-execute the predeploy command. Do NOT run `vsd_destroy` as this command destroys the "old" VM which is not what we want to do here.

3. Deploy new VSD nodes two and three.

     `./metro-ansible vsd_ha_upgrade_deploy_2_and_3 -vvvv`

     The VSD nodes have been upgraded.
     
     **Troubleshooting**: If you experience a failure before the VSD install script runs, re-execute the command. If it fails a second time or if the failure occurs after the VSD install script runs, destroy the VMs (either manually or with the command `./metro-ansible vsd_ha_upgrade_destroy_2_and_3`) then re-execute the deploy command. Do NOT run `vsd_destroy` as this command destroys the "old" VM.
     
4. Power off VSD node one.

     `./metro-ansible vsd_ha_upgrade_shutdown_1 -vvvv`

     `vsd_node1` shuts down; it is not deleted. (The new node is brought up with the `upgrade_vmname` you previously specified. You have the option of powering down VSD manually instead.
     
     **Troubleshooting**: If you experience a failure you can re-execute the command or power off the VM manually.

5. Predeploy the new VSD node one.

     `./metro-ansible vsd_ha_upgrade_predeploy_1 -vvvv`

     The new VSD node one is now up and running; it is not yet configured.
     
     **Troubleshotting**: If you experience a failure, delete the newly-created node by executing the command `./metro-ansible vsd_ha_upgrade_destroy_1`, then re-execute the predeploy command. Do NOT run `vsd_destroy` as this command destroys the "old" VM

6. Deploy the new VSD node one.

     `./metro-ansible vsd_ha_upgrade_deploy_1 -vvvv`

     All three VSD nodes are upgraded.
     
     **Troubleshooting**: If you experience a failure before the VSD install script runs, re-execute the command. If it fails a second time or if the failure occurs after the VSD install script runs, destroy the VMs (either manually or with the command `./metro-ansible vsd_ha_upgrade_destroy_1`) then re-execute the deploy command. Do NOT run `vsd_destroy` as this command destroys the "old" VM.

7. Set the VSD upgrade complete flag.

     `./metro-ansible vsd_upgrade_complete -vvvv`

     The upgrade flag is set to complete.
     
     **Troubleshooting**: If you experience a failure, you can re-execute the command.

8. Log into the VSDs and verify the new versions.

## Upgrade VSC Node One

1. Run VSC health check (optional).

     `./metro-ansible vsc_health -e report_filename=vsc_preupgrade_health.txt -vvvv`

     You performed health checks during preupgrade preparations, but it is good practice to run the check here as well to make sure the VSD upgrade has not caused any problems.

2. Backup and prepare VSC node one.

     `./metro-ansible vsc_ha_upgrade_backup_and_prep_1 -vvvv`
     
     **Troubleshooting**: If you experience a failure, you can re-execute the command.

3. Deploy VSC node one.

     `./metro-ansible vsc_ha_upgrade_deploy_1 -vvvv`

     VSC node one has been upgraded.
     
     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy (via scp) the .tim file, bof.cfg, and config.cfg (that were backed up in the previous step), to the VSC. Then reboot the VSC.

4. Run postdeploy for VSC node one.

     `./metro-ansible vsc_ha_upgrade_postdeploy_1 -vvvv`

     One VSC is now running the **old** version, and one is running the **new** version.
     
     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy (via scp) the .tim file, bof.cfg, and config.cfg (that were backed up before beginning VSC upgrade), to the VSC. Then reboot the VSC.

## Upgrade VRS
Upgrade your VRS(s) and then continue with this procedure. Do not proceed without completing this step.

## Upgrade VSC Node Two

1. Backup and prepare VSC node two.

     `./metro-ansible vsc_ha_upgrade_backup_and_prep_2 -vvvv`
     
     **Troubleshotting**: If you experience a failure, you can re-execute the command.

2. Deploy VSC node two.

     `./metro-ansible vsc_ha_upgrade_deploy_2 -vvvv`

     VSC node two has been upgraded.
     
     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy (via scp) the .tim file, bof.cfg, and config.cfg (that were backed up before beginning VSC upgrade), to the VSC. Then reboot the VSC.

3. Run postdeploy for VSC node two.

     `./metro-ansible vsc_ha_upgrade_postdeploy_2 -vvvv`

     Both VSCs are now running the **new** version.
     
     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy (via scp) the .tim file, bof.cfg, and config.cfg (that were backed up before beginning VSC upgrade), to the VSC. Then reboot the VSC.

## Upgrade VSTAT
Our example includes a VSTAT node. If your topology does not include one, proceed to *Finalize the Upgrade* below.

1. Run VSTAT health check (optional).

     `./metro-ansible vstat_health -e report_filename=vstat_preupgrade_health.txt -vvvv`

     You performed health checks during preupgrade preparations, but it is good practice to run the check here as well to make sure the VSD upgrade has not caused any problems.

2. Backup the VSTAT node.

     `./metro-ansible vstat_upgrade_data_backup -vvvv`

     Data from the VSTAT node is backed up in the NFS shared folder.
     
     **Troubleshooting**: If you experience a failure, you can re-execute the command.

3. Power off the VSTAT node.

     `./metro-ansible vstat_destroy -vvvv`

     VSTAT shuts down; it is not deleted. (The new node will be brought up with the new VM name.) You have the option of performing this step manually instead.
     
     **Troubleshooting**: If you experience a failure you can re-execute the command or power off the VM manually.

4. Predeploy the new VSTAT node.

     `./metro-ansible vstat_predeploy`

     The new VSD node is now up and running; it is not yet configured.
     
     **Troubleshooting**: If you experience a failure, delete the new node by executing the command `./metro-ansible vstat_upgrade_destroy` then re-execute the predeploy command. Do NOT run `vstat_destroy` for this step.

5. Deploy the new VSTAT node.

     `./metro-ansible vstat_deploy -vvvv`

     The new VSTAT node has been deployed and configured to talk with the VSD node.
     
     **Troubleshooting**: If you experience a failure, re-execute the command. If it fails a second time, destroy the VMs (either manually or with the command `./metro-ansible vstat_upgrade_destroy`) then proceed from the predeploy step above. Do NOT run `vstat_destroy` for this step.

6. Migrate data to new VSTAT node.

     `./metro-ansible vstat_upgrade_data_migrate -vvvv`

     The data from the old VSTAT node is migrated to the new VSTAT node from the NFS shared folder.
     
     **Troubleshooting**: If you experience a failure, you can re-execute the command.

## Finalize the Upgrade
1. Finalize the settings

     `./metro-ansible vsp_upgrade_postdeploy -vvvv`

     The final steps for the upgrade are executed.
     
     **Troubleshooting**: If you experience a failure, you can re-execute the command.

2. Run a health check.

     `./metro-ansible vsp_postupgrade_health -vvvv`

     Health reports are created that can be compared with the ones produced during preupgrade preparations. Investigate carefully any errors or discrepancies.

## Questions, Feedback, and Contributing
Ask questions and get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroÆ site](https://devops.nuagenetworks.net/).  
You may also contact us directly.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.
