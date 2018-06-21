# Metro Automation Engine Release Notes
## Release 2.4.1
### New Features and Enhancements
* PR #670 - Add check to verify VSDs are connected to VSCs 
* PR #665 - Add validation for vsd hostname 
* PR #662 - Change remote user from ‘root’ (or nothing) to a variable 
* PR #664 - Add support for checking REST and JMS gateway on VSD and check VSTAT web gateway
* PR #663 - Update paramiko version in two files
* PR #661 - Delete all os-compute-*, osc-*, and infra-* from roles and playbooks
* PR #657 - Change ‘vsc_upgrade_backup_and_prep’ to vsc_sa_upgrade_backup_and_prep’ in UPGRADE.md
* PR #652 - Add parameter to specify backup location when upgrading
* PR #649: Support for master/slave VCIN.
* PR #648: Remove deprecated `include:` Ansible commands.
* PR #645: Added yum_proxy support to dns.
* PR #638: Added static route support for VNSUTIL.
* PR #618: Added new roles for installation of VRS compute nodes, vrs-vm.

### Resolved Issues
* PR #675 – Minor correction in ‘hosts.j2’ vsr section
* PR #674 - Correct SROS prompt 
* PR #671 - Change ‘inventory hostname’ to ‘vm_name’ for dns image path 
* PR #667 - Fix a failure during pip package check
* PR #666 - Change ‘inventory hostname’ to ‘vm_name’ for dns image path 
* PR #658 - Add yum update and libguestfs-tools to ‘roles/vrs-vm-deploy/tasks/main.yml’
* PR #656 - Import validate-build-vars task from common roles
* PR #654 - Add name ‘nsgv_predeploy’ to ‘install_vns.yml’
* PR #653 - Delete sgt-qos section of config.cfg.j2
* PR #651 Add check for DNS qcow2
* PR #650: Add guestfish from the libguestfs-tools package as a prerequisite.
* Issue #646: The handle_vars playbook did not take into account custom provided build_vars_files or user_creds_file and calculated/verified the MD5 sum of the wrong files (static build_vars.yml and user_creds.yml instead of the provided values.
* PR #643: vrs-vr image directory fix.
* PR #640: Fix error on dns-predeploy when hostname and vmname are the same.
