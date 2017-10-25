# Nuage Networks MetroAG Automation EnGine (AG)
## Overview
MetroAG is an automation engine used for deploying and upgrading Nuage Networks components. 
After specifing the individual details for your target platform, MetroAG (leveraging Ansible playbooks and roles) will setup the environment as specified. Alternatively, the environment could be upgraded, rolled-back, health-checked, etc.

## Getting started

To get started, you would typically go through these steps:

1. [Setup](Documentation/SETUP.md) your Nuage MetroAG Ansible environment on the host on which MetroAG is to be run.

2. [Customize](Documentation/BUILD.md) variable files so they match your network topology and desribe your NuageNetworks deployment specifics.

3. [Deploy](Documentation/DEPLOY.md) the various components (if they have not previously been deployed), perform an [Upgrade](Documentation/UPGRADE.md), or run a [Health check](Documentation/HEALTH.md) on your system.

4. If things did notwork out as expected, [Destroy](Documentation/DESTROY.md) or [Rollback](Documentation/ROLLBACK.md) your environment.

## Supported Nuage VSP Components for deployment
The following Nuage VSP components are supported for deployment using MetroAG. These are all deployed as VMs on a given _target server_.


Component | Stand-alone (SA) | Clustered (HA) | KVM (el7) | ESXi 
------- | ---------------- | -------------- | --- | --- 
VSD (Virtualized Services Directory) | X | X | X | X
VSTAT (Elastic Backend for statistics)  | X | X | X | X
VSC (Virtualized Services Controller) | X | X | X | X
VCIN (vCenter Integration Node) | X |  | X | X
VNSUTIL (Virtualized Network Services - Utility) VM | X |  | X | X

Dataplane coponents are as follows (installed as package/agent):

Component |  KVM <br>(el6, el7 or ubuntu 14.04/16.04) | ESXi
--------- | ---- | -------
VRS (Virtual Routing & Switching) | X | (upgrade only)
Libnetwork on VRS nodes  | X | 
NSG-V (Network Services Gateway-Virtual) |  X |

Auxiliary services are also provided:
* DNS/NTP

![topology](topology.png)

## Supported Nuage VSP Components for upgrade

MetroAG currently also provides upgrade support for

Component | KVM (el7) | ESXi
------- | --- | --- 
VSD | X | X
VCIN | X | X
VSC |X | X

## Use of Ansible Playbooks and Roles  
**Ansible** provides a method to easily define one or more actions to be performed on one or more computers. These tasks can target the local system Ansible is running from, as well as other systems that Ansible can reach over the network. The Ansible engine has minimal installation requirements. Python, with a few additional libraries, is all that is needed for the core engine. MetroAG includes a few custom Python modules and scripts. Agent software is not required on the hosts to be managed. Communication with target hosts defaults to SSH. Ansible does not require the use of a persistent state engine. Every Ansible run determines state as it goes, and adjusts as necessary given the action requirements. Running Ansible requires only an inventory of potential targets, state directives, either expressed as an ad hoc action, or a series coded in a YAML file, and the credentials necessary to communicate with the target.

**Playbooks** are the language by which Ansible orchestrates, configures, administers and deploys systems. They are YAML-formatted files that collect one or more plays. Plays are one or more tasks linked to the hosts that they are to be executed on. 

**Roles** build on the idea of include files and combine them to form clean, reusable abstractions. Roles are ways of automatically loading certain vars files, tasks, and handlers based on a known file structure.

### MetroAG Playbooks and Roles
MetroAG playbooks and roles fall into the following categories:   

Playbook/Role | Description |
------------- | ----------- |
Predeploy | prepares infrastructure with necessary packages and makes the component(s) reachable |
Deploy | installs and configures component(s) |
Postdeploy | performs integration checks, and some basic commissioning tests |
Health | checks health for a running component without assuming it was deployed with MetroAG |
Destroy | removes component(s) from the infrastructure |
Upgrade | upgrades component(s) from one release to another |
Rollback | restores component(s) to their previous version (if an upgrade fails) |

## Documentation
The [Documentation](Documentation/) directory contains the following guides to assist you in successfully working with MetroAG.

File name | Description
--------- | --------
[RELEASE_NOTES.md](Documentation/RELEASE_NOTES.md) | New features, resolved issues and known limitations and issues
[SETUP.md](Documentation/SETUP.md) | Set up your environment by cloning the repo, installing packages and configuring access.
[BUILD.md](Documentation/BUILD.md) | Populate variables for your specific environment, unzip Nuage software, and execute the build.
[DEPLOY.md](Documentation/DEPLOY.md) | Deploy all VSP components or choose components individually.
[DESTROY.md](Documentation/DESTROY.md) | Remove existing deployment(s) and start over.
[UPGRADE.md](Documentation/UPGRADE.md) | Upgrade component(s) from one release to the next.
[ROLLBACK.md](Documentation/ROLLBACK.md) | Restore VSP components to their previous version if an upgrade fails.
[CONTRIBUTING.md](Documentation/CONTRIBUTING.md) | Submit your code and become a contributor to Nuage MetroAG.
[OPENSTACK.md](Documentation/OPENSTACK.md) | Deploy VSP components in OpenStack (limited support).


## Questions, Feedback and Contributing
Ask questions and get support on the [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project") mailing list.   

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.
 
You may also [contribute](Documentation/CONTRIBUTING.md) to Nuage MetroAG by submitting your own code to the project.
 
## License
Apache License 2.0
