# MetroAG Release Notes
## Release 2.4.0
### New Features and Enhancements
* Eliminate the build_upgrade.yml playbook and consolidate upgrade_vars.yml into build_vars.yml. Enhance user_creds.yml to contain variables for all component logins. There are now only 3 user data files: build_vars.yml, user_creds.yml, and zfb_vars.yml.
* Support in-place ElasticSearch upgrade. Add support for both old and new upgrade procedure in vstat. Eliminate upgrade_major_or_minor var.
* Added support to VSS and AAR. New file “roles/vstat-deploy/tasks/aar_vss_enable.yml” creates certificates from VSD and pushes them to the stats VM. Also starts the nginx engine. Modified “roles/vstat-deply/tasks/non_heat.yml” to include file
* Build step is now run automatically when user runs Nuage playbooks directly.
* Refactor build role – VSR+VRS_DNS_Nuage OpenStack Plugins. Removes get_paths.yml from build and build-upgrade role. Includes refactor of VSR, VRS, DNS and Nuage OpenStack plugin files
* Added skipping of VSTAT when iptables/firewalld rules are already in place
* VSC health failure indication and displaying the error messages after all VSC health checks have been done
* Skip all components if healthy. Adds skipping functionality for all components (VSC, VRS, VSTAT, VNSUTILS, NSGV) in predeploy and deploy if the component is already running and healthy.
* Add installation of Nuage-selinux packages for RHEL7 & CentOS7. The Nuage selinux package allows the user to set selinux to enforcing mode on the nodes running the VRS. This is supported for RHEL7 and CentOS7.
* Support some VSCs having system IPs, and some not. Eliminates undefined variable error when some VSCs have system IPs, and some don’t
* Limit VSC name length check to system name, and allow user to specify a shorter one
* Add option to create dvSwitch when deploying VCIN
* Call ‘fallocate’ on VSD VM disk for KVM – adds a variable for the disk size to preallocate, default 285GB
* Execute vsd-health as part of vsd-post-deploy
* In vrs-health, look for interfaces connected to alubr0 instead of named tap*
* In vrs-postdeploy, better regex to determine ovs-vtep ip in case VSC is routed via default route, or indirect route
* For VSC, vsc_mgmt_static_route_list is now optional for cases where no static route list is required.
* Skip predeploy and deploy when already present, allowing, for example, re-running install_everything multiple times.

### Resolved Issues
* Fix problems in AAR VSS support. Eliminate installing pip and pexpect, only generate the certificate once
* Fix timeouts on backing up VSC by scp directly
* Add data_bridge support in the vnsutil hosts template and remove waiting for vmware tools for nsgv
* Add paramiko to pip install list. Pinning paramiko version 2.2.1 as there is a bug in the latest version (paramiko 2.3.1) installed by Ansible 2.4.
* Reset VSD keystore password to default when upgrading. In the field, we’ve run into issues where customers configure a non-default password on the keystore, and our VSD upgrade/decouple scripts fail. This task checks if the keystore password is still set to default, and if not asks the user to configure a variable with the current password so we can change it back to default.
* Fix VRS health check for VMs with multiple vnics, or interfaces not named ‘tapxxxx’
* NSGV bug fix. MAC address of NSGV, which is needed for ZFB, was not getting populated in the build
* Fix VSC user credentials. The vrs-postdeploy tasks depend on vsc_username and vsc_password being specified for each VSC
* Remove cloud-init files from Utils VM
* Install missing VRS dependency python-six, .rpm does not list it as dependency
* Fix bug in VSTAT XML definition. Upgrade was not picking up vm_name since vmname is defined in XML definition
* Eliminate check for exactly 3 XMPP users
* Fixed vnsutil-postdeploy to run the install script with the data_fqdn
