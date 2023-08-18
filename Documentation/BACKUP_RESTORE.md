# Backing up and Restoring Components with MetroAE

MetroAE can create and manage backups of selected components.  It is also capable of restoring those components from existing backups.

## Currently Supported Components for Backup and Restore

* VSD
* VSC

## Backup Procedure

Ensure that all components you wish to have backed up are specified under your deployment.  See [CUSTOMIZE.md](CUSTOMIZE.md) for details about specifying components in a deployment.  All backups are stored under a backup root directory on the MetroAE deployment host.  The backup root directory is specified by the `backup_directory_root` field in the `common.yml` deployment file.  Absent this configuration, the `nuage_backup_root` field of the `upgrade.yml` deployment file is used.  If neither of these is specified, a backup directory is created off of the `nuage_unzipped_files_dir` directory of the `common.yml` deployment file.

To perform a backup of all supported components issue:

    metroae-container backup

To perform a backup of a specific component issue:

    metroae-container backup vsds

Substitute the component name to be backed up if different than `vsds`.

MetroAE will first health check the component to ensure it is operating properly before backup.  It will then produce a timestamped backup file under the backup root directory.  The number of backups to be stored can be managed by MetroAE as well.  Specifying `max_num_stored_backups` in the `common.yml` deployment file will instruct MetroAE to clean excess backup sets exceeding the limit.  The backups to be deleted are always the oldest ones by the timestampped path name.  Specifying the default of -1 to `max_num_stored_backups` causes all backups to be saved with no limit.

*Note*: As part of the procedure for upgrade of the VSD, a backup is automatically created.  This backup follows the same rules for backup root directory and cleanup as described above.

## Restore Procedure

Ensure that all components you wish to have restored are specified under your deployment.  See [CUSTOMIZE.md](CUSTOMIZE.md) for details about specifying components in a deployment.  The backup set directory to be restored must be present under the backup root directory and specified as the `backup_to_restore` field in `common.yml`.  Components to be restored should not already exist and thus should be destroyed if already running.  See [DESTROY.md](DESTROY.md) for more information on this.

To restore all supported components issue:

    metroae-container restore

To restore a specific component issue:

    metroae-container restore vsds

Substitute the component name to be backed up if different than `vsds`.

Restore can alternatively be performed with each step separately using:

    metroae-container restore vsds predeploy
    metroae-container restore vsds deploy
    metroae-container restore vsds postdeploy

## TLS Configuration on VSC During Restore

If `xmpp_tls` or `openflow_tls` is enabled within the `common.yml` deployment file during restore, any TLS configuration within the restored VSC configuration will be removed and readded.  This occurs because the TLS certificates are reobtained from the VSD immediately after the VSC backup config is reapplied during restore.  Any backup TLS configuration cannot be applied due to missing the original TLS certificates.  Note that changes are made in a temporary location and the original backup remains untouched.  When `xmpp_tls` and `openflow_tls` are both disabled, no modifications will be made during the restore. 

## Questions, Feedback, and Contributing  
Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).  
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:devops@nuagenetworks.net "send email to nuage-metro project").
 
Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
