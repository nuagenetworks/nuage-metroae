# MetroAG Release Notes
## Release 0.0.0
### New Features and Enhancements
* Execute vsd-health as part of vsd-post-deploy
* In vrs-health, look for interfaces connected to alubr0 instead of named tap*
* In vrs-postdeploy, better regex to determine ovs-vtep ip in case VSC is routed via default route, or indirect route
* For VSC, vsc_mgmt_static_route_list is now optional for cases where no static route list is required.
* Skip predeploy and deploy when already present, allowing, for example, re-running install_everything multiple times.
* Add installation of nuage-selinux packages.
### Resolved Issues
* Eliminate check for exactly 3 XMPP users
* Allow NSGV MAC address to be set
* Support limit on VSC system name length without limiting hostname length
* Fixed vnsutil-postdeploy to run the install script with the data_fqdn
## Release 2.3.1
### Resolved Issues
* Under certain conditions, VSTAT upgrade would fail because we didn't use the _upgrade_ VM name for the new VM.
* Change VSTAT password from env variable to vsc_creds.yml
* Added python-six dependency to vrs-predeploy
* Updated Dockerfile support
* Replaced list_of_vscs variable to eliminate undefined var error
* Add dvSwitch when deploying VCIN
* fallocate space for VSD VM during predeploy
* Remove cloud init files from VNS Utils VM (for 5.1.2 support)

### Known Limitations
When using Ansible 2.4.0 with MetroAG 2.3.1 the shell fails to open on VSC healthcheck.

Example:
```
TASK [vsc-health : Get output of 'show version'] ************************************************************
task path: /metro/nuage-metro-2.3.1/roles/vsc-health/tasks/main.yml:27
<localhost> using connection plugin network_cli
<localhost> socket_path: None
fatal: [vsc1-404.newport.npi -> localhost]: FAILED! => {
    "changed": false,
    "failed": true,
    "msg": "unable to open shell. Please see: https://docs.ansible.com/ansible/network_debug_troubleshooting.html#unable-to-open-shell"
}
```
This is a result of a bug in paramiko 2.3.1, the Python package that is installed with Ansible 2.4. Ansible uses paramiko to connect to SROS devices, e.g. VSC. We have a couple of workarounds to choose from.

* Downgrade to paramiko==2.2.1.
`pip install paramiko==2.2.1`
See also instructions for [debugging this error](http://docs.ansible.com/ansible/latest/network_debug_troubleshooting.html#unable-to-open-shell) and for [enabling network logging](http://docs.ansible.com/ansible/latest/network_debug_troubleshooting.html#enable-network-logging) in Ansible for guidance.

* Remove the python-gssapi package.
`pip uninstall python-gssapi`
The specific bug in paramiko that we are addressing is that it throws an exception loading the GSSAPI package. A possible alternative to downgrading paramiko to 2.2.1 is to remove the python-gssapi package. It isn’t needed, and removing it will not affect MetroAG operation.

## Release 2.3.0
### New Features and Enhancements
*	Support Ansible 2.3/2.4 (Use Ansible==2.4)
*	Added script to setup MetroAG environment
* Moved playbooks and docs to subfolders to reduce clutter
* Reorganized and clarified docs
*	Added support for per-VM network bridges
*	Added VSR deploy support
* Added VRS upgrade support
*	Added vsd-postdeploy
*	Added Early DNS validation
* Added build_var.yml validation
*	Retargeted VCIN deploy to use VSD roles
*	Move vsc-health variables to build_vars.yml
*	Added VRSG health checks
*	Enhanced Nuage-unzip
*	Removed test directory and its contents
*	Allow XMPP connection type setting on VSD
*	Support per-VSC health variable setting
* Enhanced license script to deploy multiple licenses
### Resolved Issues
*	Align vsd-destroy for vcenter with vsd-destroy fo kvm
*	Several fixes for VSC/VSD upgrade
*	Ejabberd connected user test
*	Make system_ip in build_vars.yml optional
*	Fix vstat-destroy to preserve VMs on upgrade
*	Fix known_hosts file cleaning
*	Fix vstat-deploy to look for firewalld
*	Add more time for NTP sync
*	Fix error when producing lists of VRS packages to install
*	Check max length of VSC hostname
* Added iptables for VSTAT
### Known Limitations
*	VSD health checks during the upgrade only takes in to account monit summary, not other checks.
*	No support for release specific commands to stop elastic search/vstat process on vsd when upgrading from 3.2R8 to 4.0RX.
*	No support for release specific commands to stop core process on vsd when upgrading from 3.2R8 to 4.0RX.
*	Nuage Metro will not run on el6 (e.g. CentOS 6.8) hosts due to a lack of modern python-jinja2 support.
*	VNS support on VMware is only available for VSP version 5.0.1 and later.
* VSPK version for the `nsgv-predeploy` role is hardcoded to v4_0 in `library/nuage_vspk.py`. If you need v5_0, edit `library/nuage_vspk.py` accordingly.
* When using Ansible 2.3.1, it is possible to have a VSC operation fail similar to the following:
```
01:41:05 fatal: [jenkinsvsc1.example.com -> localhost]: FAILED! => {
01:41:05     "changed": false,
01:41:05     "err": "[Errno 111] Connection refused",
01:41:05     "failed": true,
01:41:05     "invocation": {
01:41:05         "module_args": {
01:41:05             "backup": false,
01:41:05             "config": null,
01:41:05             "defaults": false,
01:41:05             "host": null,
01:41:05             "lines": [
01:41:05                 "******** save"
01:41:05             ],
01:41:05             "match": "line",
01:41:05             "parents": null,
01:41:05             "password": null,
01:41:05             "port": null,
01:41:05             "provider": {
01:41:05                 "host": "192.168.122.214",
01:41:05                 "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
01:41:05                 "port": null,
01:41:05                 "ssh_keyfile": null,
01:41:05                 "timeout": null,
01:41:05                 "transport": "cli",
01:41:05                 "username": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
01:41:05             },
01:41:05             "save": false,
01:41:05             "src": null,
01:41:05             "ssh_keyfile": null,
01:41:05             "timeout": null,
01:41:05             "username": null
01:41:05         }
01:41:05     },
01:41:05     "msg": "unable to connect to socket"
01:41:05 }
```
This is a result of a bug in Ansible 2.3.1. When making connections to network devices, such as a VSC, Ansible uses a “persistent connection” mode. That is, Ansible opens a socket to the network device and keeps it open for some time after the task that opened the connection completes. If another task wants to make a connection to the network device and the socket is still present, the new task reuses the socket, saving the overhead of creating a new socket. This was added for performance enhancement. Under some circumstances, notably when deploying the same VM over and over again, the socket file on disk that represents the connection isn’t properly cleaned up. When one of these stale files exists, it can sometimes cause the error, above.

The work around is to manually delete the socket file. Ansible puts the persistent connection socket file in the directory `~/.ansble/pc/`. If you experience the error, above, try deleting the contents of `~/.ansible/pc/`, then re-running the playbook.

## Release 3.0.0

### New Procedures and Improvements

* **Deprecation of build_vars.yml.**  There is no longer a single monolithic configuration file for MetroAG.  Configuration is specified through "deployments".  A tool is provided to convert an obsolute build_vars.yml file to a deployment.  See [Customization](Documentation/CUSTOMIZATION.md) for details on deployments.
* **Deprecation of `build`.**  The user no longer needs to issue the `build` playbook.  This will be handled automatically and seamlessly by the MetroAG tool.  MetroAG also tracks changes and will skip steps not required if configuration is unmodified.
* **Schema validation of deployment data.**  All configuration specified in a deployment is automatically validated against json-schema.org schemas.  This ensures that all required fields are set and every field has the correct syntax.  Any error will be found as early as possible and a specific error message will call out the exact problem.
* **Workflows instead of playbooks.**  In order to simplify usage, the concept of `playbook` is being replaced by a `workflow`.  The .yml extension is no longer required.  Thus, issue `vsd_deploy` instead of `vsd_deploy.yml`.  The MetroAG tool is renamed from `metro-ansible` to `metroag`.  It now supports different arguments, including `--list` which displays all supported workflows.
* **Cleanup of repo.**  The MetroAG repository has been cleaned.  Only tools useful for users are present in the root directory.  The internal workings of the tool have been moved to sub-directories like src/.
