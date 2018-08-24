# Customizing for your Topology

## Prerequisites / Requirements

To confirm that your components are supported by Metro Automation Engine, see [README.md](../README.md).

If you have not previously set up your Metro Automation Engine Ansible environment, see [SETUP.md](SETUP.md) before proceeding.

## Main Steps

[1. Customize variables](#1-customize-variables)  
[2. Unzip Nuage files](#2-unzip-nuage-files)  

## 1. Customize Variables

Setting variables correctly ensures that when playbooks run they configure components as intended. Precise syntax is crucial for success. See the [examples directory](/examples/) for references. *Up to* three variable files are used to build the environment: `user_creds.yml`, `build_vars.yml` and `zfb_vars.yml`.

### `user_creds.yml`
`user_creds.yml` contains user credentials for VSD, VCIN and VSC. Default values are specified; you can modify them as necessary.

### `build_vars.yml`
`build_vars.yml` contains configuration parameters for each component. You determine which components Metro Automation Engine operates on, as well as *how* those components are operated on, by including them or excluding them in this file.

If this is your first time deploying or upgrading with Metro Automation Engine, and you intend on automatically unzipping the required Nuage software files as described in step 2 below, ensure that you have specified the following source and target directories in `build_vars.yml`.

```
 nuage_zipped_files_dir: "<your_path_with_zipped_software>"
 nuage_unzipped_files_dir: "<your_path_for_unzipped_software>"
```

### `zfb_vars.yml`
If you intend on deploying VNS with zero factor bootstrapping, you must customize the variables in this additional file. See [ZFB.md](ZFB.md) for more information.

## 2. Unzip Nuage Files

Before executing with Metro Automation Engine *for the first time*, ensure that the required unzipped Nuage software files (QCOW2, OVA, and Linux Package files) are available for the components being installed. Use one of the two methods below.
### Automatically
Ensure that you have specified the directory paths for zipped and unzipped files in `build_vars.yml`. (See step 1 above.)

Execute the command:
```
./metro-ansible nuage_unzip.yml
```

### Manually
Alternatively, you can create the directories under the <nuage_unzipped_files_dir> directory and manually copy the appropriate files to those locations as shown in the example below.

  ```
  <nuage_unzipped_files_dir>/vsd/qcow2/
  <nuage_unzipped_files_dir>/vsd/ova/ (for VMware)
  <nuage_unzipped_files_dir>/vsd/migration/
  <nuage_unzipped_files_dir>/vsc/
  <nuage_unzipped_files_dir>/vrs/el7/
  <nuage_unzipped_files_dir>/vrs/u14_04/
  <nuage_unzipped_files_dir>/vrs/ul16_04/
  <nuage_unzipped_files_dir>/vrs/vmware/
  <nuage_unzipped_files_dir>/vrs/hyperv/
  <nuage_unzipped_files_dir>/vstat/
  <nuage_unzipped_files_dir>/vstat/backup/
  <nuage_unzipped_files_dir>/vns/nsg/
  <nuage_unzipped_files_dir>/vns/util/
  ```

## Hosting your variable files outside of the repo

When you are contributing code, or pulling new versions of Metro quite often, it may make sense to host your variable files in a separate directory outside of `nuage-metro/`.
The metro-ansible command supports passing the location of this file explicitly as extra variable:

```
./metro-ansible nuage_unzip -e build_vars_file="/path/to/your/build_vars.yml"
./metro-ansible install_everything -e build_vars_file="/path/to/your/build_vars.yml" -e "user_creds_file=/path/to/your/user_creds.yml"
```

## Having Issues? Reset your environment

If you have issues with the contents of your user data files, you can reset to factory settings and start over.

WARNING: **You may lose your work!** A timestamped backup copy, in the form of `<data_file_name>.yml.<date and time>~` is created (in case you change your mind.) Make sure you have enough storage for it.

Execute the command:

```
./metro-ansible reset_build
```

## Next Steps

After you've set up your environment and customized for your topology, you have several options:
* deploy new components. See [DEPLOY.md](DEPLOY.md) for guidance.
* upgrade existing components to a newer version. See [UPGRADE.md](UPGRADE.md) for guidance.
* remove previously deployed components(s). See [DESTROY.md](DESTROY.md) for guidance.

## Questions, Feedback, and Contributing

Ask questions and get support via email.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")  

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to Nuage Metro Automation Engine by submitting your own code to the project.
