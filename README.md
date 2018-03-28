# Nuage Networks MetroAG Automation EnGine (AG)
(4 minute read)

Version: 3.0

MetroAG is an automation engine that deploys and upgrades Nuage Networks components.
After you specify the individual details of your deployment, MetroAG (leveraging Ansible playbooks and roles) sets up the environment as specified. MetroAG can also upgrade, roll-back, and health-check the environment.

## New procedures in version 3.0
If you have used previous versions of MetroAG, the usage of the tool has been greatly improved for usability.  Please note the following overall changes:

* **Deprecation of build_vars.yml.**  There is no longer a single monolithic configuration file for MetroAG.  Configuration is specified through "deployments".  A tool is provided to convert an obsolute build_vars.yml file to a deployment.  See [Customization](Documentation/CUSTOMIZATION.md) for details on deployments.
* **Deprecation of `build`.**  The user no longer needs to issue the `build` playbook.  This will be handled automatically and seamlessly by the MetroAG tool.  MetroAG also tracks changes and will skip steps not required if configuration is unmodified.
* **Schema validation of deployment data.**  All configuration specified in a deployment is automatically validated against json-schema.org schemas.  This ensures that all required fields are set and every field has the correct syntax.  Any error will be found as early as possible and a specific error message will call out the exact problem.
* **Workflows instead of playbooks.**  In order to simplify usage, the concept of `playbook` is being replaced by a `workflow`.  The .yml extension is no longer required.  Thus, issue `vsd_deploy` instead of `vsd_deploy.yml`.  The MetroAG tool is renamed from `metro-ansible` to `metroag`.  It now supports different arguments, including `--list` which displays all supported workflows.
* **Cleanup of repo.**  The MetroAG repository has been cleaned.  Only tools useful for users are present in the root directory.  The internal workings of the tool have been moved to sub-directories like src/.

## Supported Components for Deployment
MetroAG supports deployment of the following components as VMs on the target server. The same target server types are supported as the VSP platform.

Component | KVM (el7)<br>Stand-alone (SA) | KVM (el7)<br>Clustered (HA) | ESXi<br>Stand-alone (SA) | ESXi<br>Clustered (HA)
------- | :---: | :---: | :----: | :---:
VSD (Virtualized Services Directory) | X | X | X | X
VSTAT (Elastic Backend for statistics) | X | X | X | X
VSC (Virtualized Services Controller) | X | X | X | X
VCIN (vCenter Integration Node) | X |  | X |
VNSUTIL<br>(Virtualized Network Services-Utility) | X |  | X |

#### Supported Dataplane components (installed as package/agent):

Component |  KVM <br>(el6, el7,ubuntu 14.04/16.04) | ESXi
--------- | :----: | -------
VRS (Virtual Routing & Switching) | X | (upgrade only)
Libnetwork on VRS nodes  | X |
NSG-V (Network Services Gateway-Virtual) |  X |

#### Provided Auxiliary Services
* DNS/NTP

![topology](Documentation/topology.png)

## Supported Components for Upgrade
MetroAG supports upgrade of the following Nuage VSP components.

Component | KVM (el7)<br> SA | KVM (el7)<br> HA | ESXi<br>SA | ESXi<br>HA
------- | :---: | :---: | :----: | :---:
VSD | X | X | X | X
VSTAT | X | X | X | X
VSC | X | X | X | X
VCIN | X |  | X |

## Main Steps for Using MetroAG

1. [Setup](Documentation/SETUP.md) the MetroAG Host.

2. [Customize](Documentation/CUSTOMIZATION.md) your deployment to match your network topology, and describe your Nuage Networks specifics.

3. [Deploy](Documentation/DEPLOY.md) new components, [upgrade](Documentation/UPGRADE.md) existing components, or run a health check on your system.

4. If things did not work out as expected, [destroy](Documentation/DESTROY.md) or [rollback](Documentation/ROLLBACK.md) your environment.

## Setup
[Setup](Documentation/SETUP.md) is required to prepare the host for running MetroAG.  This includes retrieving the repository, installing prerequisite packages and setting up SSH access.

## Deployment Specification
The settings required by MetroAG are specified in a set of configuration files called a deployment.  These are yaml files stored under a sub-directory of deployments/ under the MetroAG base directory.  Each deployment can describe a different set of components.  During the execution of a workflow the deployment is selected by the sub-directory name.  A deployment named "default" comes pre-packaged with MetroAG with a starter blueprint.  See [Customization](Documentation/CUSTOMIZATION.md) for details.

## MetroAG Workflows
MetroAG workflows are the operations that can be performed against a specified deployment.  All supported workflows can be listed via:

    ./metroag --list

Workflows fall into the following categories:

Workflow | Description |
------------- | ----------- |
Predeploy | prepares infrastructure with necessary packages and makes the component(s) reachable |
Deploy | installs and configures component(s) |
Postdeploy | performs integration checks, and some basic commissioning tests |
Health | checks health for a running component without assuming it was deployed with MetroAG |
Destroy | removes component(s) from the infrastructure |
Upgrade | upgrades component(s) from one release to another |
Rollback | restores component(s) to their previous version (if an upgrade fails) |

The following workflows are examples that combine together several of the above operations into simple to use groups:

* install_everything - Deploys all components specified in a deployment.
* destroy_everything - Destroys all components specified in a deployment.
* nuage_health - Checks the health of all components specified in a deployment.

## MetroAG Execution
After [setup](Documentation/SETUP.md) and specification of a [deployment](Documentation/CUSTOMIZATION.md), MetroAG can perform a workflow using the command-line tool as follows:

    ./metroag <workflow> [deployment] [options]

* `workflow`: Name of the workflow to perform.  Can be listed with --list option.
* `deployment`: Name of the deployment directory containing configuration files.  See [customization](Documentation/CUSTOMIZATION.md)
* `options`: Other options for the tool.  These can be shown using --help.  Also, any options not directed to the metroag tool are passed to Ansible.

The following are some examples:

    ./metroag install_everything

Installs all components described in deployments/default/.

    ./metroag vsd_destroy east_network -vvv

Takes down only the VSD components described by deployments/east_network/vsds.yml.  Additional output will be displayed with 3 levels of verbosity.

## Ansible
MetroAG is based off of the Python-based Ansible operations tool.  The following sections provide more detail of how Ansible is utilized to perform workflows.

### Nomenclature
**Ansible Host**: The host where MetroAG runs. Ansible and the required packages are installed on this host. The Ansible Host must run el7 Linux host, e.g. Cent)S 7.* or RHEL 7.*

**MetroAG User**: The user who runs MetroAG to deploy and upgrade components.

**Target Server**: The hypervisor on which one or more VSP components are installed as VMs. Each deployment may contain more than one Target Server.

### Use of Ansible Playbooks and Roles
**Ansible** provides a method to easily define one or more actions to be performed on one or more computers. These tasks can target the local system Ansible is running from, as well as other systems that Ansible can reach over the network. The Ansible engine has minimal installation requirements. Python, with a few additional libraries, is all that is needed for the core engine. MetroAG includes a few custom Python modules and scripts. Agent software is not required on the hosts to be managed. Communication with target hosts defaults to SSH. Ansible does not require the use of a persistent state engine. Every Ansible run determines state as it goes, and adjusts as necessary given the action requirements. Running Ansible requires only an inventory of potential targets, state directives, either expressed as an ad hoc action, or a series coded in a YAML file, and the credentials necessary to communicate with the target.

**Playbooks** are the language by which Ansible orchestrates, configures, administers and deploys systems. They are YAML-formatted files that collect one or more plays. Plays are one or more tasks linked to the hosts that they are to be executed on.

**Roles** build on the idea of include files and combine them to form clean, reusable abstractions. Roles are ways of automatically loading certain vars files, tasks, and handlers based on a known file structure.

## Documentation
The [Documentation](Documentation/) directory contains the following guides to assist you in successfully working with MetroAG.

File name | Description
--------- | --------
[RELEASE_NOTES.md](Documentation/RELEASE_NOTES.md) | New features, resolved issues and known limitations and issues
[SETUP.md](Documentation/SETUP.md) | Set up your environment by cloning the repo, installing packages and configuring access.
[CUSTOMIZATION.md](Documentation/CUSTOMIZATION.md) | Populate variable files for a deployment and unzip Nuage software.
[BUILD_UPGRADE.md](Documentation/BUILD_UPGRADE.md) | Populate variable files, unzip Nuage software, and build the environment for upgrading.
[DEPLOY.md](Documentation/DEPLOY.md) | Deploy all VSP components or choose components individually.
[DESTROY.md](Documentation/DESTROY.md) | Remove existing deployment(s) and start over.
[UPGRADE.md](Documentation/UPGRADE.md) | Upgrade component(s) from one release to the next.
[ROLLBACK.md](Documentation/ROLLBACK.md) | Restore VSP components to their previous version if an upgrade fails.
[CONTRIBUTING.md](CONTRIBUTING.md) | Submit your code and become a contributor to Nuage MetroAG.
[OPENSTACK.md](Documentation/OPENSTACK.md) | Deploy VSP components in OpenStack (limited support).

## Questions, Feedback, and Contributing
Ask questions and get support via email.
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](CONTRIBUTING.md) to Nuage MetroAG by submitting your own code to the project.

## License
Apache License 2.0
