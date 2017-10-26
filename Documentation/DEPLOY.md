# Deploying Nuage Networks Components with MetroAG
You can execute MetroAG playbooks to perform the following installations:
* [Deploy All Components](#deploy-all-components)  
* [Deploy Individual Modules](#deploy-individual-modules)  
* [Install a Particular Role or Host](#install-a-particular-role-or-host)  
## Prerequisites / Requirements
Before deploying any components, you must have previously [set up your Nuage MetroAG Ansible environment](SETUP.md "link to SETUP documentation") and [customized the environment for your target platform](BUILD.md "link to BUILD documentation"). If you have set up and built your environment successfully you will have
* a `hosts` file in `nuage-metro/`, which acts as the Ansible inventory file
* a dynamically-generated `host_vars/` and `group_vars/` directory containing variables that are used for every component in the system

Make sure you have unzipped the Nuage Networks *.tar.gz files into their proper locations in the directory structure, so MetroAG can find the path of the Nuage components automatically when running `build.yml`. You should have done this in the BUILD phase. See [BUILD.md](BUILD.md) for details.
## Deploy All Components
MetroAG playbooks operate on components as you have defined them in `build_vars.yml`. If you run a playbook for a component not specified in `build_vars.yml`, the playbook skips all tasks associated with that component and runs to completion without error. Thus, if you run the `install_everything` playbook when only VRS appears in `build_vars.yml`, the playbook deploys VRS successfully while ignoring the tasks for the other components not specified. Deploy all specified components with one command as follows:
```
./metro-ansible install_everything.yml
```
Note: `metro-ansible` is a shell script that executes `ansible-playbook` with the proper includes and command line switches. Use `metro-ansible` (instead of `ansible-playbook`) when running any of the playbooks provided herein.
## Deploy Individual Modules
MetroAG offers modular execution models in case you don't want to deploy all components together. See modules below.

Module | Command | Description
 ---|---|---
VCS | `./metro-ansible install_vcs.yml` | Installs components for Virtualized Cloud Services
VNS | `./metro-ansible install_vns.yml` | Installs VNS component on top of a VSP
DNS<br>(experimental) | `./metro-ansible install_dns.yml` | Installs a DNS server based on `named`, with a zone file containing all necessary entries for VSP
OSC (experimental) | `./metro-ansible install_osc.yml` | Installs an RDO OpenStack environment that is integrated against VSD

## Install a Particular Role or Host
MetroAG has a complete library of [playbooks](/playbooks "link to playbooks directory"), which are directly linked to each individual role. You can limit your deployment to a particular role or component, or you can skip steps you are confident need not be repeated. For example, to deploy only the VSD VM-images and get them ready for VSD software installation, run:
```
./metro-ansible vsd_predeploy.yml
```
 To limit your deployment to a particular host, just add `--limit` parameter:
 ```
 ./metro-ansible vsd_predeploy.yml --limit "vsd1.example.com"
```
## Additional Steps for Specific Deployments
### NSGV and Bootstrapping
MetroAG can automatically bootstrap (ZFB) a NSGV when deploying a VNS UTIL VM. To direct MetroAG to generate the ISO file needed for zero factor bootstrapping, perform the following tasks before deploying:

* Customize variables in [`zfb_vars.yml`](/zfb_vars.yml "link to zfb_vars.yml file")
* Specify `bootstrap_method: zfb_metro,` in mynsgvs parameters in [`build_vars.yml`](/build_vars.yml "link to build_vars.yml file")

## Debugging
By default, ansible.cfg tells ansible to log to ./ansible.log.

Ansible supports different levels of verbosity, specified with one of the following command line flags:
-v
-vv
-vvv
-vvvv

More letters means more verbose. The highest level, -vvvv, provides SSH connectivity information.

Running individual playbooks is useful for debugging. For example, `vsd_predeploy.yml`, `vsd_deploy.yml`, and `vsd_postdeploy.yml`.

If you would like to remove an entire deployment, or individual components, and start over, see [DESTROY.md](DESTROY.md "link to DESTROY documentation") for details.

If you would like to reset your variables, see [BUILD.md](BUILD.md "link to BUILD documentation") for details.
## Next Steps
After you have successfully deployed Nuage Networks VSP components, you may want to [upgrade](UPGRADE.md) to a newer version at some point in the future. See [UPGRADE.md](UPGRADE.md) for details.

## Questions, Feedback, and Contributing
Ask questions and get support via email.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](CONTRIBUTING.MD) to Nuage MetroAG by submitting your own code to the project.
