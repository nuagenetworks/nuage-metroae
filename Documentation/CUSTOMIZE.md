# Customizing Components for a Deployment
The steps below apply when you choose to work via CLI. A similar set of steps, facilitated by the GUI, is also available if you choose to deploy MetroÆ via Docker Container. If you choose to work via the GUI you can access it by pointing your browser at the address and port that was specified during the container setup. The default address is https://metroaehostname:5001.
## Note for users of MetroÆ before version 3.0
MetroÆ before version 3.0 used the now deprecated build_vars.yml configuration.  In the current version, build_vars.yml is replaced with *deployments* as described in this document.  You can convert an obsolete build_vars.yml file to a deployment using the following tool:

```
./convert_build_vars_to_deployment.py <build_vars_file> <deployment_name>
```

Deprecation Notice: The convert_build_vars_to_deployment tool is not actively updated for new features and will be removed in MetroÆ v3.4.0. Users of this tool should either edit deployment files directly or modify their process to take advantage of the jinja2 templates available in src/deployment_templates to auto-generate deployment files.

## Prerequisites / Requirements
If you have not already set up your MetroÆ Host environment, see [SETUP.md](SETUP.md) before proceeding.  

## Customize Deployment
Based on your network topology and the specific components you plan on deploying, you will configure several files. Setting configuration files correctly ensures that when you subsequently execute workflows they configure components as intended. Precise syntax is crucial.

When a workflow is executed, each configuration file is validated against a data schema which ensures that all required fields are present and in the correct syntax. These schemas are located in the [schemas/](/schemas/) directory. They follow the [json-schema.org standard](https://json-schema.org).

You have the option of configuring the default files provided in the deployments/default/ sub-directory or creating your own sub-directories under the deployments/ directory. You can find examples of configuration files for different deployments in the [examples/](/examples/) directory. Unless you specify a different deployment sub-directory name, the default deployment is used when a workflow is executed. This method allows MetroÆ to support many deployments (different configurations) in parallel and the ability to switch between them as required. See below for the supported configuration files that you can specify in a deployments sub-directory.

### `common.yml`
`common.yml` contains the common configuration parameters for the deployment that are used for all components and workflows.  This file is always required for any workflow.

#### Notes for `common.yml`
- `nuage_unzipped_files_dir` is a required parameter that points to the location of the image and package files used for Install and Upgrade workflows. When running MetroÆ in a container, this parameter should *not* begin with a '/' and be set equal to the relative path from the images path you configured when you installed the container. For example, if you set the images path for the container to `/home/username/images` and you will unzip the files you are going to use into `/home/username/images/6.0.1`, set `nuage_unzipped_files_dir` to `6.0.1`. MetroÆ will concatenate the two paths to access your files. If, however, you are operating without the container and, instead, cloned the nuage-metro repo to your disk, set `nuage_unzipped_files_dir` to the full, absolute path to the images directory, `/home/username/images/6.0.1` in the example, above.
- For best performance, `ntp_server_list` should include the same servers that the target servers will be using. This will help to ensure NTP synchronization.

### `credentials.yml`
`credentials.yml` contains user credentials for command-line access to individual components, e.g. VSD, authentication parameters for HTTP and hypervisor access, and the passwords for internal VSD services. All of the credentials in this file are optional. MetroÆ will use default parameters when these are not specified. This file does not require modification if you are not using non-default credentials.

### `nsgvs.yml`
`nsgvs.yml` contains the definition of the NSGvs to be operated on in this deployment. This file should be present in your deployment only if you are specifying NSGvs. If not provided, no NSGvs will be operated on. This file is of yaml list type and may contain as many NSGv definitions as required.

#### Notes for `nsgvs.yml`
ZFB support is included in the nsgv schema and supporting files. In the beta release of MetroÆ 3, however, ZFB is not supported.

### `upgrade.yml`
`upgrade.yml` contains the configuration parameters for an upgrade workflow. This file is only required when performing an upgrade.

### `vcins.yml`
`vcins.yml` contains the definition of the VCINs to be operated on in this deployment. This file should be present in your deployment only if you are specifying VCINs. If not provided, no VCINs will be operated on. This file is of yaml list type and may contain as many VCIN definitions as required.

### `vnsutils.yml`
`vnsutils.yml` contains the definition of the VNSUTILs to be operated on in this deployment. This file should be present in your deployment only if you are specifying VNSUTILs. If not provided, no VNSUTILs will be operated on. This file is of yaml list type and may contain as many VNSUTILs definitions as you require, though one is usually sufficient.

### `vrss.yml`
`vrss.yml` contains the definition of the VRSs to be operated on in this deployment. This file should be present in your deployment only if you are specifying VRSs. If not provided, no VRSs will be operated on. This file is of yaml list type and may contain as many VRS defintions as you require.

### `vscs.yml`
`vscs.yml` contains the definition of the VSCs to be operated on in this deployment. This file should be present in your deployment only if you are specifying VSCs. If not provided, no VSCs will be operated on. This file is of yaml list type and may contain as many VSC definitions as you require.

### `vsds.yml`
`vsds.yml` contains the definition of the VSDs to be operated on in this deployment. This file should be present in your deployment only if you are specifying VSDs. If not provided, no VSDs will be operated on. This file is of yaml list type and must contain either 0, 1 or 3 VSD definitions.

### `vstats.yml`
`vstats.yml` contains the definition of the VSTATs (VSD Statistics) to be operated on in this deployment. This file should be present in your deployment only if you are specifying VSTATs. If not provided, no VSTATs will be operated on. This file is of yaml list type and must contain either 0, 1 or 3 VSTAT definitions.

#### Notes for VSD security enhancements
### `vsds.yml`
- `ca_certificate_path` is an optional parameter that points to the location of the certificate of the signing authority.
- `certificate_path` is an optional parameter that points to the location of the certificate pem file for the vsd.
- `intermediate_certificate_path` is an optional parameter that points to the location of the chain certificate.
- `failed_login_attempts` is an optional parameter to set the number of failed login attempts.
- `failed_login_lockout_time` is an optional parameter that set the lockout time after reaching the max number of failed login attempts.
- `adavanced_api_access_logging` is an optional parameter to enable adding custom header to access log.
- `tls_version` is an optional parameter to set the minimum TLS version to use.

### `vscs.yml`
- `ca_certificate_path` is an optional parameter that points to the location of the certificate of the signing authority.
- `certificate_path` is an optional parameter that points to the location of the certificate pem file for the vsc.
- `private_key_path` is an optional parameter that points to the location of the certificate private key pem file for the vsc.
- `ejjaberd_id` is an optional parameter that defines the ejjaberd username used to when creating the certificate.

### `vrss.yml`
- `ca_certificate_path` is an optional parameter that points to the location of the certificate of the signing authority.
- `certificate_path` is an optional parameter that points to the location of the certificate pem file for the vrs.
- `private_key_path` is an optional parameter that points to the location of the certificate private key pem file for the vrs.


### Unsupported Components/Operations
The following components/operations are not supported in the beta release.
* dns
* gmv
* mesos
* nsgv bootstrap (install is supported)
* stcv
* vsr
* vrs-vm
* osc-integration
* AWS-based VSTAT upgrade
* upgrade of VRS through VCIN

### Operating using the Default Deployment
The Default deployment is provided as a starting place for your workflows. It is located in a subdirectory named `Default` within the Deployments directory. You can operate MetroÆ by simply editing the contents of the Default deployment. Follow these steps:
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
When you are contributing code, or pulling new versions of MetroÆ quite often, it may make sense to host your variable files in a separate directory outside of `nuage-metro/deployments/`.  A deployment directory in any location can be specified instead of a deployment name when issuing the `metroae` command.

## Generating example deployment configuration files
A sample of the deployment configuration files are provided in the deployments/default/ directory and also in [examples/](/examples/).  If these are overwritten or deleted or if a "no frills" version of the files with only the minimum required parameters are desired, they can be generated with the following command:

```
./generate_example_from_schema.py --schema <schema_filename> [--no-comments]
```

This will print an example of the deployment file specified by <schema_filename> under the [schemas/](/schemas/) directory to the screen.  The optional `--no-comments` will print the minimum required parameters (with no documentation).

Example:

```
./generate_example_from_schema.py --schema vsds > deployments/new/vsds.yml
```

Creates an example vsds configuration file under the "new" deployment.

## Next Steps
The next step is to deploy your components. See [DEPLOY.md](DEPLOY.md) for guidance.

## Questions, Feedback, and Contributing
Ask questions and get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroÆ site](https://devops.nuagenetworks.net/).  
You may also contact us directly.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.
