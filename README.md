# Nuage Networks Metro Automation Engine (MetroÆ)
(4 minute read)

Version: 3.3.0

MetroÆ is an automation engine that deploys and upgrades Nuage Networks components. You specify the individual details of your target platform, then let MetroÆ install, upgrade, destroy, or health-check the environment for you.

## Important Notes

You can now run `python run_wizard.py` to let MetroÆ help you setup your server and create or edit a deployment. The wizard will ask you questions about what you'd like to do and then create the proper files on disk. run_wizard.py is most useful when you are working with a clone of the nuage-metro repo. It can be used to generate deployments that can be used with the Docker container version of MetroÆ, but thos edeployments would need to be copied manually from the nuage-metro repo clone to the container's metroae_data directory.

Please see [RELEASE_NOTES.md](Documentation/RELEASE_NOTES.md) for all the details about what has changed or been added in this release.

All MetroÆ operations, including Docker container management, use a command `metroae` for consistent usage and syntax. Please see [DOCKER.md](Documentation/DOCKER.md) for details on configuration and use of the container version of MetroÆ.

## Supported Components for Deployment
MetroÆ supports deployment of the following components as VMs on the target server. These are the same target server types that are supported on the VSP platform.

Component | KVM (el7)<br>Stand-alone (SA) | KVM (el7)<br>Clustered (HA) | ESXi<br>Stand-alone (SA) | ESXi<br>Clustered (HA)
------- | :---: | :---: | :----: | :---:
VSD (Virtualized Services Directory) | X | X | X | X
VSTAT (Elasticsearch stats-in) | X | X | X | X
VSC (Virtualized Services Controller) | X | X | X | X
VCIN (vCenter Integration Node) | X |  | X |
VNSUTIL<br>(Virtualized Network Services-Utility) | X |  | X |

#### Supported Dataplane components (installed as package/agent):

Component |  KVM <br>(el6, el7,ubuntu 14.04/16.04) | ESXi
--------- | :----: | -------
VRS (Virtual Routing & Switching) | X | (upgrade only)
Libnetwork on VRS nodes  | X |

#### Required Auxiliary Services
* DNS/NTP

## Typical Nuage Topology
![topology](Documentation/topology.png)

## Supported Components for Upgrade
MetroÆ supports upgrade of the following Nuage VSP components.

Component | KVM (el7)<br> SA | KVM (el7)<br> HA | ESXi<br>SA | ESXi<br>HA
------- | :---: | :---: | :----: | :---:
VSD | X | X | X | X
VSTAT (stats-in) | X | X | X | X
VSC | X | X | X | X
VCIN | X |  | X |

## Main Steps for Using MetroÆ

1. [Setup](Documentation/SETUP.md) the MetroÆ host. Setup prepares the host for running MetroÆ, including retrieving the repository, installing prerequisite packages and setting up SSH access. You also have the option of installing MetroÆ in a container, and then working with it via CLI or the GUI.

2. [Customize](Documentation/CUSTOMIZE.md) your deployment to match your network topology, and describe your Nuage Networks specifics.

3. [Deploy](Documentation/DEPLOY.md) new components, upgrade a [standalone](Documentation/UPGRADE_SA.md) or [clustered](Documentation/UPGRADE_HA.md) deployment, or run a health check on your system.

4. If things did not work out as expected, [destroy](Documentation/DESTROY.md) your environment and redeploy.

## MetroÆ Workflows
MetroÆ workflows are the operations that can be performed against a specified deployment.  All supported workflows can be listed via:

    metroae --list

Workflows fall into the following categories:

Workflow | Operation Description |
------------- | ----------- |
Predeploy | prepares infrastructure with necessary packages and makes the component(s) reachable |
Deploy | installs and configures component(s) |
Postdeploy | performs integration checks, and some basic commissioning tests |
Health | checks health for a running component without assuming it was deployed with MetroÆ |
Destroy | removes component(s) from the infrastructure |
Upgrade | upgrades component(s) from one release to another |

The following workflows are examples that combine together several of the above operations into simple to use groups:

* install_everything - Deploys all components specified in a deployment.
* destroy_everything - Destroys all components specified in a deployment.
* nuage_health - Checks the health of all components specified in a deployment.

## Python-based Ansible Operations Tool
MetroÆ is based off of the Python-based Ansible operations tool.

**Ansible** provides a method to easily define one or more actions to be performed on one or more computers. These tasks can target the local system Ansible is running from, as well as other systems that Ansible can reach over the network. The Ansible engine has minimal installation requirements. Python, with a few additional libraries, is all that is needed for the core engine. MetroÆ includes a few custom Python modules and scripts. Agent software is not required on the hosts to be managed. Communication with target hosts defaults to SSH. Ansible does not require the use of a persistent state engine. Every Ansible run determines state as it goes, and adjusts as necessary given the action requirements. Running Ansible requires only an inventory of potential targets, state directives, either expressed as an ad hoc action, or a series coded in a YAML file, and the credentials necessary to communicate with the target.

**Playbooks** are the language by which Ansible orchestrates, configures, administers and deploys systems. They are YAML-formatted files that collect one or more plays. Plays are one or more tasks linked to the hosts that they are to be executed on.

**Roles** build on the idea of include files and combine them to form clean, reusable abstractions. Roles are ways of automatically loading certain vars files, tasks, and handlers based on a known file structure.

## Nomenclature
**Ansible Host**: The host where MetroÆ runs. Ansible and the required packages are installed on this host. The Ansible Host must run el7 Linux host, e.g. CentOS 7.* or RHEL 7.*.

**MetroÆ User**: The user who runs MetroÆ to deploy and upgrade components.

**Target Server**: The hypervisor on which one or more VSP components are installed as VMs. Each deployment may contain more than one Target Server.

## Documentation
The [Documentation](Documentation/) directory contains the following guides to assist you in successfully working with MetroÆ. The current documentation covers using MetroÆ CLI only.

File name | Description
--------- | --------
[RELEASE_NOTES.md](Documentation/RELEASE_NOTES.md) | New features, resolved issues and known limitations and issues
[GETTING_STARTED.md](Documentation/GETTING_STARTED.md) | MetroÆ Quick Start Guide
[SETUP.md](Documentation/SETUP.md) | Set up your environment by cloning the repo, installing packages and configuring access.
[CUSTOMIZE.md](Documentation/CUSTOMIZE.md) | Populate variable files for a deployment and unzip Nuage software.
[DEPLOY.md](Documentation/DEPLOY.md) | Deploy all VSP components or choose components individually.
[DESTROY.md](Documentation/DESTROY.md) | Remove existing deployment(s) and start over.
[UPGRADE_SA.md](Documentation/UPGRADE_SA.md) | Upgrade component(s) from one release to the next in a standalone environment.
[UPGRADE_HA.md](Documentation/UPGRADE_HA.md) | Upgrade component(s) from one release to the next in a clustered environment.
[VAULT_ENCRYPT.md](Documentation/VAULT_ENCRYPT.md) | Safeguard sensitive data
[DOCKER.md](Documentation/DOCKER.md) | Installing and using MetroÆ Docker container

## Questions, Feedback, and Contributing
Ask questions and get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroÆ site](https://devops.nuagenetworks.net/).
You may also contact us directly.
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.

## License
[LICENSE.md](LICENSE.md)
