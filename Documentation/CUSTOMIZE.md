# Customizing Components for a Deployment

## Prerequisites / Requirements

If you have not already set up your MetroAE Host environment, see [SETUP.md](SETUP.md) before proceeding.

## What is a Deployment?

Deployments are component configuration sets.  You can have one or more deployments in your setup.
The files within each deployment directory describe all of the components you want to install or upgrade.

If you issue:

    ./metroae-container install everything

The files under nuage-metroae/deployments/default will be used to do an install.

If you issue:

    ./metroae-container install everything mydeployment

The files under `nuage-metroae/deployments/mydeployment` will be used to do an install.  This allows for different sets of component definitions for various projects.

The deployment files and the image files must be located within the git clone folder. The docker container will mount the git clone folder inside the container and will not have access to files outside of that location. All file paths must be defined as relative to the git clone folder and never using absolute paths

You can also do:
```
./metroae-container install everything deployment_spreadsheet_name.xlsx
```

to run the install everything playbook using the deployment information present in the specified Excel spreadsheet. More details about Excel deployments can be found in the `Customize Your Own Deployment` section below.

Each time you issue MetroaÆ, the inventory will be completely rebuilt from the deployment name specified.  This will overwrite any previous inventory, so it will reflect exactly what is configured in the deployment that was specified.

## Customize Your Own Deployment

You can customize the deployment files for your workflows using any of the following methods:

* Edit the files in the `default` deployment
* Edit the files in a new deployment directory that you have created
* Run `run_wizard.py` to let MetroAE create or edit your deployment
* Create your deployment using the MetroAE spreadsheet (CSV file)
* Create your deployment using an Excel spreadsheet (XLSX file)

Based on your network topology and the specific components you plan on deploying, you will configure several files. Setting deployment files correctly ensures that when you subsequently execute workflows they configure components as intended. Precise syntax is crucial.

When a workflow is executed, each deployment file is validated against a data schema which ensures that all required fields are present and in the correct syntax. These schemas are located in the [schemas/](/schemas/) directory. They follow the [json-schema.org standard](https://json-schema.org).

You have the option of configuring the default deployment files provided in the deployments/default/ sub-directory or creating your own sub-directories under the deployments/ directory. You can find examples of deployment files for different deployments in the [examples/](../examples/) directory. Unless you specify a different deployment sub-directory name, the default deployment is used when a workflow is executed. This method allows MetroAE to support many deployments (different configurations) in parallel and the ability to switch between them as required. See below for the supported deployment files that you can specify in a deployments sub-directory.

Note that you can edit the deployment files manually at any time. MetroAE comes with its own wizard for automating the creation and editing of deployment files when you are working with a clone of the nuage-metroae repo. To start the wizard:
```
python run_wizard.py
```
You can use the wizard to setup your MetroAE environment, if you wish. Or you can skip the setup step and go directly to the creation and editing of your deployment.

You can also use the MetroAE spreadsheet to create your deployment. You can find the MetroAE CSV template in `deployment_spreadsheet_template.csv`. When you finish customizing the spreadsheet, save it to a CSV file of your own naming. Then you can either convert the CSV directly to a deployment using this syntax:
```
convert_csv_to_deployment.py deployment_spreadsheet_name.csv your_deployment_name
```
or you can let `metroae-container` handle the conversion for you by  specifying the name of the CSV file instead of the name of your deployment::
```
metroae-container deployment_spreadsheet_name.csv
```
This will create or update a deployment with the same name as the CSV file - without the extension.

MetroAE also supports deployment files filled out in an Excel (.xlsx) spreadsheet. You can find examples under the [examples/excel](../examples/excel) directory. Similar to a csv-based deployment, you have multiple options for creating a deployment from an Excel spreadsheet. You can run the converter script directly:
```
convert_excel_to_deployment.py deployment_spreadsheet_name.xlsx your_deployment_name
```
or you can use `metroae-container` do the conversion for you by running build, like this:
```
metroae-container build deployment_spreadsheet_name.xlsx
```

For Excel deployments, all playbooks (aside from `nuage_unzip` and `reset_build`) invoke the build step and can replace build in the command above.

The deployment files that can be configured using the wizard, spreadsheet (csv or xlsx), or edited manually are listed, below.

### `common.yml`

`common.yml` contains the common configuration parameters for the deployment that are used for all components and workflows.  This file is always required for any workflow.

#### Notes for `common.yml`

* `nuage_unzipped_files_dir` is a required parameter that points to the location of the binary image and package files used for Install and Upgrade workflows. We require that you have obtained those files from Nuage/Nokia online customer support prior to running MetroAE. When running MetroAE in a container, this parameter should *not* begin with a '/' and be set equal to the relative path from the images path you configured when you installed the container. For example, if you set the images path for the container to `/home/username/images` and you will unzip the files you are going to use into `/home/username/images/6.0.1`, set `nuage_unzipped_files_dir` to `6.0.1`. MetroAE will concatenate the two paths to access your files. If, however, you are operating without the container and, instead, cloned the nuage-metroae repo to your disk, set `nuage_unzipped_files_dir` to the full, absolute path to the images directory, `/home/username/images/6.0.1` in the example, above.
* For best performance, `ntp_server_list` should include the same servers that the target servers will be using. This will help to ensure NTP synchronization.

### `credentials.yml`

`credentials.yml` contains user credentials for command-line access to individual components, e.g. VSD, authentication parameters for HTTP and hypervisor access, and the passwords for internal VSD services. All of the credentials in this file are optional. MetroAE will use default parameters when these are not specified. This file does not require modification if you are not using non-default credentials.

### `nsgvs.yml`

`nsgvs.yml` contains the definition of the NSGvs to be operated on in this deployment. This file should be present in your deployment only if you are specifying NSGvs. If not provided, no NSGvs will be operated on. This file is of yaml list type and may contain as many NSGv definitions as required.

#### Notes for `nsgvs.yml`

ZFB support is included in the nsgv schema and supporting files. In the beta release of MetroAE 3, however, ZFB is not supported.

### `upgrade.yml`

`upgrade.yml` contains the configuration parameters for an upgrade workflow. This file is only required when performing an upgrade.

### `vcins.yml`

`vcins.yml` contains the definition of the VCINs to be operated on in this deployment. This file should be present in your deployment only if you are specifying VCINs. If not provided, no VCINs will be operated on. This file is of yaml list type and may contain as many VCIN definitions as required.

### `vnsutils.yml`

`vnsutils.yml` contains the definition of the VNSUTILs to be operated on in this deployment. This file should be present in your deployment only if you are specifying VNSUTILs. If not provided, no VNSUTILs will be operated on. This file is of yaml list type and may contain as many VNSUTILs definitions as you require, though one is usually sufficient.

### `nuhs.yml`

`nuhs.yml` contains the definition of the NUHs to be operated on in this deployment. This file should be present in your deployment only if you are specifying NUHs. If not provided, no NUHs will be operated on. This file is of yaml list type and may contain as many NUHs definitions as you require, though one is usually sufficient.

### `webfilters.yml`
`webfilters.yml` contains the definition of the Webfilters to be operated on in this deployment. This file should be present in your deployment only if you are specifying Webfilters. If not provided, no Webfilters will be operated on. This file is of yaml list type and may contain as many Webfilters definitions as you require, though one is usually sufficient.

### `vrss.yml`

`vrss.yml` contains the definition of the VRSs to be operated on in this deployment. This file should be present in your deployment only if you are specifying VRSs. If not provided, no VRSs will be operated on. This file is of yaml list type and may contain as many VRS defintions as you require.

### `vscs.yml`

`vscs.yml` contains the definition of the VSCs to be operated on in this deployment. This file should be present in your deployment only if you are specifying VSCs. If not provided, no VSCs will be operated on. This file is of yaml list type and may contain as many VSC definitions as you require.

### `vsds.yml`

`vsds.yml` contains the definition of the VSDs to be operated on in this deployment. This file should be present in your deployment only if you are specifying VSDs. If not provided, no VSDs will be operated on. This file is of yaml list type and must contain either 0, 1, 3, or 6 VSD definitions. 1 VSD is for stand-alone VSD operation. 3 VSDs are for a single cluster operation. 6 VSDs are defined for active-standby, geo-redundant operation.

#### Notes on `vsds.yml` for active-standby, geo-redundant deployment and upgrade

When installing or upgrading an active-standby, geo-redundant cluster, all 6 VSDs must be defined in the `vsds.yml` file in your deployment. The first 3 VSDs are assumed to be `active` and the second 3 VSDs are assumed to be `standby`.

### `vstats.yml`

`vstats.yml` contains the definition of the VSTATs (VSD Statistics) to be operated on in this deployment. This file should be present in your deployment only if you are specifying VSTATs. If not provided, no VSTATs will be operated on. This file is of yaml list type. If it contains exactly 3 VSTAT definitions, a cluster installation or upgrade will be executed. Any other number of VSTAT definitions will result in 1 or more stand-alone VSTATs being installed or upgraded.

## VSD RTT Performance Testing

You can use MetroAE to verify that your VSD setup has sufficient RTT performance. By default, the RTT performance test will run at the beginning of the VSD deploy step, prior to installing the VSD software. The parameters that you can use to control the operation of the test are available in 'common.yml':

* `vsd_run_cluster_rtt_test` When true, run RTT tests between VSDs in a cluster or standby/active cluster, else skip the test
* `vsd_ignore_errors_rtt_test` When true, continue MetroAE execution upon error and do not validate the RTT between VSDs in a cluster is less than max RTT, else stop MetroAE execution upon error
* `vsd_max_cluster_rtt_msec` Maximum RTT in milliseconds between VSDs in a cluster
* `vsd_max_active_standby_rtt_msec` Maximum RTT in milliseconds between Active and Standby VSDs

In addition to the automatic execution that takes place in the VSD deploy step, you can run the VSD disk performance test at any time using `metroae-container vsd test rtt`.

## VSD Disk Performance Testing

You can use MetroAE to verify that your VSD setup has sufficient disk performance (IOPS). By default, the disk performance test will run at the beginning of the VSD deploy step, prior to installing the VSD software. The parameters that you can use to control the operation of the test are available in 'common.yml':

* `vsd_run_disk_performance_test` Run the VSD disk performance test when true, else skip the test
* `vsd_disk_performance_test_total_file_size` Sets the total size of created files for VSD disk performance test. For a valid measurement, the total file size must be larger than VSD RAM to minimize the effects of caching.
* `vsd_disk_performance_test_minimum_threshold` Sets the minimum value for VSD disk performance test in IOPS
* `vsd_disk_performance_test_max_time` Sets the duration of the VSD disk performance test in seconds
* `vsd_ignore_disk_performance_test_errors` When true, continue MetroAE execution upon error and ignore the results of the VSD disk performance test, else stop MetroAE execution upon error

You can skip the test, specify the total size of all the files used in the test, and modify the minimum threshold requirement in IOPS for the test. Note that to minimize the effects of file system caching, the total file size must exceed the total RAM on the VSD. If MetroAE finds that the test is enabled and the disk performance is below the threshold, an error will occur and installation will stop. The default values that are provided for the test are recommended for best VSD performance in most cases. Your specific situation may require different values or to skip the test entirely.

In addition to the automatic execution that takes place in the VSD deploy step, you can run the VSD disk performance test at any time using `metroae-container vsd test disk`.

## Enabling post-installation security features

You can use MetroAE to enable optional post-installation security features to 'harden' the installation. Your deployment contains a number of optional variables that can be used to accomplish this. These variables are described, below. For more detail, please see the Nuage VSP Install Guide.

### `vsds.yml`

* `ca_certificate_path` is an optional parameter that points to the location of the certificate of the signing authority.
* `certificate_path` is an optional parameter that points to the location of the certificate pem file for the vsd.
* `intermediate_certificate_path` is an optional parameter that points to the location of the chain certificate.
* `failed_login_attempts` is an optional parameter to set the number of failed login attempts.
* `failed_login_lockout_time` is an optional parameter that set the lockout time after reaching the max number of failed login attempts.
* `advanced_api_access_logging` is an optional parameter to enable adding custom header to access log.
* `tls_version` is an optional parameter to set the minimum TLS version to use.

### `vscs.yml`

* `ca_certificate_path` is an optional parameter that points to the location of the certificate of the signing authority.
* `certificate_path` is an optional parameter that points to the location of the certificate pem file for the vsc.
* `private_key_path` is an optional parameter that points to the location of the certificate private key pem file for the vsc.
* `ejabberd_id` is an optional parameter that defines the ejabberd username used to when creating the certificate.

### `vrss.yml`

* `ca_certificate_path` is an optional parameter that points to the location of the certificate of the signing authority.
* `certificate_path` is an optional parameter that points to the location of the certificate pem file for the vrs.
* `private_key_path` is an optional parameter that points to the location of the certificate private key pem file for the vrs.

### `vnsutils`

Currently post install security hardening is not supported for VNSUTILs(proxy) using MetroAE. If using custom certificates, they need to copied into /opt/proxy/config/keys and supervisord needs to be restarted.

### Operating using the Default Deployment

The Default deployment is provided as a starting place for your workflows. It is located in a subdirectory named `Default` within the Deployments directory. You can operate MetroAE by simply editing the contents of the Default deployment. Follow these steps:

1. Edit the files for the components you will operate on that already exist in the Default subdirectory
2. Remove the files for the components you will *not* operate on that already exist in the Default subdirectory
3. To add components to the default directory, or replace ones you previously deleted, copy and then edit files found in the examples directory.

### Adding a new Deployment

To create a new deployment:

1. Create a new subdirectory under deployments.
2. Copy the contents of an existing deployment subdirectory, e.g. deployments/default, to the new subdirectory.
3. Edit the files in the new subdirectory.
4. If you'd like to add components that are not included, you can copy a *blank* file from the examples directory.

## Hosting your deployment files outside of the repo

When you are contributing code, or pulling new versions of MetroAE quite often, it may make sense to host your variable files in a separate directory outside of `nuage-metroae/deployments/`.  A deployment directory in any location can be specified instead of a deployment name when issuing the `metroae` command.

## Generating example deployment configuration files

A sample of the deployment configuration files are provided in the deployments/default/ directory and also in [examples/](../examples/).  If these are overwritten or deleted or if a "no frills" version of the files with only the minimum required parameters are desired, they can be generated with the following command:

```
metroae-container tools generate example --schema <schema_filename> [--no-comments]
```

This will print an example of the deployment file specified by <schema_filename> under the [schemas/](/schemas/) directory to the screen.  The optional `--no-comments` will print the minimum required parameters (with no documentation).

Example:

```
metroae-container tools generate example --schema vsds > deployments/new/vsds.yml
```

Creates an example vsds configuration file under the "new" deployment.

## Running MetroAE using a Proxy VM

MetroAE version 3.4.0 onwards supports using a proxy VM for deployment of VSC, VSD and VSTATS(ES). In this configuration, the host on which MetroAE is run on, does not have direct access to the VSD, VSC and VSTATS. In such a case, a proxy VM can be set between the host and individual components which has access to all the components. To operate in such a manner, user can edit their `deployments\<deployment_name>\common.yml` parameters to indicate the proper `ssh_proxy_username` and `ssh_proxy_host` and then run the MetroAE commands as usual.

## Next Steps

The next step is to deploy your components. See [DEPLOY.md](DEPLOY.md) for guidance.

## Questions, Feedback, and Contributing

Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).  
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:devops@nuagenetworks.net "send email to nuage-metro project").

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metroae/issues "nuage-metroae issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
