# Metro Automation Engine Release Notes
## Release 2.4.5
### Resolved Issues
* Set validate_certs to no for VMware playbooks
* Clean socket files to work around Ansible persistent connection bug
* Fix vsc_health and vstat_health to support custom username and password
* Remove vstat_health from UPGRADE procedures
* Fix vstat-vsd-health role to only run when VSTATs are defined
* Removed unused datafile, upgrade_vars.yml
* Removed unused playbooks, vsc_ha_node1_upgrade.yml and vsc_ha_node2_upgrade.yml

## Release 2.4.4
### New Features and Enhancements
* upgrade VSTAT and VSC operating with user other than root
* Skip shared domain for maintenance mode
* Updates to use a simpler path for the backup directory on the VSD, to rename some variables so that their use is more obvious, and to clean up the backup directory on the VSD after the backup has been transferred from the VSD to the localhost.
### Resolved Issues
* Remove local connection from VSD decouple
* add remote user to get monit summary process
* add become privileges to monit_summary


## Release 2.4.3
### New Features and Enhancements
* add 5.3.1 from version to VSTAT upgrade skip list
* refactor logic behind destroy during install and upgrade, edit VSTAT list of versions to be skipped during upgrade.
* add vnc console access in VSD template
* add vault encryption procedure doc
* check the 'show router interface' command to verify that states for Adm and Oprv4 are correct for control interface
* add support for new cloud-init version for 5.3.2
* add support for upgrade to version 5.3.2
* add suppport for non-root usernames for VSD upgrade
* add support for NuageX deployment type
* add support for branding the VSD GUI
* add NSG bootstrap via activation link
* add VSD license expiration check
* update OpenStack Compute and Plugin integration, remove need to specify vsd_ip in myoscs, add handler to restart Neutron-server, reduce time to restart Neutron-server by adding tasks to Neutron-integration idempotent, make vsd-osc-integration equivalent to os-vsd-osc-integration, move stopping of Neutron services to the vrs-oscompute-integration role, change nuage_plugin.ini to be configured to use VSD FQDN
* improve integration with OpenStack controller, primarily by speeding up lab-installs of Nuage and OpenStack
* add ability to customize passwords for VSD programs and services
* add playbook to copy qcow2 files before predeploy step, add checks in predeploy step for qcow2 existence if skipCopyImages is set
### Resolved Issues
* user-related fixes
   - vsd-predeploy role tries to use the password listed in user_creds.yml to authenticate in the vmware_vm_shell tasks, rather than root/Alcateldc, which it should be using for a freshly-deployed OVF.
   - roles/vstat-vsd-health/tasks/main.yml: Needs remote_user: "{{ vstat_username }}" on the monit_waitfor_service task, otherwise it tries to SSH into vstat using the local username on the metro host, not the root user.
   - roles/vstat-health/tasks/main.yml: Needs delegate to localhost.
   - roles/vsc-backup/vars/main.yml: All the scp command lines refer to vsc_user - it should be vsc_username.
* add become privilege to ActiveMQ status monitoring
* Set and verify JMS Master Node SA
* Add default VSD username for ActiveMQ status
* Paramiko check and JMS Gateway Check Refactoring
* add functionality to configure autostart for vCenter VMs. Turn off autostart for VMs that are shutdown during the upgrade process.
* fix inconsistency in the way VMs were shutdown during upgrade
* update dns zones with values from build_vars.yml and solve the firewalld issue from dns-deploy/task/main.yaml file
* support custom group setting on ansible.log file
* support doing MD5 checks of user input files in locations other than the current directory
* removed redundant check for netaddr package
* fix username for vmware-vm_shell commands in vsd-predeploy
* fix username for executing monit_waitfor_service task in vstat-vsd-health
* fix uri task in vstat-health to execute on localhost
