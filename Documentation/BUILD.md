# Customizing the Nuage MetroAG Ansible Environment
The main steps for customizing (modeling) your Nuage MetroAG environment are:  
[1. Customize variables](#1-customize-variables)  
[2. Make files available](#2-make-files-available)  
[3. Execute `build.yml`](#3-execute-build.yml)  
## Prerequisites / Requirements
If you have not previously set up the Nuage MetroAG Ansible environment, see [SETUP.md](SETUP.md) before proceeding.

## 1. Customize Variables
Setting variables correctly ensures that when the automated deployment scripts are run later they configure components as intended. Precise syntax is crucial for success.

`build_vars.yml` contains a dictionary of configuration parameters for each component. You determine which components MetroAG operates on, as well as *how* those components are operated on, by including them or excluding them in the `build_vars.yml` file.

If you are using zero factor bootstrapping on VNS, also refer to [ZFB.md](ZFB.md) for more information.

## 2. Make Files Available

Before installing or upgrading with Nuage MetroAG for the first time, ensure that the required unzipped Nuage software files (QCOW2, OVA, and Linux Package files) are available for the components being installed or upgraded. Use one of the two methods below.
### Make Files Available Automatically
1. Specify the appropriate source and target directories in `build_vars.yml` as follows:
```
 nuage_zipped_files_dir: "<your_path_with_zipped_software>"
 nuage_unzipped_files_dir: <your_path_for_unzipped_software>"
```
2. Execute the following command:
```
./metro-ansible nuage_unzip.yml
```
### Make Files Available Manually
Alternatively, you can manually copy the proper files to their locations as shown below, as applicable.

  ```
  <nuage_unzipped_files_dir/vsd/qcow2/
  <nuage_unzipped_files_dir/vsd/ova/ (for VMware)
  <nuage_unzipped_files_dir/vsc/
  <nuage_unzipped_files_dir/vrs/el7/
  <nuage_unzipped_files_dir/vrs/u14_04/
  <nuage_unzipped_files_dir/vrs/ul16_04/
  <nuage_unzipped_files_dir/vrs/vmware/
  <nuage_unzipped_files_dir/vrs/hyperv/
  <nuage_unzipped_files_dirh/vstat/
  <nuage_unzipped_files_dir/vns/nsg/
  <nuage_unzipped_files_dir/vns/util/
  ```

## 3. Execute build.yml

After you have set up your variables and made the required software files available, automatically populate the Ansible variable files by running the `build` playbook with the following command:

`./metro-ansible build.yml`

Note: `metro-ansible` is a shell script that executes `ansible-playbook` with the proper includes and command line switches. Use `metro-ansible` (instead of `ansible-playbook`) when running any of the playbooks provided herein.

When you execute `build.yml`, it takes the variables that you defined in `build_vars.yml` and performs the following tasks for you.

* creates a `host` file populated with the hostnames of all components in the list. (The host file defines the inventory that the playbooks operate on.)
* populates a `host_vars` subdirectory with the variable files for each component in the list. (These variable files contain configuration information specific to each component in the list.)
* populates a `group_vars` directory
* sets additional variables that configure the overall operation of the playbooks

## Hosting your variable files outside of the repo

When you are contributing code, or pulling new versions of Metro quite often, it may make sense to host your variable files in a separate directory outside of `nuage-metro/`.
Both `nuage-unzip.yml` and `build.yml` support passing the location of this file explicitly as extra variable:

```
./metro-ansible nuage_unzip.yml -e build_vars_file="/path/to/your/build_vars.yml"
./metro-ansible build.yml -e build_vars_file="/path/to/your/build_vars.yml" user_creds_file=/path/to/your/user_creds.yml"
```
## Having Issues? Reset your environment
If you have issues with running the build, you can reset to factory settings and start over.

WARNING: **You may lose your work!** A timestamped backup copy, in the form of `build_vars.yml.<date and time>~` is created (in case you change your mind.) Make sure you have enough storage for it.

Reset the build with the following command:
```
./metro-ansible reset_build.yml
```
Note: `metro-ansible` is a shell script that executes `ansible-playbook` with the proper includes and command line switches. Use `metro-ansible` (instead of `ansible-playbook`) when running any of the playbooks provided herein.

`reset_build.yml` performs the following tasks for you.
* overwrites `build_vars.yml`, `upgrade_vars.yml`, and hosts
* destroys the `host` file
* destroys the `host_vars` directory
* destroys the `group_vars` directory
* resets the variable configuration of Metro to factory settings

## Next Steps
After successfully building your environment you have several options. Refer to the applicable documentation below for instructions.

What Do You Want to Do Next? | Documentation
---- | ----
Deploy Nuage components for the first time | [DEPLOY.md](DEPLOY.md)
Add additional components to an existing deployment | [DEPLOY.md](DEPLOY.md)
Upgrade existing components to a newer version | [UPGRADE.md](UPGRADE.md)
Remove previously deployed component(s) | [DESTROY.md](DESTROY.md)

## Questions, Feedback, and Contributing
Ask questions and get support via email.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](CONTRIBUTING.md) to Nuage MetroAG by submitting your own code to the project.
