# Metro: Automated Deployment of Nuage Software

## What's new

1. Added pre-deploy support for VMware. Tested on R4.0R6.1 and 4.0R7.
1. Added support for mixed VRS architectures. That is, you can have some VRSs deployed on Ubuntu and some on RedHat/CentOS all using a single build.yml file.
1. Enhanced support for Dockermon install.
1. Documentation enhancements, including examples and how-tos.
1. Several bug fixes and infrastruture upgrades, including enhanced OpenStack deployment support and Jenkins CI integration.
1. Tested with *3.2R8, 4.0R4, and 4.0R7*

Feedback and bug reports should be provided via the Issues feature of Github or via email to [Brian Castelli](mailto://brian.castelli@nokia.com).

## Deprecation notice
In the near future (date TBD), Metro is going to drop support for using Ubuntu as a deployment target for new VMs, e.g. VSD, VSC, VSTAT, etc. VRS and Dockermon will continue to be supported on Ubuntu 14.04 and Ubuntu 16.04.

## Overview

This set of playbooks can be used to automatically deploy VCS/VNS components with target servers of the following types:

1. el7 (CentOS, RedHat)
1. el6 (CentOS, RedHat)
1. esx (VMware)
1. ubuntu14.04 (deprecated for all but VRS)
1. ubuntu16.04 (deprecated for all but VRS)

The VCS/VNS components that are supported are:

1. VSD (HA or stand-alone)
2. VSC (1 or more)
3. VRS on existing nodes (1 or more)
4. Dockermon on VRS nodes
5. VSTAT (1 or more)
6. VNSUTIL (1 or more)
7. NSGV (1)
8. VCIN

## For the impatient

The short version of the instructions are:

1. Install Ansible 2.2 on the deployment host for full support
1. Install Netmiko and its dependencies on deployment host.
1. Clone this repository to the deployment host
1. Customize `build.yml` with your VSD, VSC, VRS, VNSUTIL, NSGV  and VSTAT information. (See `BUILD.md` for details.)
1. Execute `./metro-ansible build.yml` to automatically populate variables in the appropriate places, e.g. the `host_vars` directory.
1. Execute `./metro-ansible install_everything.yml`
1. To get rid of everything that has been deployed, execute `./metro-ansible destroy_everything.yml'
1. To destroy all variables and reset `build.yml` to factory settings, execute `./metro-ansible reset_build.yml`. A `build.bak` file will be created just in case you didn't mean it.

Note that `install_everything.yml` can be edited for customizing your deployment.

## Branches

The latest sane code is found in the `master` branch. The `dev` branch is for ongoing development. The stability of the `dev` branch is not guaranteed.

If you want to contribute back, you must create your own branch or fork, push your changes to that, and create a pull request to the `dev` branch. All pull requests against the `master` branch will be rejected. Sorry. All pull requests should include tests for new functionality. See `CONTRIBUTING.md` for more details.

## Prerequisites

The following restrictions and conditions apply prior to executing the playbooks:

1. The hypervisor hosts must be running RedHat or CentOS. Support for Ubuntu exists but has been deprecated.
1. If host names are used for target systems, VSD, VSC, VSTAT, VNSUTIL and VRS nodes, those names must be discoverable via DNS *or* added to the /etc/hosts file of the ansible deployment host.
1. Each VM that is created for VSD, VSC, VSTAT, VNSUTIL or NSGV connects to one or more bridges on the target server. Those bridges must be created on the target server prior to deployment. Their names must be specified in the `build.yml` file. See `BUILD.md` for details.
1. Python 2.7+ and all its dependencies must be installed on the deployment host. Python 3.0 and above is untested.
1. Ansible 2.2 and all its dependencies must be installed on the deployment host.
1. Netmiko and all its dependencies must be installed on deployment host. The easiest way to install Netmiko is by using `pip install netmiko`. A common Netmiko dependency that could be missing is the cryptography package. See https://cryptography.io/en/latest/installation/ for more information.
1. VSPK (nuage python module) must be installed on the deployment host.
1. The ansible deployment host may also be a target server.
1. It may be necessary to remove the vsd, vsc and vstat entries from the ansible user's `~/.ssh/known_hosts` file to prevent errors from suspected DNS spoofing. This would only be necessary if multiple runs are attempted.
1. Under certain conditions, the `destroy_everything.yml` playbook must be run as sudo/root.

**Note:** These playbooks should work as long as there is network connectivity between the deployment host, the hypervisors, and the VMs on the hypervisors. Connectivity in this case means they can ping one another's hostname or IP address.

## vsd cluster mode

Currently VSD in cluster mode is supported exactly for 3 VSD nodes. 

## metro-ansible

`metro-ansible` is a shell script that executes ansible-playbook with the proper includes and command line switches. `metro-ansible` should be used when running *any* of the playbooks provided herein.

## HOWTO

The file `HOWTO.md` has been provided. It contains a few procedures for doing some more-complex deployments using Metro, e.g. deploying VRS to both Debian and RedHat family compute nodes.

## examples/

The `examples/` directory is populated with samples of files that can be used as models for particular kinds of operations, e.g. VSD only.

## Customization

### build.yml

`build.yml` contains a set of variables that should be customized by the user prior to running the playbooks. These variables are used to configure network connectivity for the VSC, VSTAT and the VSD.

`zfb.yml` contains a set of variables that should be customized by the user prior to running the nsgv playbooks. These variables are used to create NSG profile in the VSD Architect and also creates ISO file that is attached to NSG VM

## Playbook Organization

All playbooks, whether installation or destruction, must be executed using the `metro-ansible` script.

Each element to be deployed has up to 5 corresponding playbooks:

* `predeploy` : prepares infrastructure with necessary packages, finishing up by making the element reachable.
* `deploy` : installs and configures the element
* `postdeploy` : 
* `destroy` : removes the element from the infrastructure
* `health` : checks health for a running element without assuming it was deployed with Metro.

Every supported element must have at least a deploy playbook.

Playbooks `install_everything.yml` and `destroy_everything.yml` are provided as a convenience, but any playbook may be run stand-alone. This is especially useful for debugging or for skipping steps that you are confident need not be repeated.

## Debug

`ansible.cfg` is provided. By default, it tells ansible to log to ./ansible.log.

ansible supports different levels of verbosity, specified with one of the following command line flags:

* `-v`
* `-vv`
* `-vvv`
* `-vvvv`

More letters means more verbose. The highest level, `-vvvv`, provides ssh connectivity information.

## License

TBD
