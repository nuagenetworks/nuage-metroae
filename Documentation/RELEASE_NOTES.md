# Metro Automation Engine Release Notes
## Release 2.4.X
### New Features and Enhancements
* add support for branding the VSD GUI  
* add NSG bootstrap via activation link  
* add VSD license expiration check
* update OpenStack Compute and Plugin integration, remove need to specify vsd_ip in myoscs, add handler to restart Neutron-server, reduce time to restart Neutron-server by adding tasks to Neutron-integration idempotent, make vsd-osc-integration equivalent to os-vsd-osc-integration, move stopping of Neutron services to the vrs-oscompute-integration role, change nuage_plugin.ini to be configured to use VSD FQDN
* improve integration with OpenStack controller, primarily by speeding up lab-installs of Nuage and OpenStack
* add ability to customize passwords for VSD programs and services
* add playbook to copy qcow2 files before predeploy step, add checks in predeploy step for qcow2 existence if skipCopyImages is set
### Resolved Issues  
* support custom group setting on ansible.log file  
* support doing MD5 checks of user input files in locations other than the current directory
* removed redundant check for netaddr package
