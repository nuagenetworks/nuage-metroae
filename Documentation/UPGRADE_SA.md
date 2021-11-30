# Upgrading a Standalone Deployment with MetroAE

## Prerequisites / Requirements / Notes

Before upgrading any components, you must have previously [set up your MetroAE environment](SETUP.md) and [customized the upgrade environment for your target platform](CUSTOMIZE.md).

Ensure that you have added upgrade.yml to your deployment and specified `upgrade_from_version` and `upgrade_to_version`. MetroAE uses these values to determine whether it is to perform a patch upgrade, a major upgrade or a minor upgrade. Failure to populate these variables correctly could cause the wrong type of upgrde to be attempted, possibly resulting in an error. If a minor upgrade is treated as a major upgrade, for example, you may get stuck in the turn-on-api step which should not be executed for minor upgrades.

Note that if your existing VSP components were not installed using MetroAE or were installed using a different MetroAE host, you can still use MetroAE to do the upgrade. You must manually copy the MetroAE host user's ssh public key to each of the VSP Linux-based components (VSD, VSTAT, VNSUTIL) and to any KVM-based hypervisors used for VSP components and any KVM-based hypervisors where data-plane endpoints (VRS, NSGv) have been installed. This will allow passwordless ssh between the Ansible host and the Linux nodes in the deployment. Passwordless ssh to these nodes is a requirement for proper MetroAE operation for health and upgrade.

By default, the special enterprise called Shared Infrastructure is created on the VSD. When putting domains in maintenance mode prior to an upgrade, MetroAE skips Shared Infrastructure domains because they cannot be modified.

### Patch Upgrade for VSD, while installing VSD
A inplace upgrade can be carried out during the installation of the VSD cluster. The VSDs are installed and patch will be performed directly if the `vsd_install_inplace_upgrade` is set to true. The migration ISO wil be mounted and the migration script will be executed after the successful installation of VSD. A VSD inplace upgrade during the installation is:

* Supported beginning in VSD version 5.4.1.
* The `upgrade_from_version` variable must be set to main version of VSD i.e. 5.4.1,6.0.3 or 20.10.R1 and `upgrade_to_version` variable must be set to respactive patch versions i.e for 5.4.1 it could be 5.4.1u1, for 6.0.3 it could be 6.0.5, for 20.10.R1 it could be 20.10.R2 etc.

Note that to upgrade VSDs during the installation it can be done using `install everything`, `install vsds` commands.

### Patch Upgrade for VSD, AKA in-place upgrade

A patch upgrade is applicable to the VSD cluster when upgrading from one 'u' release to another. A patch upgrade is also referred to as an in-place upgrade. The existing VSDs will remain in service. The migration ISO will be mounted and the migration script will be executed on each VSD. A patch upgrade is:

* Supported beginning in VSD version 5.4.1.
* `upgrade_from_version` and `upgrade_to_version` variables must be set to 'u' versions of the same release, e.g. 5.4.1 and 5.4.1u1, 5.4.1u1 and 5.4.1u4, etc.

Note that MetroAE only supports patch upgrades for VSD using the `upgrade_vsds` play. Attempting to do a patch release upgrade via any other method will result in an error.

## Example Deployment

For this example, our standalone (SA) deployment consists of:

* one VSD node
* one VSC node
* VRS instance(s)
* one VSTAT (Elasticsearch) node

## Upgrading Automatically

If your topology does not include VRS you can upgrade everything with one command. If it does includes VRS you can upgrade everything with two commands. MetroAE also gives you the option of upgrading individual components with a single command for each. If you prefer to have more control over each step in the upgrade process proceed to [Upgrading By Individual Steps](#upgrading-by-individual-steps) for instructions.

### Upgrade All Components (without VRS)

     metroae-container upgrade everything

Issuing this workflow will detect if components are clustered (HA) or not and will upgrade all components that are defined in the deployment.  This option does not pause until completion to allow VRS(s) to be upgraded.  If VRS(s) need to be upgraded, the following option should be performed instead.

### Upgrade All Components (with VRS)

     metroae-container upgrade beforevrs

     ( Upgrade the VRS(s) )

     metroae-container upgrade aftervrs

Issuing the above workflows will detect if components are clustered (HA) or not and will upgrade all components that are defined in the deployment.  This option allows the VRS(s) to be upgraded in-between other components.

### Upgrade Individual Components

     metroae-container upgrade preupgrade health

     metroae-container upgrade vsds

     metroae-container upgrade vscs beforevrs

     ( Upgrade the VRS(s) )

     metroae-container upgrade vscs aftervrs

     metroae-container upgrade vstats

     metroae-container upgrade postdeploy

     metroae-container upgrade postupgrade health

Issuing the above workflows will detect if components are clustered (HA) or not and will upgrade all components that are defined in the deployment.  This option allows the VRS(s) to be upgraded in-between other components.  Performing individual workflows can allow specific components to be skipped or upgraded at different times.

## Upgrading By Individual Steps

The following workflows will upgrade each component in individual steps.  The steps listed below are only applicable for stand-alone (SA) deployments.  Performing an upgrade in this way allows full control of the timing of the upgrade process.

### Preupgrade Preparations

1. Run health checks on VSD, VSC and VSTAT.

     `metroae-container upgrade preupgrade health`

     Check the health reports carefully for any reported errors before proceeding. You can run health checks at any time during the upgrade process.

2. Backup the VSD node database.

     `metroae-container upgrade sa vsd dbbackup`

    The VSD node database is backed up.

    **Troubleshooting**: If you experience a failure you can re-execute the command.

    **Note**
    MetroAE provides a simple tool for optionally cleaning up the backup files that are generated during the upgrade process. The tool deletes the backup files for both VSD and VSC. There are two modes foe clean-up, the first one deletes all the backups and the second one deletes only the latest backup. By default the tool deletes only the latest backup. If you'd like to clean-up the backup files, you can simply run below commands:
    Clean up all the backup files: `metroae-container vsp_upgrade_cleanup -e delete_all_backups=true`
    Clean up the latest backup files: `metroae-container vsp_upgrade_cleanup`

### Upgrade VSD

1. Power off the VSD node.

     `metroae-container upgrade sa vsd shutdown`

     VSD is shut down; it is not deleted. (The new node is brought up with the `upgrade_vmname` you previously specified.) You have the option of powering down VSD manually instead.

     **Troubleshooting**: If you experience a failure you can re-execute the command or power off the VM manually.

2. Predeploy the new VSD node.

     `metroae-container install vsds predeploy`

     The new VSD node is now up and running; it is not yet configured.

     **Troubleshooting**: If you experience a failure, delete the new node by executing the command `metroae-container upgrade destroy sa vsd`, then re-execute the predeploy command. Do NOT run `metroae-container destroy vsds` as this command destroys the "old" VM which is not what we want to do here.

3. Deploy the new VSD node.

     `metroae-container upgrade sa vsd deploy`

     The VSD node is upgraded.

     **Troubleshooting**: If you experience a failure before the VSD install script runs, re-execute the command. If it fails a second time or if the failure occurs after the VSD install script runs, destroy the VMs (either manually or with the command `metroae-container upgrade destroy sa vsd`) then re-execute the deploy command. Do NOT run `metroae-container destroy vsds` for this step.

4. Set the VSD upgrade complete flag.

     `metroae-container upgrade sa vsd complete`

     The upgrade flag is set to complete.

     **Troubleshooting**: If you experience a failure, you can re-execute the command.
5. Apply VSD license (if needed)
     
     `metroae-container vsd license`

     The VSD license will be applied.
     
6. Log into the VSD and verify the new version.

### Upgrade VSC

This example is for one VSC node. If your topology has more than one VSC node, proceed to the **Upgrade VSC Node One** section of  [UPGRADE_HA.md](UPGRADE_HA.md) and follow those instructions through to the end.

1. Run VSC health check (optional).

     `metroae-container upgrade sa vsc health -e report_filename=vsc_preupgrade_health.txt`

     You performed health checks during preupgrade preparations, but it is good practice to run the check here as well to make sure the VSD upgrade has not caused any problems.

2. Backup and prepare the VSC node.

     `metroae-container upgrade sa vsc backup`

     **Troubleshooting**: If you experience failure, you can re-execute the command.

3. Deploy VSC.

     `metroae-container upgrade sa vsc deploy`

     The VSC is upgraded.

     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy a valid .tim file to the VSC to affect the deployment. If that fails, deploy a new VSC using the old version, or recover the VM from a backup. You can use MetroAE for the deployment (vsc_predeploy, vsc_deploy, vsc_postdeploy...).

4. Run VSC postdeploy.

     `metroae-container upgrade sa vsc postdeploy`

     VSC upgrade is complete.

     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy a valid .tim file to the VSC to affect the deployment. If that fails, deploy a new VSC using the old version, or recover the VM from a backup. You can use MetroAE for the deployment (vsc_predeploy, vsc_deploy, vsc_postdeploy...).

### Upgrade VRS

Upgrade your VRS(s) and then continue with this procedure. Do not proceed without completing this step.

### Upgrade VSTAT

Our example includes a VSTAT node. If your topology does not include one, proceed to *Finalize the Upgrade* below.

1. Run VSTAT health check (optional).

     `metroae-container upgrade sa vstat health -e report_filename=vstat_preupgrade_health.txt`

     You performed health checks during preupgrade preparations, but it is good practice to run the check here as well to make sure the VSD upgrade has not caused any problems.

2. Prepare the VSTAT node for upgrade.

     `metroae-container upgrade sa vstat prep`

     Sets up SSH and disables stats collection.

3. Upgrade the VSTAT node.

     `metroae-container upgrade sa vstat inplace`

     Performs an in-place upgrade of the VSTAT.

4. Complete VSTAT upgrade and perform post-upgrade checks.

     `metroae-container upgrade sa vstat wrapup`

     Completes the upgrade process, renables stats and performs a series of checks to ensure the VSTAT is healthy.

### Finalize the Upgrade

1. Finalize the settings.

     `metroae-container upgrade postdeploy`

     The final steps for the upgrade are executed.

     **Troubleshooting**: If you experience a failure, you can re-execute the command.

2. Run a health check.

     `metroae-container upgrade postupgrade health`

     Health reports are created that can be compared with the ones produced during preupgrade preparations. Investigate carefully any errors or discrepancies.

## Questions, Feedback, and Contributing

Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).  
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:devops@nuagenetworks.net "send email to nuage-metro project").

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
