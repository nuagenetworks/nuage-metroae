# Customizing the Components for a Deployment

## Note for users of MetroAG before version 3.0
MetroAG before version 3.0 used the deprecated build_vars.yml configuration.  In the current version, this is replaced with "deployments" as described in this document.  An obsolete build_vars.yml file can be converted to a deployment using the following tool:

```
./convert_build_vars_to_deployment.py <build_vars_file> <deployment_name>
```

## Prerequisites / Requirements
To confirm that the intended deployment is supported by MetroAG, see [README.md](../README.md).

If you have not previously set up your MetroAG Ansible environment, see [SETUP.md](SETUP.md) before proceeding.

## Main Steps

[1. Customize Deployment](#1-customize-deployment)

[2. Unzip Nuage files](#2-unzip-nuage-files)

## 1. Customize Deployment
Based on your network topology and the specific components you plan on deploying, you will configure several files. Setting configuration files correctly ensures that when you subsequently execute workflows they configure components as intended. Precise syntax is crucial.

When a workflow is executed, each configuration file is validated against a data schema which ensures that all required fields are present and in the correct syntax. These schemas are located in the [schemas/](/schemas/) directory. They follow the json-schema.org standard.

You have the option of configuring the default files provided in the deployments/default/ sub-directory, or creating your own sub-directories under the deployments/ directory. You can find examples of configuration files for different deployments in the [examples/](/examples/) directory. Unless a different deployment sub-directory name is specified, the default deployment is used when a workflow is executed. This method allows MetroAG to support many deployments (different configurations) in parallel and the ability to switch between them as required. See below for the supported configuration files that you can specify in a deployments sub-directory.

### `common.yml`
`common.yml` contains the common configuration parameters for the deployment for all components and workflows.  This file is always required for any workflow.

### `credentials.yml`
`credentials.yml` contains user credentials for VSD, VCIN and VSC. Default values are specified; you can modify them as necessary.  This file is optional.

### `upgrade.yml`
`upgrade.yml` contains the configuration parameters for an upgrade workflow.  This file is only required when performing an upgrade.

### `vcenter.yml`
`vcenter.yml` contains the configuration parameters for workflows against a VCenter type deployment.  This file is only required when components are of server type VCenter.

### `zfb_vars.yml`
If you intend on deploying VNS with zero factor bootstrapping, you must customize the variables in this additional file. See [ZFB.md](ZFB.md) for more information.

### `vsds.yml`
`vsds.yml` contains the definition of the VSDs to be operated on in this deployment.  This file is of yaml list type and must contain either 0, 1 or 3 VSD definitions.  If not provided or empty, then no VSDs will be operated on during workflows.

### `vscs.yml`
`vscs.yml` contains the definition of the VSCs to be operated on in this deployment.  This file is of yaml list type and must contain either 0, 1 or 2 VSC definitions.  If not provided or empty, then no VSCs will be operated on during workflows.

### `vstats.yml`
`vstats.yml` contains the definition of the VSTATs (VSD Statistics) to be operated on in this deployment.  This file is of yaml list type and must contain either 0, 1 or 3 VSTAT definitions.  If not provided or empty, then no VSTATs will be operated on during workflows.

## 2. Unzip Nuage Files

Before deploying with MetroAG *for the first time*, ensure that the required unzipped Nuage software files (QCOW2, OVA, and Linux Package files) are available for the components being installed. Use one of the two methods below.

### Automatically
Execute the command:

```
./nuage-unzip <zipped_directory> <unzip_directory>
```

After executing the command, specify the <unzip_directory> in the `common.yml` deployment configuration as the nuage_unzipped_files_dir parameter.

### Manually
Alternatively, you can create the directories under the <nuage_unzipped_files_dir> directory and manually copy the appropriate files to those locations as shown in the example below.

  ```
  <nuage_unzipped_files_dir>/vsd/qcow2/
  <nuage_unzipped_files_dir>/vsd/ova/ (for VMware)
  <nuage_unzipped_files_dir>/vsc/
  <nuage_unzipped_files_dir>/vrs/el7/
  <nuage_unzipped_files_dir>/vrs/u14_04/
  <nuage_unzipped_files_dir>/vrs/ul16_04/
  <nuage_unzipped_files_dir>/vrs/vmware/
  <nuage_unzipped_files_dir>/vrs/hyperv/
  <nuage_unzipped_files_dir>/vstat/
  <nuage_unzipped_files_dir>/vns/nsg/
  <nuage_unzipped_files_dir>/vns/util/
  ```

After executing the command, specify the <nuage_unzipped_files_dir> in the `common.yml` deployment configuration as the nuage_unzipped_files_dir parameter.

## Hosting your deployment files outside of the repo
When you are contributing code, or pulling new versions of Metro quite often, it may make sense to host your variable files in a separate directory outside of `nuage-metro/deployments/`.  A deployment directory in any location can be specified instead of a deployment name when issuing the `./metroag` command.

## Generating example deployment configuration files
A sample of the deployment configuration files are provided in the deployments/default/ directory and also in [examples/](/examples/).  If these are overwritten or deleted or if a "no frills" version of the files with only the minimum required parameters are desired, they can be generated with the following command:

```
./generate_example_from_schema.py --schema <schema_filename> [--no-comments]
```

This will print an example of the deployment file specified by <schema_filename> under the [schemas/](/schemas/) diretory to the screen.  The optional `--no-comments` will print the minimum required parameters (with no documentation).

Example:

```
./generate_example_from_schema.py --schema vsds > deployments/new/vsds.yml
```

Creates an example vsds configuration file under the "new" deployment.

## Next Steps
The next step is to deploy your components. See [DEPLOY.md](DEPLOY.md) for guidance.

## Questions, Feedback, and Contributing
Ask questions and get support via email.
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to Nuage MetroAG by submitting your own code to the project.
