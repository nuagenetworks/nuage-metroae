# Metro: Nuage Networks Automation Engine

## What's new

1. New upgrade procedure for VSD, VSC and VSTAT (ElasticSearch). See UPGRADE.md for details.
1. Added support for upgrade and rollback of VCIN.
1. Several enhancements to VMware support.
1. Added YAML syntax checker for build_vars.yml.
1. Mark VMs to autostart.
1. Deploy STCv on VMware.
1. Support ZFB external ISOs.
1. yum proxy support.
1. Sample Docker file to build Metro container.
1. Start libvirtd when doing a fresh install.
1. Updates and bug fixes for infra, upgrade, and deployment. See RELEASE_NOTES.md.
1. Tested with 4.0.R10 and 5.0.1.
1. Regression tested with 3.2.R10, 4.0.R4, 4.0.R8.
1. Many more...

## Questions, Feedback, and Issues

Questions should be directed to the [nuage-metro-interest mailing list](mailto://nuage-metro-interest@list.nokia.com).

Feedback and issues should be reported via the Github Issues feature or via email to [Brian Castelli](mailto://brian.castelli@nokia.com).

## Overview

This set of playbooks can be used to automatically deploy and (in some cases) upgrade VCS/VNS components with target servers of the following types:

1. el7 (CentOS, RedHat)
1. el6 (CentOS, RedHat)
1. esx (VMware)
1. ubuntu14.04 (VRS only)
1. ubuntu16.04 (VRS only)

The VCS/VNS components that are supported are:

1. VSD (HA or stand-alone)
2. VSC (1 or more)
3. VRS on existing nodes (1 or more)
4. Dockermon on VRS nodes
5. VSTAT (1 or more)
6. VNSUTIL (1 or more)
7. NSGV (1)
8. VCIN
9. DNS/NTP (1)

## Branches

The latest stable code is found in the `master` branch. The `dev` branch is for ongoing development. The stability of the `dev` branch is not guaranteed.

If you want to contribute back, you must create your own branch or fork, push your changes to that, and create a pull request to the `dev` branch. All pull requests against the `master` branch will be rejected. Sorry. All pull requests should include tests for new functionality. See `CONTRIBUTING.md` for more details.

## Prerequisites

### Priviledged execution on the Ansible host.

Metro operation requires priviledged execution on the Ansible host. By default, the variable `ansible_sudo_username` in build_vars.yml is set to `root` for priviledge execution. When `ansible_sudo_username` is set to `root`, no additional configuration on the Ansible host is required. For situations where you aren't allowed to use `root` for priviledged execution, changes are required in the `/etc/sudoers` file on the Ansible host.

When `root` is not used, passwordless execution must be enabled for the username set for `ansible_sudo_username`. The command `sudo visudo` must be used to make this change. Execute the command and configure:

```
## Next comes the main part: which users can run what software on
## which machines (the sudoers file can be shared between multiple
## systems).
## Syntax:
##
##      user    MACHINE=COMMANDS
##
## The COMMANDS section may have other options added to it.
##
## Allow root to run any commands anywhere
root    ALL=(ALL)       ALL
<ansible_sudo_username> ALL=(ALL) NOPASSWD: ALL
```

Substitute the username for `<ansible_sudo_username>` in the /etc/sudoers file. For example:

`jenkins ALL=(ALL) NOPASSWD: ALL`

Also, when `root` is not used, tty must not be required for the username set for `ansible_sudo_username`. The command `sudo visudo` must be used to make this change. Execute the command and configure:

```
#
# Disable "ssh hostname sudo <cmd>", because it will show the password in clear.
#         You have to run "ssh -t hostname sudo <cmd>".
#
#Defaults    requiretty
Defaults:<ansible_sudo_username> !requiretty
```

Substitute the username for `<ansible_sudo_username>` in the /etc/sudoers file. For example:

`Defaults:jenkins !requiretty`
`jenkins ALL=(ALL) NOPASSWD: ALL`

### Other Prerequisites

1. Ansible 2.2.1 is required.
1. The Ansible host must have the package python-jinja2 >= 2.7. python-jinja2 is installed by default with Ansible, but el6 hosts (e.g. CentOS 6.8) are limited to python-jinja2 < 2.7. Therefore, Nuage Metro will not run on el6 hosts.
1. The hypervisor hosts must be running RedHat or CentOS. Support for Ubuntu exists but has been deprecated.
1. If host names are used for target systems, VSD, VSC, VSTAT, VNSUTIL and VRS nodes, those names must be discoverable via DNS *or* added to the /etc/hosts file of the ansible deployment host.
1. Each VM that is created for VSD, VSC, VSTAT, VNSUTIL, NSGV and DNS/NTP connects to one or more bridges on the target server. Those bridges must be created on the target server prior to deployment. Their names must be specified in the `build_vars.yml` file. See `BUILD.md` for details.
1. The ansible deployment host may also be a target server.
1. It may be necessary to remove the vsd, vsc, vstat and dns/ntp entries from the ansible user's `~/.ssh/known_hosts` file to prevent errors from suspected DNS spoofing. This would only be necessary if multiple runs are attempted.
1. Under certain conditions, the `destroy_everything.yml` playbook must be run as sudo/root.

## Vcenter Prerequisites

In addition to the above prerequisites, the following packages are needed for vcenter deployments

1. Nuage software version 4.0R7 and greater is supported. Previous versions of Nuage software lack the required support.
1. `ovftool` package needs to installed on ansible deployment host. This package is available to download from here https://www.vmware.com/support/developer/ovf/.
1. pysphere  and pyvmomi packages needs to be installed on ansible deployment host. This can be done with pip install pysphere pyvmomi.

## OpenStack Prerequisites

In addition to the above prerequisites, the following packages are needed for openstack deployments

1. `shade` python module needs to installed on ansible deployment host. You can install using pip.

**Note:** These playbooks should work as long as there is network connectivity between the deployment host, the hypervisors, and the VMs on the hypervisors. Connectivity in this case means they can ping one another's hostname or IP address.

## metro-ansible

`metro-ansible` is a shell script that executes ansible-playbook with the proper includes and command line switches. `metro-ansible` should be used when running *any* of the playbooks provided herein.

## Detailed Instructions

1. Create ssh key pair for the user that runs metro playbooks
    > `ssh-keygen`
1. Copy ssh keys to localhosts's authorized key file
    > `ssh-copy-id localhost`
1. Install python pip on the Ansible host based on Redhat or Debian OS families
    > `yum install python2-pip` 
    > `apt-get install python-pip`
1. Install Ansible 2.2.1 on the Ansible host for full support
    > `pip install ansible==2.2.1`
1. Install Netmiko and its dependencies on the Ansible host.
    > `pip install netmiko`
1. Install netaddr and its dependencies on the Ansible host.
    > `pip install netaddr`
1. Install ipaddress and its dependencies on the Ansible host.
    > `pip install ipaddress`
1. Install Python pexpect module
    > `pip install pexpect`
1. Install VSPK Python module
    > `pip install vspk`
1. Clone this repository to the Ansible host
1. Customize `build_vars.yml` (and `zfb_vars.yml` if you are deploying VNS) with your VSD, VSC, VRS, VNSUTIL, NSGV  and VSTAT information. (See `BUILD.md` and `ZFB.md` for details.)
1. Copy your binary files to the proper locations. (See `BUILD.md` for details.) *If the files are not copied to the proper locations, the next step will fail to find them!*
1. Optionally execute `./metro-ansible nuage_unzip.yml` if you are installing from tar-gz files.
1. Execute `./metro-ansible build.yml` to automatically populate variables in the appropriate places, e.g. the `host_vars` directory.
1. Execute `./metro-ansible install_everything.yml`
1. To get rid of everything that has been deployed, execute `./metro-ansible destroy_everything.yml'
1. To destroy all variables and reset `build_vars.yml` to factory settings, execute `./metro-ansible reset_build.yml`. A backup of the existing `build_vars.yml` file will be created just in case you didn't mean it. The file name will be of the form `build_vars.yml.<date and time>~`.

Note that `install_everything.yml` can be edited for customizing your deployment.

## HOWTO

The file `HOWTO.md` has been provided. It contains a few procedures for doing some more-complex deployments using Metro, e.g. deploying VRS to both Debian and RedHat family compute nodes.

## examples/

The `examples/` directory is populated with samples of files that can be used as models for particular kinds of operations, e.g. VSD only.

## Customization

### build_vars.yml

`build_vars.yml` contains a set of variables that should be customized by the user prior to running the playbooks. These variables are used to configure network connectivity for the VSC, VSTAT, VSD and the DNS/NTP.

`zfb_vars.yml` contains a set of variables that should be customized by the user prior to running the nsgv playbooks. These variables are used to create NSG profile in the VSD Architect and also creates ISO file that is attached to NSG VM

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

## Metro Ansible Role Categories

### Core Ansible Roles
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

### Experimental
These are playbooks that are stable but under development or contributed from the field. Support is _best effort_.

- dns-deploy
- dns-destroy
- dns-postdeploy
- dns-predeploy
- mesos-deploy
- stcv-postdeploy
- stcv-predeploy

### Lab Playbooks
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

## Deprecation notice
In the near future (date TBD), Metro is going to drop support for using Ubuntu as a deployment target for new VMs, e.g. VSD, VSC, VSTAT, etc. VRS and Dockermon will continue to be supported on Ubuntu 14.04 and Ubuntu 16.04.

## License

TBD
