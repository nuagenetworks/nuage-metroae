# Metro Automation Engine Release Notes
## Release 2.4.3
### New Features and Enhancements
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
* fix inconsistency in the way VMs were shutdown during upgrade
* update dns zones with values from build_vars.yml and solve the firewalld issue from dns-deploy/task/main.yaml file
* support custom group setting on ansible.log file
* support doing MD5 checks of user input files in locations other than the current directory
* removed redundant check for netaddr package
* fix username for vmware-vm_shell commands in vsd-predeploy
* fix username for executing monit_waitfor_service task in vstat-vsd-health
* fix uri task in vstat-health to execute on localhost
