# Metro Automation Engine Release Notes
## Release 2.4.1
### New Features and Enhancements
* Support for Nuage Networks version 5.2.3
* Add check to verify VSDs are connected to VSCs
* Add validation for vsd hostname
* Change remote user from ‘root’ (or nothing) to a variable
* Add support for checking REST and JMS gateway on VSD and check VSTAT web gateway
* Update paramiko version in two files
* Delete all os-compute-*, osc-*, and infra-* from roles and playbooks
* Change ‘vsc_upgrade_backup_and_prep’ to vsc_sa_upgrade_backup_and_prep’ in UPGRADE.md
* Add parameter to specify backup location when upgrading
* Support for master/slave VCIN.
* Remove deprecated `include:` Ansible commands.
* Added yum_proxy support to dns.
* Added static route support for VNSUTIL.
* Added new roles for installation of VRS compute nodes, vrs-vm.

### Resolved Issues
* Minor correction in ‘hosts.j2’ vsr section
* Correct SROS prompt
* Change ‘inventory hostname’ to ‘vm_name’ for dns image path
* Fix a failure during pip package check
* Change ‘inventory hostname’ to ‘vm_name’ for dns image path
* Add yum update and libguestfs-tools to ‘roles/vrs-vm-deploy/tasks/main.yml’
* Import validate-build-vars task from common roles
* Add name ‘nsgv_predeploy’ to ‘install_vns.yml’
* Delete sgt-qos section of config.cfg.j2
* Add check for DNS qcow2
* Add guestfish from the libguestfs-tools package as a prerequisite.
* The handle_vars playbook did not take into account custom provided build_vars_files or user_creds_file and calculated/verified the MD5 sum of the wrong files (static build_vars.yml and user_creds.yml instead of the provided values.
* vrs-vr image directory fix.
* Fix error on dns-predeploy when hostname and vmname are the same.
* Fix issue with running metro-ansible without root user.
