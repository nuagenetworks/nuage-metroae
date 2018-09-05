# Upgrading a Standalone Deployment with  Metro&#198;
## Prerequisites / Requirements / Notes
Before upgrading any components, you must have previously [set up your MetroÆ environment](SETUP.md) and [customized the upgrade environment for your target platform](CUSTOMIZE.md). Ensure that you have specified `upgrade_from_version` and `upgrade_to_version` in `build_vars.yml`. MetroÆ uses these values to determine whether it is to perform a major upgrade or a minor upgrade. Failure to populate these variables could cause a minor upgrade to be treated as a major upgrade which results in the task being stuck in turn-on-api (which should not be executed for minor upgrades).

By default, the special enterprise called Shared Infrastructure is created on the VSD. When putting domains in maintenance mode prior to an upgrade, MetroÆ skips Shared Infrastructure domains because they cannot be modified.

## Example Deployment
For this example, our standalone (SA) deployment consists of:
* one VSD node
* one VSC node
* VRS instance(s)
* one VSTAT (Elasticsearch) node


## Preupgrade Preparations
1. Run health checks on VSD, VSC and VSTAT.

     `./metro-ansible vsp_preupgrade_health -vvvv`

     Check the health reports carefully for any reported errors before proceeding. You can run health checks at any time during the upgrade process.

2. Backup the VSD node database.

     `./metro-ansible vsd_sa_upgrade_database_backup -vvvv`

    The VSD node database is backed up. If you experience a failure you can re-execute the command.

## Upgrade VSD

1. Power off the VSD node.

     `./metro-ansible vsd_sa_upgrade_shutdown -vvvv`

     VSD is shut down; it is not deleted. (The new node is brought up with the `upgrade_vmname` you specified in `build_vars.yml`.) You have the option of powering down VSD manually instead. If you experience a failure you can re-execute the command or power off the VM manually.

2. Predeploy the new VSD node.

     `./metro-ansible vsd_predeploy -vvvv`

     The new VSD node is now up and running; it is not yet configured. If you experience a failure, delete the new node by executing the command `./metro-ansible vsd_sa_upgrade_destroy`, then re-execute the predeploy command.

3. Deploy the new VSD node.

     `./metro-ansible vsd_sa_upgrade_deploy -vvvv`

     The VSD node is upgraded. If you experience a failure before the VSD install script runs, re-execute the command. If it fails a second time or if the failure occurs after the VSD install script runs, destroy the VMs (either manually or with the command `./metro-ansible vsd_destroy`) then re-execute the deploy command.

4. Set the VSD upgrade complete flag.

     `./metro-ansible vsd_upgrade_complete -vvvv`

     The upgrade flag is set to complete. If you experience a failure, you can re-execute the command.

5. Log into the VSD and verify the new version.

## Upgrade VSC
This example is for one VSC node. If your topology has more than one VSC node, proceed to the **Upgrade VSC Node One** section of  [UPGRADE_HA.md](Documentation/UPGRADE_HA.md) and follow those instructions through to the end.

1. Run VSC health check (optional).

     `./metro-ansible vsc_health -e report_filename=vsc_preupgrade_health.txt -vvvv`

     You performed health checks during preupgrade preparations, but it is good practice to run the check here as well to make sure the VSD upgrade has not caused any problems.

2. Backup and prepare the VSC node.

     `./metro-ansible vsc_sa_upgrade_backup_and_prep -vvvv`
     
     If you experience failure, you can re-execute the command.

3. Deploy VSC.

     `./metro-ansible vsc_sa_upgrade_deploy -vvvv`

     The VSC is upgraded. If you experience a failure, you can re-execute the command. If it fails a second time, manually copy a valid .tim file to the VSC to affect the deployment. If that fails, deploy a new VSC using the old version, or recover the VM from a backup. You can use Metro&#198; for the deployment (vsc_predeploy, vsc_deploy, vsc_postdeploy...).

4. Run VSC postdeploy.

     `./metro-ansible vsc_sa_upgrade_postdeploy -vvvv`

     VSC upgrade is complete. If you experience a failure, you can re-execute the command. If it fails a second time, manually copy a valid .tim file to the VSC to affect the deployment. If that fails, deploy a new VSC using the old version, or recover the VM from a backup. You can use Metro&#198; for the deployment (vsc_predeploy, vsc_deploy, vsc_postdeploy...).

## Upgrade VRS
Upgrade your VRS(s) and then continue with this procedure. Do not proceed without completing this step.

## Upgrade VSTAT
1. Run VSTAT health check (optional).

     `./metro-ansible vstat_health -e report_filename=vstat_preupgrade_health.txt -vvvv`

     You performed health checks during preupgrade preparations, but it is good practice to run the check here as well to make sure the VSD upgrade has not caused any problems.

2. Backup the VSTAT node.

     `./metro-ansible vstat_upgrade_data_backup -vvvv`

     Data from the VSTAT node is backed up in the NFS shared folder. If you experience a failure, you can re-execute the command.

3. Power off the VSTAT node.

     `./metro-ansible vstat_destroy -vvvv`

     VSTAT shuts down; it is not deleted. (The new node will be brought up with the new VM name.) You have the option of performing this step manually instead. If you experience a failure you can re-execute the command or power off the VM manually.

4. Predeploy the new VSTAT node.

     `./metro-ansible vstat_predeploy`

     The new VSD node is now up and running; it is not yet configured. If you experience a failure, delete the new node by executing the command then re-execute the predeploy command.  

5. Deploy the new VSTAT node.

     `./metro-ansible vstat_deploy -vvvv`

     The new VSTAT node has been deployed and configured to talk with the VSD node. If you experience a failure, re-execute the command. If it fails a second time, destroy the VMs (either manually or with the command `./metro-ansible vstat_upgrade_destroy`) then proceed from the predeploy step above.

6. Migrate data to new VSTAT node.

     `./metro-ansible vstat_upgrade_data_migrate -vvvv`

     The data from the old VSTAT node is migrated to the new VSTAT node from the NFS shared folder. If you experience a failure, you can re-execute the command.

## Finalize the Upgrade
1. Finalize the settings.

     `./metro-ansible vsp_upgrade_postdeploy -vvvv`

     The final steps for the upgrade are executed. If you experience a failure, you can re-execute the command.

2. Run a health check.

     `./metro-ansible vsp_postupgrade_health -vvvv`

     Health reports are created that can be compared with the ones produced during preupgrade preparations. Investigate carefully any errors or discrepancies.

## Questions, Feedback, and Contributing

Ask questions and get support via email.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")  

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to Nuage Metro Automation Engine by submitting your own code to the project.
