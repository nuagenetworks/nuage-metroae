# Upgrading a Clustered Deployment with MetroAE
## Prerequisites / Requirements / Notes
Before upgrading any components, you must have previously [set up your MetroAE environment](SETUP.md) and [customized the upgrade environment for your target platform](CUSTOMIZE.md).

Ensure that you have added upgrade.yml to your deployment and specified `upgrade_from_version` and `upgrade_to_version`. MetroAE uses these values to determine whether it is to perform a patch upgrade, a major upgrade or a minor upgrade. Failure to populate these variables correctly could cause the wrong type of upgrde to be attempted, possibly resulting in an error. If a minor upgrade is treated as a major upgrade, for example, you may get stuck in the turn-on-api step which should not be executed for minor upgrades.

Note that if your existing VSP components were not installed using MetroAE or were installed using a different MetroAE host, you can still use MetroAE to do the upgrade. You must manually copy the MetroAE host user's ssh public key to each of the VSP Linux-based components (VSD, VSTAT, VNSUTIL) and to any KVM-based hypervisors used for VSP components and any KVM-based hypervisors where data-plane endpoints (VRS, NSGv) have been installed. This will allow passwordless ssh between the Ansible host and the Linux nodes in the deployment. Passwordless ssh to these nodes is a requirement for proper MetroAE operation for health and upgrade.

By default, the special enterprise called Shared Infrastructure is created on the VSD. When putting domains in maintenance mode prior to an upgrade, MetroAE skips Shared Infrastructure domains because they cannot be modified.

### Patch Upgrade for VSD, AKA in-place upgrade
A patch upgrade is applicable to the VSD cluster when upgrading from one 'u' release to another. A patch upgrade is also referred to as an in-place upgrade. The existing VSDs will remain in service. The migration ISO will be mounted and the migration script will be executed on each VSD. A patch upgrade is:

* Supported beginning in VSD version 5.4.1.
* `upgrade_from_version` and `upgrade_to_version` variables must be set to 'u' versions of the same release, e.g. 5.4.1 and 5.4.1u1, 5.4.1u1 and 5.4.1u4, etc.

Note that MetroAE only supports patch upgrades for VSD using the `upgrade_vsds` play. Attempting to do a patch release upgrade via any other method will result in an error.

### Active/Standby cluster upgrade
You can use MetroAE to upgrade Active/Standby VSD clusters, also known as geo-redundant clusters. You can also use MetroAE to upgrade Active/Standby VSTAT (ES) clusters. The support for this is built into the `upgrade_everything`, `upgrade_vsds`, and `upgrade_vstats` plays. A step-by-step manual procedure is supported, but is not documented here. See [Upgrading By Individual Steps](#upgrading-by-individual-steps-not-including-active-standby-clusters) for more information.

## Example Deployment
For this example, our clustered (HA) deployment consists of:
* three VSD nodes in a cluster
* two VSC nodes
* VRS instance(s)
* one VSTAT (Elasticsearch) node

## Upgrading Automatically
If your upgrade plans do not include upgrading VRSs or other dataplane components, you can upgrade everything with one command. If your upgrade plans do include VRSs or other dataplane components, you can upgrade everything with two commands. MetroAE also gives you the option of upgrading all instances of a component type, e.g. VSC, with a single command for each component type. If you prefer to have more control over each step in the upgrade process proceed to [Upgrading By Individual Steps](#upgrading-by-individual-steps-not-including-active-standby-clusters) for instructions.

### Upgrade All Components including Active/Standby clusters (does not pause for external VRS/dataplane upgrade)

     metroae upgrade everything

Issuing this workflow will detect if components are clustered (HA) or not and will upgrade all components that are defined in the deployment.  This option does not pause until completion to allow VRSs and other dataplane components to be upgraded.  If dataplane components need to be upgraded, the following option should be performed instead.

### Upgrade All Components including Active/Standby clusters (includes pause for VRS)

     metroae upgrade beforevrs

     ( Upgrade the VRSs andn other dataplane components )

     metroae upgrade aftervrs

Issuing the above workflows will detect if components are clustered (HA) or not and will upgrade all components that are defined in the deployment.  This option allows the VRSs and other dataplane components to be upgraded between other components.

### Upgrade Individual Components including Active Standby clusters

     metroae upgrade preupgrade health

     metroae upgrade vsds

     metroae upgrade vscs beforevrs

     ( Upgrade the VRS(s) )

     metroae upgrade vscs aftervrs

     metroae upgrade vstats

     metroae upgrade postdeploy

     metroae upgrade postupgrade health

Issuing the above workflows will detect if components are clustered (HA) or not and will upgrade all components that are defined in the deployment.  This option allows the VRS(s) to be upgraded in-between other components.  Performing individual workflows can allow specific components to be skipped or upgraded at different times.

## Upgrading By Individual Steps not including Active/Standby clusters
The following workflows will upgrade each component in individual steps. Performing an upgrade in this way allows full control of the timing of the upgrade process and provides opportunities for you to add custom steps to the overall process. Note that the steps listed below are only applicable for clustered (HA) deployments.  Active/Standby cluster upgrades require additional steps that are not documented here. See the component playbooks `src\playbooks\with_build\upgrade_vsds.yml` and `src\playbooks\with_build\upgrade_vstats.yml` for the full list of steps.

### Preupgrade Preparations
1. Run health checks on VSD, VSC and VSTAT.

     `metroae upgrade preupgrade health`

     Check the health reports carefully for any reported errors before proceeding. You can run health checks at any time during the upgrade process.

2. Backup the database and decouple the VSD cluster.

     `metroae upgrade ha vsd dbbackup`

    `vsd_node1` has been decoupled from the cluster and is running in standalone (SA) mode.

    **Troubleshooting**: If you experience a failure, recovery depends on the state of `vsd_node1`. If it is still in the cluster, you can re-execute the command. If not, you must redeploy `vsd_node1` from a backup or otherwise recover.

    **Note**
    MetroAE provides a simple tool for optionally cleaning up the backup files that are generated during the upgrade process. The tool deletes the backup files for both VSD and VSC. There are two modes foe clean-up, the first one deletes all the backups and the second one deletes only the latest backup. By default the tool deletes only the latest backup. If you'd like to clean-up the backup files, you can simply run below commands:
    Clean up all the backup files: `metroae upgrade cleanup -e delete_all_backups=true`
    Clean up the latest backup files: `metroae upgrade cleanup`

### Upgrade VSD

1. Power off VSD nodes two and three.

     `metroae upgrade ha vsd shutdown23`

     `vsd_node2` and `vsd_node3` are shut down; they are not deleted. The new nodes are brought up with the upgrade vmnames you previously specified. You have the option of powering down VSDs manually instead.

     **Troubleshooting**: If you experience a failure you can re-execute the command or power off the VM manually.

2. Predeploy new VSD nodes two and three.

     `metroae upgrade ha vsd predeploy23`

     The new `vsd_node2` and `vsd_node3` are now up and running; they are not yet configured.

     **Troubleshooting**: If you experience a failure, delete the newly-created nodes by executing the command `metroae upgrade destroy ha vsd23`, then re-execute the predeploy command. Do NOT run `metroae destroy vsds` as this command destroys the "old" VM which is not what we want to do here.

3. Deploy new VSD nodes two and three.

     `metroae upgrade ha vsd deploy23`

     The VSD nodes have been upgraded.

     **Troubleshooting**: If you experience a failure before the VSD install script runs, re-execute the command. If it fails a second time or if the failure occurs after the VSD install script runs, destroy the VMs (either manually or with the command `metroae upgrade destroy ha vsd23`) then re-execute the deploy command. Do NOT run `metroae destroy vsds` as this command destroys the "old" VM.

4. Power off VSD node one.

     `metroae upgrade ha vsd shutdown1`

     `vsd_node1` shuts down; it is not deleted. The new node is brought up with the `upgrade_vmname` you previously specified. You have the option of powering down VSD manually instead.

     **Troubleshooting**: If you experience a failure you can re-execute the command or power off the VM manually.

5. Predeploy the new VSD node one.

     `metroae upgrade ha vsd predeploy1`

     The new VSD node one is now up and running; it is not yet configured.

     **Troubleshooting**: If you experience a failure, delete the newly-created node by executing the command `metroae upgrade destroy ha vsd1`, then re-execute the predeploy command. Do NOT run `vsd_destroy` as this command destroys the "old" VM.

6. Deploy the new VSD node one.

     `metroae upgrade ha vsd deploy1`

     All three VSD nodes are upgraded.

     **Troubleshooting**: If you experience a failure before the VSD install script runs, re-execute the command. If it fails a second time or if the failure occurs after the VSD install script runs, destroy the VMs (either manually or with the command `metroae upgrade destroy ha vsd1`) then re-execute the deploy command. Do NOT run `metroae destroy vsds` as this command destroys the "old" VM.

7. Set the VSD upgrade complete flag.

     `metroae upgrade ha vsd complete`

     The upgrade flag is set to complete.

     **Troubleshooting**: If you experience a failure, you can re-execute the command.

8. Log into the VSDs and verify the new versions.

### Upgrade VSC Node One

1. Run VSC health check (optional).

     `metroae upgrade ha vsc health -e report_filename=vsc_preupgrade_health.txt`

     You performed health checks during preupgrade preparations, but it is good practice to run the check here as well to make sure the VSD upgrade has not caused any problems.

2. Backup and prepare VSC node one.

     `metroae upgrade ha vsc backup1`

     **Troubleshooting**: If you experience a failure, you can re-execute the command.

3. Deploy VSC node one.

     `metroae upgrade ha vsc deploy1`

     VSC node one has been upgraded.

     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy (via scp) the .tim file, bof.cfg, and config.cfg (that were backed up in the previous step), to the VSC. Then reboot the VSC.

4. Run postdeploy for VSC node one.

     `metroae upgrade ha vsc postdeploy1`

     One VSC is now running the **old** version, and one is running the **new** version.

     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy (via scp) the .tim file, bof.cfg, and config.cfg (that were backed up before beginning VSC upgrade), to the VSC. Then reboot the VSC.

### Upgrade VRS
Upgrade your VRS(s) and then continue with this procedure. Do not proceed without completing this step.

### Upgrade VSC Node Two

1. Backup and prepare VSC node two.

     `metroae upgrade ha vsc backup2`

     **Troubleshooting**: If you experience a failure, you can re-execute the command.

2. Deploy VSC node two.

     `metroae upgrade ha vsc deploy2`

     VSC node two has been upgraded.

     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy (via scp) the .tim file, bof.cfg, and config.cfg (that were backed up before beginning VSC upgrade), to the VSC. Then reboot the VSC.

3. Run postdeploy for VSC node two.

     `metroae upgrade ha vsc postdeploy2`

     Both VSCs are now running the **new** version.

     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy (via scp) the .tim file, bof.cfg, and config.cfg (that were backed up before beginning VSC upgrade), to the VSC. Then reboot the VSC.

### Upgrade VSTAT
Our example includes a VSTAT node. If your topology does not include one, proceed to *Finalize the Upgrade* below.

1. Run VSTAT health check (optional).

     `metroae upgrade ha vstat health -e report_filename=vstat_preupgrade_health.txt`

     You performed health checks during preupgrade preparations, but it is good practice to run the check here as well to make sure the VSD upgrade has not caused any problems.

2. Prepare the VSTAT nodes for upgrade.

     `metroae upgrade ha vstat prep`

     Sets up SSH and disables stats collection.


3. Upgrade the VSTAT nodes.

     `metroae upgrade ha vstat inplace`

     Performs an in-place upgrade of the VSTAT nodes.

4. Complete VSTAT upgrade and perform post-upgrade checks.

     `metroae upgrade ha vstat wrapup`

     Completes the upgrade process, renables stats and performs a series of checks to ensure the VSTAT nodes are healthy.

### Finalize the Upgrade
1. Finalize the settings

     `metroae upgrade postdeploy`

     The final steps for the upgrade are executed.

     **Troubleshooting**: If you experience a failure, you can re-execute the command.

2. Run a health check.

     `metroae upgrade postupgrade health`

     Health reports are created that can be compared with the ones produced during preupgrade preparations. Investigate carefully any errors or discrepancies.

## Questions, Feedback, and Contributing
Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project").

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
