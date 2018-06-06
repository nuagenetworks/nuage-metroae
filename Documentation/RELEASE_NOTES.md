# MetroAG Release Notes
## Release 2.4.1
### New Features and Enhancements
* PR #649: Support for master/slave VCIN.
* PR #648: Remove deprecated `include:` Ansible commands.
* PR #645: Added yum_proxy support to dns.
* PR #638: Added static route support for VNSUTIL.
* PR #618: Added new roles for installation of VRS compute nodes, vrs-vm.

### Resolved Issues
* Issue #646: The handle_vars playbook did not take into account custom provided build_vars_files or user_creds_file and calculated/verified the MD5 sum of the wrong files (static build_vars.yml and user_creds.yml instead of the provided values.
* PR #650: Add guestfish from the libguestfs-tools package as a prerequisite.
* PR #643: vrs-vr image directory fix.
* PR #640: Fix error on dns-predeploy when hostname and vmname are the same.
