# Deploying Components with MetroAE

You can execute MetroAE workflows to perform the following installations:
* [Deploy All Components](#deploy-all-components)
* [Deploy Individual Modules](#deploy-individual-modules)
* [Install a Particular Role or Host](#install-a-particular-role-or-host)
* [Copy QCOW2 files](#copy-qcow2-files-before-deployment)
* [Deploy Standby Cluster](#deploy-the-standby-clusters)
* [Debugging](#debugging)

## Prerequisites / Requirements
Before deploying any components, you must have previously [set up your Nuage MetroAE environment](SETUP.md "link to SETUP documentation") and [customized the environment for your target platform](CUSTOMIZE.md "link to deployment documentation").

Make sure you have unzipped copies of all the Nuage Networks files you are going to need for installation or upgrade. These are generally distributed as `*.tar.gz` files that are downloaded by you from Nokia OLCS/ALED. There are a few ways you can use to unzip:

* If you are running MetroAE via a clone of the nuage-metro repo, you can unzip these files by using the nuage-unzip shell script `nuage-unzip.sh` which will place the files in subdirectories under the path specified for the `nuage_unzipped_files_dir` variable in `common.yml`.
* If you are running MetroAE via the MetroAE container, you can unzip these files using the metroae command. During the setup, you were promoted for the location of an data directory on the host. This data directory is mounted in the container as `/data`. Therefore, for using the unzip action, you must 1) copy your tar.gz files to a directory under the directory you specified at setup time and 2) you must specify a container-relative path on the unzip command line. For example, if you specified the data directory as `/tmp`, setup created the directory `/data/metroae_data` on your host and mounted that same directory as `/data` in the container. Assuming you copied your tar.gz files to `/tmp/metroae_data/6.0.1` on the docker host, your unzip command line would be as follows: `metroae tools unzip images /data/6.0.1/ /data/6.0.1`.
* You can also unzip the files manually and copy them to their proper locations by hand. For details of this process, including the subdirectory layout that MetroAE expects, see [SETUP.md](SETUP.md). 


## Use of MetroAE Command Line
MetroAE can perform a workflow using the command-line tool as follows:

    metroae <workflow> <componment> [deployment] [options]

* `workflow`: Name of the workflow to perform, e.g. 'install' or 'upgrade'.  Supported workflows can be listed with --list option.
* `component`: Name of the component to apply the workflow to, e.g. 'vsds', 'vscs', 'everything', etc.
* `deployment`: Name of the deployment directory containing configuration files.  See [CUSTOMIZE.md](CUSTOMIZE.md)
* `options`: Other options for the tool.  These can be shown using --help.  Also, any options not directed to the metroae tool are passed to Ansible.

The following are some examples:

    metroae install everything

Installs all components described in deployments/default/.

    metroae destroy vsds east_network

Takes down only the VSD components described by deployments/east_network/vsds.yml.  Additional output will be displayed with 3 levels of verbosity.

## Deploy All Components
MetroAE workflows operate on components as you have defined them in your deployment. If you run a workflow for a component not specified, the workflow skips all tasks associated with that component and runs to completion without error. Thus, if you run the `install everything` workflow when only VRS configuration is present, the workflow deploys VRS successfully while ignoring the tasks for the other components not specified. Deploy all specified components with one command as follows:

```
metroae install everything
```
Note: `metroae` is a shell script that executes `ansible-playbook` with the proper includes and command line switches. Use `metroae` (instead of `ansible-playbook`) when running any of the workflows provided herein.

## Deploy Individual Modules

MetroAE offers modular execution models in case you don't want to deploy all components together. See modules below.

Module | Command | Description
 ---|---|---
VCS | `metroae install vsds` | Installs VSD components
VNS | `metroae install vscs` | Installs VSC components

## Install a Particular Role or Host
MetroAE has a complete library of [workflows](/src/playbooks "link to workflows directory"), which are directly linked to each individual role. You can limit your deployment to a particular role or component, or you can skip steps you are confident need not be repeated. For example, to deploy only the VSD VM-images and get them ready for VSD software installation, run:
```
metroae install vsds predeploy
```

 To limit your deployment to a particular host, just add `--limit` parameter:

 ```
 metroae install vsds predeploy --limit "vsd1.example.com"
```
VSD predeploy can take a long time. If you are **vCenter user** you may want to monitor progress via the vCenter console.

Note: If you have an issue with a VM and would like to reinstall it, you must destroy it before you replace it. Otherwise, the install will find the first one still running and skip the new install.

## Copy QCOW2 Files before Deployment

When installing or upgrading in a KVM environment, MetroAE copies the QCOW2 image files to the target file server during the predeploy phase. As an option, you can pre-position the qcow2 files for all the components by running copy_qcow2_files. This gives the ability to copy the required images files first and then run install or upgrade later.

When QCOW2 files are pre-positioned, you must add a command-line variable, 'skip_copy_images', to indicate that copying QCOW2 files should be skipped. Otherwise, the QCOW2 files will be copied again. An extra-vars 'skip_copy_images' needs to be passed on the command line during the deployment phase to skip copying of the image files again. For example, to pre-position the QCOW2 images, run:

```
metroae tools copy qcow
```

Then, to skip the image copy during the install:

```
metroae install everything --extra-vars skip_copy_images=True
```

## Deploy the Standby Clusters

MetroAE can be used to bring up the Standby VSD and VSTAT(ES) cluster in situations where the active has already been deployed. This can be done using the following commands. For VSD Standby deploy
```
metroae install vsds standby predeploy
metroae install vsds standby deploy
```
For Standby VSTATs(ES)
```
metroae install vstats standby predeploy
metroae install vstats standby deploy
```

## Debugging

By default, ansible.cfg tells ansible to log to ./ansible.log.

Ansible supports different levels of verbosity, specified with one of the following command line flags:
-v
-vv
-vvv
-vvvv

More letters means more verbose, usually for debugging. The highest level, -vvvv, provides SSH connectivity information.

Running individual workflows is also useful for debugging. For example, `vsd_predeploy`, `vsd_deploy`, and `vsd_postdeploy`.

If you would like to remove an entire deployment, or individual components, and start over, see [DESTROY.md](DESTROY.md "link to DESTROY documentation") for details.

## Next Steps

After you have successfully deployed Nuage Networks VSP components, you may want to upgrade to a newer version at some point in the future. See [UPGRADE_SA.md](UPGRADE_SA.md) for standalone deployments and [UPGRADE_HA.md](UPGRADE_HA.md) for clustered deployments.

## Questions, Feedback, and Contributing  
Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).  
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project").
 
Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
