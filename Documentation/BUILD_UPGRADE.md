# Readying the MetroAG Environment for Upgrading  
(4 minute read)  

## Prerequisites / Requirements
To confirm that the intended upgrade is supported by MetroAG, see [README.md](../README.md).

If you have not previously set up your MetroAG Ansible environment, see [SETUP.md](SETUP.md) before proceeding.

## Main Steps
[1. Customize variables](#1-customize-variables)  
[2. Unzip Nuage files](#2-unzip-nuage-files)  
[3. Execute `build_upgrade.yml` playbook](#3-execute-build_upgradeyml-playbook)  

## 1. Customize Variables
Setting variables correctly ensures that when you subsequently execute the upgrade playbooks they configure components as intended. Precise syntax is crucial for success. See the [examples directory](../examples) for references. Three variable files are used to build the upgrade environment: `user_creds.yml`, `build_vars.yml`, and `upgrade_vars.yml`.
### `user_creds.yml`
`user_creds.yml` contains user credentials for VSD, VCIN and VSC. Default values are specified; you can modify them as necessary.

### `build_vars.yml`
`build_vars.yml` contains configuration parameters for each component. You determine which components MetroAG operates on, as well as *how* those components are operated on, by including them or excluding them in this file. Notable parameters are described below.

* **Required Nuage Files**
If you intend on automatically unzipping the required Nuage software files as described in step 2 below, ensure that you have specified the following source and target directories in `build_vars.yml`.
```
 nuage_zipped_files_dir: "<your_path_with_zipped_software>"
 nuage_unzipped_files_dir: "<your_path_for_unzipped_software>"
```
* **Operations Lists**
Make sure to change the applicable operations lists from `install` to `upgrade`.

Examples:
```
vsd_operations_list:
  - upgrade
 ```
 ```
 vsc_operations_list:
   - upgrade
 ```
 ```
 vstat_operations_list:
   - upgrade
  ```

* **VSD (myvsds:)**
When you deployed VSD, you may have defined a value for `vmname`. (The hostname is used as a default.) When you upgrade, you must define a value for `upgrade_vmname`. During upgrade, `vmname` is powered down; it is not deleted. It is retained in case a rollback is required. Therefore, the two names must be different.

* **VSC (myvscs:)**
When you upgrade VSC, `upgrade_vmname` is *not* required. The existing VM is not replaced; it is upgraded in place.

* **VSTAT (myvstats:)**
When you deployed VSTAT, you may have defined a value for `vmname`. (The hostname is used as a default.) When you upgrade, you must define a value for `upgrade_vmname`. During upgrade, `vmname` is powered down; it is not deleted. It is retained in case a rollback is required. Therefore, the two names must be different.
### `upgrade_vars.yml`
Notable `upgrade_vars.yml` parameters are described below.  
* **VSC**
Make sure that the <.tim> file is present in the VSC path /vsc/.

* **VSTAT**
Every VSTAT node that is to be upgraded up to and including version 4.0.11 requires a value for `vstat_nfs_server_with_folder`, which is used as a backup and restore location for ES files. The value defined here will be mounted on the VSTAT VM. Prior to upgrading, the server must export the folder. The only backup method supported by MetroAG is NFS. Use the following format: `host_or_ip:/nfs/exported/folder`.

Example: `vstat_nfs_server_with_folder: 135.227.181.233:/tmp/vstat/`

## 2. Unzip Nuage Files
Make the required unzipped Nuage software files (QCOW2, OVA, and Linux Package files) available for the components being upgraded by using one of the two methods below.

### Automatically
Ensure that you have specified the directory paths for zipped and unzipped files. (See step 1 above.)

Execute the command:
```
./metro-ansible nuage_unzip.yml
```
### Manually
Alternatively, you can create the directories under the <nuage_unzipped_files_dir> directory and manually copy the appropriate files to those locations as shown in the example below.
```
<nuage_unzipped_files_dir/vsd/qcow2/
<nuage_unzipped_files_dir/vsd/ova/ (for VMware)
<nuage_unzipped_files_dir/vsd/migration/
<nuage_unzipped_files_dir/vsc/
<nuage_unzipped_files_dir/vrs/el7/
<nuage_unzipped_files_dir/vrs/u14_04/
<nuage_unzipped_files_dir/vrs/ul16_04/
<nuage_unzipped_files_dir/vrs/vmware/
<nuage_unzipped_files_dir/vrs/hyperv/
<nuage_unzipped_files_dirh/vstat/
<nuage_unzipped_files_dir/vstat/backup/
```
**VSC**
`<nuage_unzipped_files_dir/vsc/` - Ensure that the <.tim> file is present in the VSC path.

**VSD**
`<nuage_unzipped_files_dir/vsd/migration/` - As part of VSD upgrade, migration scripts are provided as a separate package (Nuage_VSD-migration-scripts-version-ISO.tar.gz) that performs database backup and declusters the existing VSD cluster. Place this package inside the migration folder of the VSD path as shown above.

**VSTAT**
`<nuage_unzipped_files_dir/vstat/backup/` - As part of VSTAT upgrade, backup scripts are provided as a separate package (Nuage-elastic-backup-version-.tar.gz) that performs backup of existing indices of ElasticSearch node. Place this package inside the backup folder of vstat path as shown above.

## 3. Execute build_upgrade.yml Playbook
Execute the command:
```
./metro-ansible build_upgrade.yml -vvvv
```
The build upgrade playbook generates variables and files needed for upgrade.

## Having Issues? Reset your environment
If you have issues with running the build, you can reset to factory settings and start over.

WARNING: **You may lose your work!** A timestamped backup copy, in the form of `build_vars.yml.<date and time>~` is created (in case you change your mind.) Make sure you have enough storage for it.

Reset the build with the following command:
```
./metro-ansible reset_build.yml
```

The reset build playbook performs the following tasks for you.
* overwrites `build_vars.yml`, `upgrade_vars.yml`, and hosts
* destroys the `host_vars` directory
* destroys the `group_vars` directory
* resets the variable configuration of Metro to factory settings

## Next Steps
After successfully preparing your environment for an upgrade, you have two options:
* upgrade existing components to a newer version. See [UPGRADE.md](UPGRADE.md) for guidance.
* Remove previously deployed component(s). See [DESTROY.md](DESTROY.md) for guidance.
## Questions, Feedback, and Contributing
Ask questions and get support via email.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")  

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to Nuage MetroAG by submitting your own code to the project.
