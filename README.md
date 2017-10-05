# Overview on NuageNetworks Metro Automation EnGine(AG)

MetroAG is a set of Ansible playbooks that can be used to automatically deploy and (in some cases) upgrade NuageNetworks VCS/VNS and closely related components. Following components are supported

1. Virtualized Services Directory (VSD): clustered or stand-alone
2. Virtualized Services Controller (VSC): 1 or more
3. Virtual Routing & Switching (VRS) on existing nodes 1 or more
4. Libnetwork on VRS nodes to add docker network support
5. ElasticSearch (VSTAT): 1 or more
6. Virtualized Network Services - Util VM: 1 or more
7. Networks Services Gateway - Virtual: 1
8. vCenter Integration Node (VCIN): 1
9. DNS/NTP (1)


All the above components (except for VRS) are deployed as VMs. Supported hypervisor types are EL7, EL6, ESXi, Ubuntu14.04, Ubuntu 16.04.

As a user of MetroAG, you will mostly interact with `metro-ansible` which is a shell script that executes ansible-playbook with the proper includes and command line switches. 


## What's new

The [MetroAG Release Notes](Documentation/RELEASE_NOTES.md) contain a full list of all changes that went into the last major version(s).
Some of the highlights are:

- New upgrade procedure for VSD, VSC and VSTAT (ElasticSearch). See [UPGRADE.md](Documentation/Upgrade.md) for details.
- Added support for upgrade and rollback of VCIN.
- Added syntax checker for build_vars.yml.
- Deploy STCv on VMware.
- Sample Docker file to build Metro container.

# Getting Started...

Metro can be used to facilitate mulitple parts of Nuage lifecycle. A typical worfklow would be:
1. Setup your environment for use with MetroAG - See [SETUP.md](Documentation/Setup.md)
2. Build (or model) your environment - See [BUILD.md](Documentation/BUILD.md)
3. Deploy NuageNetworks software in your environemnt - See [DEPLOY.md](Documentation/DEPLOY.md)
4. Upgrade the NuageNetworks software - See [UPGRADE.md](Documentation/UPGRADE.md)
5. Destroy the environment - See [DESTROY.md](Documentation/DESTROY.md)


## More Advanced Use cases

The file [HOWTO.md](Documentation/HOWTO.md) has been provided. It contains a few procedures for doing some more-complex deployments using Metro, e.g. deploying VRS to both Debian and RedHat family compute nodes.


## Playbook Organization

All playbooks, whether installation or destruction, must be executed using the `metro-ansible` script.
There are a few playbooks at top-level directory such as `install_everything.yml` and `destroy_everything.yml` which are provided as a convenience.
More modular playbooks are stored in `playbooks` folder that can be run stand-alone. This is especially useful for debuuging, or skipping steps that you are confident are not needed or don't have to bre repeated. 
It also allows the user to execute only a very specific role on a given component without having to construct its own playbook.

When browsing through this repository, you will see each component has up to 5 corresponding roles:

* `predeploy` : prepares infrastructure with necessary packages, finishing up by making the element reachable.
* `deploy` : installs and configures the element
* `postdeploy` : performs integration checks, and some basic commissioning tests
* `destroy` : removes the element from the infrastructure
* `health` : checks health for a running element without assuming it was deployed with Metro.

Every supported element must have at least a deploy playbook.

# Developing and Contributing to Metro


The latest stable code is found in the `master` branch. The `dev` branch is for ongoing development. The stability of the `dev` branch is not guaranteed.

If you want to contribute back, you must create your own branch or fork, push your changes to that, and create a pull request to the `dev` branch. All pull requests against the `master` branch will be rejected. Sorry. All pull requests should include tests for new functionality. See [CONTRIBUTING.md](Documentation/CONTRIBUTING.md) for more details.


# Metro Ansible Role Categories

## Core Ansible Roles

These are Ansible roles that are fully tested and supported.

- build-upgrade
- build
- gvm-destroy
- gvm-predeploy
- nsgv-destroy
- nsgv-predeploy
- nuage-unzip
- reset-build
- set-upgrade-flag
- validate-build-vars
- vcin-deploy
- vcin-destroy
- vcin-health
- vcin-predeploy
- vns-deploy
- vns-postdeploy-vsc
- vns-postdeploy-vsd
- vnsutil-deploy
- vnsutil-destroy
- vnsutil-postdeploy
- vnsutil-predeploy
- vrs-deploy
- vrs-destroy
- vrs-health
- vrs-postdeploy
- vrs-predeploy
- vsc-backup
- vsc-deploy
- vsc-destroy
- vsc-health
- vsc-postdeploy
- vsc-predeploy
- vsc-preupgrade
- vsc-rollback
- vsc-upgrade-deploy
- vsc-upgrade-postdeploy
- vsc-upgrade
- vsd-cluster-start
- vsd-dbbackup
- vsd-decouple
- vsd-deploy
- vsd-destroy
- vsd-ha-upgrade-block-access
- vsd-health
- vsd-license
- vsd-predeploy
- vsd-preupgrade
- vsd-rollback
- vsd-services-stop
- vsd-upgrade-destroy
- vsd-upgrade-postdeploy
- vsd-upgrade-prepare-for-deploy
- vsd-upgrade
- vstat-data-backup
- vstat-data-migrate
- vstat-deploy
- vstat-destroy
- vstat-health
- vstat-postdeploy
- vstat-predeploy
- vstat-rollback
- vstat-upgrade-destroy
- vstat-upgrade
- vstat-vrs-health
- vstat-vsc-health
- vstat-vsd-health

## Experimental
These are playbooks that are stable but under development or contributed from the field. Support is _best effort_.

- dns-deploy
- dns-destroy
- dns-postdeploy
- dns-predeploy
- mesos-deploy
- stcv-postdeploy
- stcv-predeploy

## Lab Playbooks
These are playbooks that are intended for use in the Metro Lab. You are welcome to use them, but they are not designed for general use.

- ci-deploy
- ci-destroy
- ci-predeploy
- infra-deploy
- infra-destroy
- infra-predeploy
- os-compute-deploy
- os-compute-destroy
- os-compute-postdeploy
- os-compute-predeploy
- os-snapshot
- osc-deploy
- osc-destroy
- osc-predeploy
- util-setup
- vsd-osc-config

# Deprecation notice
In the near future (date TBD), Metro is going to drop support for using Ubuntu as a deployment target for new VMs, e.g. VSD, VSC, VSTAT, etc. VRS and Dockermon will continue to be supported on Ubuntu 14.04 and Ubuntu 16.04.


# Questions, Feedback, and Issues

Questions should be directed to the [nuage-metro-interest mailing list](mailto://nuage-metro-interest@list.nokia.com).

Feedback and issues should be reported via the Github Issues feature or via email to [Brian Castelli](mailto://brian.castelli@nokia.com).

# License

TBD
