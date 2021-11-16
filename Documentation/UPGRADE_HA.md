# Upgrading a Clustered Deployment with MetroAE

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

### Active/Standby cluster upgrade

You can use MetroAE to upgrade Active/Standby VSD clusters, also known as geo-redundant clusters. You can also use MetroAE to upgrade Active/Standby VSTAT (ES) clusters. The support for this is built into the `upgrade_everything`, `upgrade_vsds`, and `upgrade_vstats` plays. A step-by-step manual procedure is supported, but is not documented here. See [Upgrading By Individual Steps](#upgrading-by-individual-steps-not-including-active-standby-clusters) for more information.

If you want to perform a standby VSD cluster inplace upgrade only, You can use the following command.

`metroae-container upgrade vsds standby inplace`

### VSD Stats-out upgrade

By default, Nuage VSD and VSTAT components are deployed in what is referred to as 'stats-in' mode. This refers to the fact that the stats collector process that feeds data to the ES cluster runs 'in' the VSDs. An alternative to this deployment, installation of which is also supported by MetroAE, is a 'stats-out' mode. In 'stats-out', three additional VSDs are deployed specifically to handle the stats collection. We refer to those extra VSD nodes as VSD stats-out nodes. In such a case, the stats collection work is not running 'in' the regular VSD cluster. Stats collection is done 'out' in the cluster of 3 VSD stats-out nodes. ES nodes are also deployed in a special way, with 3 ES nodes in a cluster and 3+ ES nodes configured as 'data' nodes. You can find out more detail about the deployments in the Nuage documentation.

You can use MetroAE to install or upgrade upgrade your stats-out configuration. Special workflows have been created to support the stats-out upgrade. These special workflows have been included automatically in the `metroae-container upgrade everything` command. Alternatively you can use the step-by-step upgrade procedure to perform your upgrade. The `metroae-container upgrade vsd stats` command will handle upgrading the separate VSD stats-out nodes. The `metroae-container upgrade vsd stats inplace` command will apply a patch (in-place) upgrade of the VSD stats-out nodes.

Note: Upgrade of the VSD stats-out nodes should take place only after the primary VSD cluster and all Elasticsearch nodes have been upgraded.

A patch upgrade of the stats out node can also be done by running `upgrade_vsd_stats_inplace` procedure.

## Example Deployment

For this example, our clustered (HA) deployment consists of:

* three VSD nodes in a cluster
* two VSC nodes
* VRS instance(s)
* one VSTAT (Elasticsearch) node

## Upgrading Automatically

If your upgrade plans do not include upgrading VRSs or other dataplane components, you can upgrade everything with one command. If your upgrade plans do include VRSs or other dataplane components, you can upgrade everything with two commands. MetroAE also gives you the option of upgrading all instances of a component type, e.g. VSC, with a single command for each component type. If you prefer to have more control over each step in the upgrade process proceed to [Upgrading By Individual Steps](#upgrading-by-individual-steps-not-including-active-standby-clusters) for instructions.

### Upgrade All Components including Active/Standby clusters (does not pause for external VRS/dataplane upgrade)

     metroae-container upgrade everything

Issuing this workflow will detect if components are clustered (HA) or not and will upgrade all components that are defined in the deployment.  This option does not pause until completion to allow VRSs and other dataplane components to be upgraded.  If dataplane components need to be upgraded, the following option should be performed instead.

### Upgrade All Components including Active/Standby clusters (includes pause for VRS)

     metroae-container upgrade beforevrs

     ( Upgrade the VRSs andn other dataplane components )

     metroae-container upgrade aftervrs

Issuing the above workflows will detect if components are clustered (HA) or not and will upgrade all components that are defined in the deployment.  This option allows the VRSs and other dataplane components to be upgraded between other components.

### Upgrade Individual Components including Active Standby clusters

     metroae-container upgrade preupgrade health

     metroae-container upgrade vsds

     metroae-container upgrade vscs beforevrs

     ( Upgrade the VRS(s) )

     metroae-container upgrade vscs aftervrs

     metroae-container upgrade vstats

     metroae-container upgrade postdeploy

     metroae-container upgrade postupgrade health

Issuing the above workflows will detect if components are clustered (HA) or not and will upgrade all components that are defined in the deployment.  This option allows the VRS(s) to be upgraded in-between other components.  Performing individual workflows can allow specific components to be skipped or upgraded at different times.

## Upgrading By Individual Steps not including Active/Standby clusters

The following workflows will upgrade each component in individual steps. Performing an upgrade in this way allows full control of the timing of the upgrade process and provides opportunities for you to add custom steps to the overall process. Note that the steps listed below are only applicable for clustered (HA) deployments.  Active/Standby cluster upgrades require additional steps that are not documented here. See the component playbooks `src\playbooks\with_build\upgrade_vsds.yml` and `src\playbooks\with_build\upgrade_vstats.yml` for the full list of steps.

### Preupgrade Preparations

1. Run health checks on VSD, VSC and VSTAT.

     `metroae-container upgrade preupgrade health`

     Check the health reports carefully for any reported errors before proceeding. You can run health checks at any time during the upgrade process.

2. Backup the database and decouple the VSD cluster.

     `metroae-container upgrade ha vsd dbbackup`

    `vsd_node1` has been decoupled from the cluster and is running in standalone (SA) mode.

    **Troubleshooting**: If you experience a failure, recovery depends on the state of `vsd_node1`. If it is still in the cluster, you can re-execute the command. If not, you must redeploy `vsd_node1` from a backup or otherwise recover.

    **Note**
    MetroAE provides a simple tool for optionally cleaning up the backup files that are generated during the upgrade process. The tool deletes the backup files for both VSD and VSC. There are two modes foe clean-up, the first one deletes all the backups and the second one deletes only the latest backup. By default the tool deletes only the latest backup. If you'd like to clean-up the backup files, you can simply run below commands:
    Clean up all the backup files: `metroae-container upgrade cleanup -e delete_all_backups=true`
    Clean up the latest backup files: `metroae-container upgrade cleanup`

### Upgrade VSD

1. Power off VSD nodes two and three.

     `metroae-container upgrade ha vsd shutdown23`

     `vsd_node2` and `vsd_node3` are shut down; they are not deleted. The new nodes are brought up with the upgrade vmnames you previously specified. You have the option of powering down VSDs manually instead.

     **Troubleshooting**: If you experience a failure you can re-execute the command or power off the VM manually.

2. Predeploy new VSD nodes two and three.

     `metroae-container upgrade ha vsd predeploy23`

     The new `vsd_node2` and `vsd_node3` are now up and running; they are not yet configured.

     **Troubleshooting**: If you experience a failure, delete the newly-created nodes by executing the command `metroae-container upgrade destroy ha vsd23`, then re-execute the predeploy command. Do NOT run `metroae-container destroy vsds` as this command destroys the "old" VM which is not what we want to do here.

3. Deploy new VSD nodes two and three.

     `metroae-container upgrade ha vsd deploy23`

     The VSD nodes have been upgraded.

     **Troubleshooting**: If you experience a failure before the VSD install script runs, re-execute the command. If it fails a second time or if the failure occurs after the VSD install script runs, destroy the VMs (either manually or with the command `metroae-container upgrade destroy ha vsd23`) then re-execute the deploy command. Do NOT run `metroae-container destroy vsds` as this command destroys the "old" VM.

4. Power off VSD node one.

     `metroae-container upgrade ha vsd shutdown1`

     `vsd_node1` shuts down; it is not deleted. The new node is brought up with the `upgrade_vmname` you previously specified. You have the option of powering down VSD manually instead.

     **Troubleshooting**: If you experience a failure you can re-execute the command or power off the VM manually.

5. Predeploy the new VSD node one.

     `metroae-container upgrade ha vsd predeploy1`

     The new VSD node one is now up and running; it is not yet configured.

     **Troubleshooting**: If you experience a failure, delete the newly-created node by executing the command `metroae-container upgrade destroy ha vsd1`, then re-execute the predeploy command. Do NOT run `vsd_destroy` as this command destroys the "old" VM.

6. Deploy the new VSD node one.

     `metroae-container upgrade ha vsd deploy1`

     All three VSD nodes are upgraded.

     **Troubleshooting**: If you experience a failure before the VSD install script runs, re-execute the command. If it fails a second time or if the failure occurs after the VSD install script runs, destroy the VMs (either manually or with the command `metroae-container upgrade destroy ha vsd1`) then re-execute the deploy command. Do NOT run `metroae-container destroy vsds` as this command destroys the "old" VM.

7. Set the VSD upgrade complete flag.

     `metroae-container upgrade ha vsd complete`

     The upgrade flag is set to complete.

     **Troubleshooting**: If you experience a failure, you can re-execute the command.

8. Apply VSD license (if needed)
     
     `metroae-container vsd license`

     The VSD license will be applied.
     
9. Log into the VSDs and verify the new versions.

### Upgrade VSC Node One

1. Run VSC health check (optional).

     `metroae-container upgrade ha vsc health -e report_filename=vsc_preupgrade_health.txt`

     You performed health checks during preupgrade preparations, but it is good practice to run the check here as well to make sure the VSD upgrade has not caused any problems.

2. Backup and prepare VSC node one.

     `metroae-container upgrade ha vsc backup1`

     **Troubleshooting**: If you experience a failure, you can re-execute the command.

3. Deploy VSC node one.

     `metroae-container upgrade ha vsc deploy1`

     VSC node one has been upgraded.

     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy (via scp) the .tim file, bof.cfg, and config.cfg (that were backed up in the previous step), to the VSC. Then reboot the VSC.

4. Run postdeploy for VSC node one.

     `metroae-container upgrade ha vsc postdeploy1`

     One VSC is now running the **old** version, and one is running the **new** version.

     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy (via scp) the .tim file, bof.cfg, and config.cfg (that were backed up before beginning VSC upgrade), to the VSC. Then reboot the VSC.

### Upgrade VRS

Upgrade your VRS(s) and then continue with this procedure. Do not proceed without completing this step.

### Upgrade VSC Node Two

1. Backup and prepare VSC node two.

     `metroae-container upgrade ha vsc backup2`

     **Troubleshooting**: If you experience a failure, you can re-execute the command.

2. Deploy VSC node two.

     `metroae-container upgrade ha vsc deploy2`

     VSC node two has been upgraded.

     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy (via scp) the .tim file, bof.cfg, and config.cfg (that were backed up before beginning VSC upgrade), to the VSC. Then reboot the VSC.

3. Run postdeploy for VSC node two.

     `metroae-container upgrade ha vsc postdeploy2`

     Both VSCs are now running the **new** version.

     **Troubleshooting**: If you experience a failure, you can re-execute the command. If it fails a second time, manually copy (via scp) the .tim file, bof.cfg, and config.cfg (that were backed up before beginning VSC upgrade), to the VSC. Then reboot the VSC.

### Upgrade VSTAT

Our example includes a VSTAT node. If your topology does not include one, proceed to *Finalize the Upgrade* below.

1. Run VSTAT health check (optional).

     `metroae-container upgrade ha vstat health -e report_filename=vstat_preupgrade_health.txt`

     You performed health checks during preupgrade preparations, but it is good practice to run the check here as well to make sure the VSD upgrade has not caused any problems.

2. Prepare the VSTAT nodes for upgrade.

     `metroae-container upgrade ha vstat prep`

     Sets up SSH and disables stats collection.

3. Upgrade the VSTAT nodes.

     `metroae-container upgrade ha vstat inplace`

     Performs an in-place upgrade of the VSTAT nodes.

4. Complete VSTAT upgrade and perform post-upgrade checks.

     `metroae-container upgrade ha vstat wrapup`

     Completes the VSTAT upgrade process, renables stats, and performs a series of checks to ensure the VSTAT nodes are healthy.

### Upgrade Stats-out Nodes

1. Upgrade the VSD stats-out nodes

     If the upgrade is a major upgrade, e.g., 6.0.* -> 20.10.* , use the following command to upgrade the VSD stats-out nodes:

     `metroae-container upgrade vsd stats`

     If the upgrade is a patch (in-place), e.g., 20.10.R1 -> 20.10.R4, first make sure that the main VSD cluster has been upgraded/patched. If the upgrade of the main VSD cluster hasn't been done, you can use the following command to patch the main VSD cluster:

     `metroae-container upgrade vsds inplace`

     When you are certain that the main VSD cluster has been patched, you can use the following command to apply the patch to the VSD stat-out nodes:

     `metroae-container upgrade vsd stats inplace`


### Finalize the Upgrade

1. Finalize the settings

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
