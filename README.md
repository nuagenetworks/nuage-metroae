# Metro: Automated Deployment of Nuage Software

**NOTE: This package is considered Beta quality. It can be used for customer demos and PoCs but should first be tested in your lab to make sure it will work. It should not be distributed.

## What's new

1. VSD HA/cluster support, limited to exactly 3 VSD nodes
1. A new pre-deploy build process to simplify variable settings

Feedback and bug reports should be provided to the Nuage CASO team via** *[email to Brian Castelli](mailto://brian.castelli@nokia.com)* **or by creating an issue at the internal** *[gitlab site](http://gitlab.us.alcatel-lucent.com/caso-metro/metro-express/issues)*

## Overview

This set of playbooks can be used to automatically deploy VCS components for use with KVM on Ubuntu or CentOS. Support is provided for:

1. VSD (HA or stand-alone)
2. VSC (1 or more)
3. VRS on existing nodes (1 or more)
4. Dockermon on VRS nodes
5. VSTAT (1 or more)

## For the impatient

The short version of the instructions are:

1. Install Ansible 2.1+ on the deployment host
1. Install Netmiko and its dependencies on deployment host.
1. Clone this repository to the deployment host
1. Customize `build.yml` with your VSD, VSC, VRS, and VSTAT information. (See `BUILD.md` for details.)
1. Execute `./metro-ansible build.yml` to automatically populate variables in the appropriate places, e.g. the `host_vars` directory.
1. Execute `./metro-ansible install_everything.yml`
1. To get rid of everything that has been deployed, execute `./metro-ansible destroy_everything.yml'
1. To destroy all variables and reset `build.yml` to factory settings, execute `./metro-ansible reset_build.yml`. A `build.bak` file will be created just in case you didn't mean it.

Note that `install_everything.yml` can be edited or individual roles exec

## Prerequisites

The following restrictions and conditions apply prior to executing the playbooks:

1. The hypervisor hosts must be running Ubuntu Linux or CentOS. Testing has been done on Ubuntu 14.04 LTS and CentOS 7.
1. If host names are used for target systems, VSD, VSC, VSTAT and VRS nodes, those names must be discoverable via DNS *or* added to the /etc/hosts file of the ansible deployment host.
1. Each VM that is created for VSD, VSC or VSTAT connects to one or more bridges on the target server. Those bridges must be created on the target server prior to deployment and specified in the `user_vars.yml` file.
1. If host names are used for target systems, VSD, VSC, VSTAT and VRS nodes, those names must be discoverable via DNS *or* added to the /etc/hosts file of the ansible deployment host.
1. Python 2.7+ and all its dependencies must be installed on the deployment host. Python 3.0 and above is untested.
1. Ansible 2.1+ and all its dependencies must be installed on the deployment host.
1. Netmiko and all its dependencies must be installed on deployment host. The easiest way to install Netmiko is by using `pip install netmiko`. A common Netmiko dependency that could be missing is the cryptography package. See https://cryptography.io/en/latest/installation/ for more information.
1. The ansible deployment host may also be a target server.
1. The public ssh key of the ansible user that will run the playbooks must be added to `/root/.ssh/authorized_keys` on each target server, even if the deployment host and the target server are one in the same machine.
1. It may be necessary to remove the vsd, vsc and vstat entries from the ansible user's `~/.ssh/known_hosts` file to prevent errors from suspected DNS spoofing. This would only be necessary if multiple runs are attempted.
1. Under certain conditions, the `destroy_everything.yml` playbook must be run as sudo/root.

**Note:** These playbooks should work as long as there is network connectivity between the deployment host, the hypervisors, and the VMs on the hypervisors. Connectivity in this case means they can ping one another's hostname or IP address.

## vsd cluster mode

Currently VSD in cluster mode is supported exactly for 3 VSD nodes. 

## metro-ansible

`metro-ansible` is a shell script that executes ansible-playbook with the proper includes and command line switches. `metro-ansible` should be used when running *any* of the playbooks provided herein.

## Customization

### build.yml

`build.yml` contains a set of variables that should be customized by the user prior to running the playbooks. These variables are used to configure network connectivity for the VSC, VSTAT and the VSD.

## Playbook Organization

All playbooks, whether installation or destruction, must be executed using the `metro-ansible` script.

Each element to be deployed has up to 5 corresponding playbooks:

* predeploy
* deploy
* postdeploy
* destroy
* health_checks

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

## Authors

[Brian Castelli](mailto://brian.castelli@nokia.com)
[Santhan Pamulapati](mailto://Santhan.Pamulapati@nokia.com)
[Siddharth Singh](mailto://Siddharth.Singh@nokia.com)

## Attribution

The VSC portion of this work has its origins in a set of VSC deployment playbooks created and maintained by:

[Remi Vichery](https://github.com/rvichery)
[Jonas Vermeulen](https://github.com/jonasvermeulen)

Overall, the work was completed with the assistance of many people, too many to list here. Thank you all!

