# Deploying Nuage Networks Components with Metro Automation Engine

You can execute MetroAG playbooks to perform the following installations:
* [Deploy All Components](#deploy-all-components)
* [Deploy Individual Modules](#deploy-individual-modules)
* [Install a Particular Role or Host](#install-a-particular-role-or-host)

## Prerequisites / Requirements
Before deploying any components, you must have previously [set up your Nuage MetroAG Ansible environment](SETUP.md "link to SETUP documentation") and [customized the environment for your target platform](CUSTOMIZATION.md "link to deployment documentation").

<<<<<<< HEAD
<<<<<<< HEAD
Make sure you have unzipped the Nuage Networks *.tar.gz files into their proper locations in the directory structure, so MetroAG can find the path of the Nuage components automatically. You should have done this in the customization phase. See [CUSTOMIZATION.md](CUSTOMIZATION.md) for details.

=======
Before deploying any components, you must have previously [set up your Nuage Metro Automation Engine Ansible environment](SETUP.md "link to SETUP documentation") and [customized your environment](CUSTOMIZE.md "link to CUSTOMIZE documentation").

Make sure you have unzipped copies of all the Nuage Networks files you are going to need for installation or upgrade. These are generally distributed as `*.tar.gz` files that are downloaded by you from Nokia OLCS. You can unzip these files by using the nuage_unzip playbook which will place the files in subdirectories under the path specified for the `nuage_unzipped_files_dir` variable in `build_vars.yml`. You can also unzip the files manually and copy them to their proper locations by hand. For details of this process, including the subdirectory layout that Metro Automation Engine expects, see [customizing your environment](CUSTOMIZE.md "link to CUSTOMIZE documentation").
>>>>>>> dev
=======
Make sure you have unzipped copies of all the Nuage Networks files you are going to need for installation or upgrade. These are generally distributed as `*.tar.gz` files that are downloaded by you from Nokia OLCS. You can unzip these files by using the nuage_unzip playbook which will place the files in subdirectories under the path specified for the `nuage_unzipped_files_dir` variable in `common.yml`. You can also unzip the files manually and copy them to their proper locations by hand. For details of this process, including the subdirectory layout that Metro Automation Engine expects.
>>>>>>> croxley_merge

## Use of MetroAG Tool
MetroAG can perform a workflow using the command-line tool as follows:

    ./metroag <workflow> [deployment] [options]

* `workflow`: Name of the workflow to perform.  Supported workflows can be listed with --list option.
* `deployment`: Name of the deployment directory containing configuration files.  See [customization](Documentation/CUSTOMIZATION.md)
* `options`: Other options for the tool.  These can be shown using --help.  Also, any options not directed to the metroag tool are passed to Ansible.

The following are some examples:

    ./metroag install_everything

Installs all components described in deployments/default/.

    ./metroag vsd_destroy east_network -vvv

Takes down only the VSD components described by deployments/east_network/vsds.yml.  Additional output will be displayed with 3 levels of verbosity.

## Deploy All Components
MetroAG workflows operate on components as you have defined them in your deployment. If you run a workflow for a component not specified, the workflow skips all tasks associated with that component and runs to completion without error. Thus, if you run the `install_everything` workflow when only VRS configuration is present, the workflow deploys VRS successfully while ignoring the tasks for the other components not specified. Deploy all specified components with one command as follows:

```
./metroag install_everything
```
Note: `metroag` is a shell script that executes `ansible-playbook` with the proper includes and command line switches. Use `metroag` (instead of `ansible-playbook`) when running any of the workflows provided herein.

## Deploy Individual Modules

Metro Automation Engine offers modular execution models in case you don't want to deploy all components together. See modules below.

Module | Command | Description
 ---|---|---
VCS | `./metroag install_vcs` | Installs components for Virtualized Cloud Services
VNS | `./metroag install_vns` | Installs VNS component on top of a VSP
DNS<br>(experimental) | `./metroag install_dns` | Installs a DNS server based on `named`, with a zone file containing all necessary entries for VSP
OSC (experimental) | `./metroag install_osc` | Installs an RDO OpenStack environment that is integrated against VSD

## Install a Particular Role or Host
MetroAG has a complete library of [workflows](/src/playbooks "link to workflows directory"), which are directly linked to each individual role. You can limit your deployment to a particular role or component, or you can skip steps you are confident need not be repeated. For example, to deploy only the VSD VM-images and get them ready for VSD software installation, run:
```
./metroag vsd_predeploy
```

 To limit your deployment to a particular host, just add `--limit` parameter:

 ```
 ./metroag vsd_predeploy --limit "vsd1.example.com"
```

## Additional Steps for Specific Deployments

### NSGV and Bootstrapping

Metro Automation Engine can automatically bootstrap (ZFB) a NSGV when deploying a VNS UTIL VM. To direct Metro Automation Engine to generate the ISO file needed for zero factor bootstrapping, perform the following tasks before deploying:

* Customize variables in [`zfb_vars.yml`](deployments/default/zfb_vars.yml "link to zfb_vars.yml file")
* Specify `bootstrap_method: zfb_metro,` in nsgvs parameters in [`nsgvs.yml`](deployments/default/nsgvs.yml "link to nsgvs.yml file")

## Copy QCOW2 Files before Deployment

When installing or upgrading in a KVM environment, the Metro Automation Engine will copy the QCOW2 image files to the target file server during the predeploy phase. As an option, the playbook copy_qcow2_files can be used to pre-position the qcow2 files for all the components. This playbook gives the ability to copy the required images files first and then run install or upgrade later.

When QCOW2 files are pre-positioned, you must add a command-line variable, 'skip_copy_qcow2', to indicate that copying QCOW2 files should be skipped. Otherwise, the QCOW2 files will be copied again. An extra-vars 'skip_copy_qcow2' needs to be passed on the command line during the deployment phase to skip copying of the image files again. For example, to pre-position the QCOW2 images, run:

```
./metro-ansible copy_qcow2_files
```

Then, to skip the image copy during the install:

```
./metro-ansible install_everything.yml --extra-vars skip_copy_qcow2=True
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

After you have successfully deployed Nuage Networks VSP components, you may want to [upgrade](UPGRADE.md) to a newer version at some point in the future. See [UPGRADE_SA.md](UPGRADE_SA.md) for standalone deployments and [UPGRADE_HA.md](UPGRADE_HA.md) for clustered deployments.

## Questions, Feedback, and Contributing

Ask questions and get support via email.
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to Nuage Metro Automation Engine by submitting your own code to the project.
