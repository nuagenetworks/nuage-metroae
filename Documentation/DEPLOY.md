# Deploying Components with MetroÆ

You can execute MetroÆ workflows to perform the following installations:
* [Deploy All Components](#deploy-all-components)
* [Deploy Individual Modules](#deploy-individual-modules)
* [Install a Particular Role or Host](#install-a-particular-role-or-host)

## Prerequisites / Requirements
Before deploying any components, you must have previously [set up your Nuage MetroÆ environment](SETUP.md "link to SETUP documentation") and [customized the environment for your target platform](CUSTOMIZE.md "link to deployment documentation").

Make sure you have unzipped copies of all the Nuage Networks files you are going to need for installation or upgrade. These are generally distributed as `*.tar.gz` files that are downloaded by you from Nokia OLCS. You can unzip these files by using the nuage_unzip shell script `nuage-unzip.sh` which will place the files in subdirectories under the path specified for the `nuage_unzipped_files_dir` variable in `common.yml`. You can also unzip the files manually and copy them to their proper locations by hand. For details of this process, including the subdirectory layout that MetroÆ expects, see [CUSTOMIZE.md](Documentation/CUSTOMIZE.md).


## Use of MetroÆ Tool
MetroÆ can perform a workflow using the command-line tool as follows:

    metroae <workflow> [deployment] [options]

* `workflow`: Name of the workflow to perform.  Supported workflows can be listed with --list option.
* `deployment`: Name of the deployment directory containing configuration files.  See [CUSTOMIZE.md](Documentation/CUSTOMIZE.md)
* `options`: Other options for the tool.  These can be shown using --help.  Also, any options not directed to the metroae tool are passed to Ansible.

The following are some examples:

    metroae install_everything

Installs all components described in deployments/default/.

    metroae vsd_destroy east_network -vvv

Takes down only the VSD components described by deployments/east_network/vsds.yml.  Additional output will be displayed with 3 levels of verbosity.

## Deploy All Components
MetroÆ workflows operate on components as you have defined them in your deployment. If you run a workflow for a component not specified, the workflow skips all tasks associated with that component and runs to completion without error. Thus, if you run the `install_everything` workflow when only VRS configuration is present, the workflow deploys VRS successfully while ignoring the tasks for the other components not specified. Deploy all specified components with one command as follows:

```
metroae install_everything
```
Note: `metroae` is a shell script that executes `ansible-playbook` with the proper includes and command line switches. Use `metroae` (instead of `ansible-playbook`) when running any of the workflows provided herein.

## Deploy Individual Modules

MetroÆ offers modular execution models in case you don't want to deploy all components together. See modules below.

Module | Command | Description
 ---|---|---
VCS | `metroae install_vcs` | Installs components for Virtualized Cloud Services
VNS | `metroae install_vns` | Installs VNS component on top of a VSP
DNS<br>(experimental) | `metroae install_dns` | Installs a DNS server based on `named`, with a zone file containing all necessary entries for VSP
OSC (experimental) | `metroae install_osc` | Installs an RDO OpenStack environment that is integrated against VSD

## Install a Particular Role or Host
MetroÆ has a complete library of [workflows](/src/playbooks "link to workflows directory"), which are directly linked to each individual role. You can limit your deployment to a particular role or component, or you can skip steps you are confident need not be repeated. For example, to deploy only the VSD VM-images and get them ready for VSD software installation, run:
```
metroae vsd_predeploy
```

 To limit your deployment to a particular host, just add `--limit` parameter:

 ```
 metroae vsd_predeploy --limit "vsd1.example.com"
```
VSD predeploy can take a long time. If you are **vCenter user** you may want to monitor progress via the vCenter console.

Note: If you have an issue with a VM and would like to reinstall it, you must destroy it before you replace it. Otherwise, the install will find the first one still running and skip the new install.

## Copy QCOW2 Files before Deployment

When installing or upgrading in a KVM environment, MetroÆ copies the QCOW2 image files to the target file server during the predeploy phase. As an option, you can pre-position the qcow2 files for all the components by running copy_qcow2_files. This gives the ability to copy the required images files first and then run install or upgrade later.

When QCOW2 files are pre-positioned, you must add a command-line variable, 'skip_copy_qcow2', to indicate that copying QCOW2 files should be skipped. Otherwise, the QCOW2 files will be copied again. An extra-vars 'skip_copy_qcow2' needs to be passed on the command line during the deployment phase to skip copying of the image files again. For example, to pre-position the QCOW2 images, run:

```
metroae copy_qcow2_files
```

Then, to skip the image copy during the install:

```
metroae install_everything.yml --extra-vars skip_copy_qcow2=True
```


## Debugging

By default, ansible.cfg tells ansible to log to ./ansible.log.

Ansible supports different levels of verbosity, specified with one of the following command line flags:
-v
-vv
-vvv
-vvvv

More letters means more verbose. The highest level, -vvvv, provides SSH connectivity information.

Running individual workflows is useful for debugging. For example, `vsd_predeploy`, `vsd_deploy`, and `vsd_postdeploy`.

If you would like to remove an entire deployment, or individual components, and start over, see [DESTROY.md](DESTROY.md "link to DESTROY documentation") for details.

## Next Steps

After you have successfully deployed Nuage Networks VSP components, you may want to upgrade to a newer version at some point in the future. See [UPGRADE_SA.md](UPGRADE_SA.md) for standalone deployments and [UPGRADE_HA.md](UPGRADE_HA.md) for clustered deployments.

## Questions, Feedback, and Contributing  
Ask questions and get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroÆ site](https://devops.nuagenetworks.net/).  
You may also contact us directly.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.
