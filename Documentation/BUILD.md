# Readying the MetroAG Environment for Deploying
## Prerequisites / Requirements
To confirm that the intended deployment is supported by MetroAG, see [README.md](README.md).

If you have not previously set up your MetroAG Ansible environment, see [SETUP.md](SETUP.md) before proceeding.

## Main Steps
[1. Customize variables](#1-customize-variables)  
[2. Unzip Nuage files](#2-unzip-nuage-files)  
[3. Execute `build.yml` playbook](#3-execute-buildyml-playbook)  

## 1. Customize Variables
Setting variables correctly ensures that when you subsequently execute the deploy playbook(s) they configure components as intended. Precise syntax is crucial for success. See the [examples directory](/examples/) for references. *Up to* three variable files are used to build the deployment environment: `user_creds.yml`, `build_vars.yml` and `zfb_vars.yml`.

### `user_creds.yml`
`user_creds.yml` contains user credentials for VSD, VCIN and VSC. Default values are specified; you can modify them as necessary.

### `build_vars.yml`
`build_vars.yml` contains configuration parameters for each component. You determine which components MetroAG operates on, as well as *how* those components are operated on, by including them or excluding them in this file.

If this is your first time deploying with MetroAG, and you intend on automatically unzipping the required Nuage software files as described in step 2 below, ensure that you have specified the following source and target directories in `build_vars.yml`.

```
 nuage_zipped_files_dir: "<your_path_with_zipped_software>"
 nuage_unzipped_files_dir: "<your_path_for_unzipped_software>"
```

### `zfb_vars.yml`
If you intend on deploying VNS with zero factor bootstrapping, you must customize the variables in this additional file. See [ZFB.md](ZFB.MD) for more information.

## 2. Unzip Nuage Files

Before deploying with MetroAG *for the first time*, ensure that the required unzipped Nuage software files (QCOW2, OVA, and Linux Package files) are available for the components being installed. Use one of the two methods below.
### Automatically
Ensure that you have specified the source and target directories in `build_vars.yml`. (See step 1 above.)

Execute the command:
```
./metro-ansible nuage_unzip.yml
```

### Manually
Alternatively, you can create the directories under the <nuage_unzipped_files_dir> directory and manually copy the appropriate files to those locations as shown in the example below.

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

## 3. Execute build.yml Playbook
Execute the command:

`./metro-ansible build.yml`

The build playbook takes the values from the variable files and performs the following tasks for you.

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

Execute the command:
```
./metro-ansible reset_build.yml
```

The reset build playbook performs the following tasks for you.
* overwrites `build_vars.yml`, `upgrade_vars.yml`, and hosts
* destroys the `host_vars` directory
* destroys the `group_vars` directory
* resets the variable configuration of Metro to factory settings

## Next Steps
The next step is to deploy your components. See [DEPLOY.md](DEPLOY.md) for guidance.

## Questions, Feedback, and Contributing
Ask questions and get support via email.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")  
  
Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](CONTRIBUTING.MD) to Nuage MetroAG by submitting your own code to the project.
