# Metro Automation Engine Release Notes

## Release info

* MetroAE Version 4.0.1
* Nuage Release Alignment 6.0.5
* Date of Release TBD

## Release Contents

### Feature Enhancements

* None

### Resolved Issues

* Support target_server_type == none for skipping predeploy
* Fix prepositioning qcow2 files as a separate workflow
* Fix permissions on /opt/metroae during setup
* Fix paramiko version check
* Fix Ansible syntax error when running disk performance stand-alone
* Added Example for NSGv and NSGv access ports (METROAE-1344)
* Fix NUH Destroy playbook error and add VMName support (METROAE-1351)
* Skip docker images that aren't tagged
* Document that pyvmomi version 6.7.3 should be used for vCenter environments
* Fix VSC incorrectly requiring xmpp_username be defined
* Set pip package versions to known, tested values

## Test Matrix

This release was tested according to the following test matrix. Other combinations and versions have been tested in previous releases of MetroAE and are likely to work. We encourage you to test this in your lab before you apply it in production.

Workflow | Target Server | Version
-------- | -------- | --------
Install | KVM | Geo-redundant 6.0.3
Install | KVM | HA 5.3.3
Install | KVM | HA 5.4.1
Install | KVM | HA 6.0.3
Install | KVM | Active-Standby ES 6.0.3
Install | KVM | HA IPv6 6.0.3
Install | KVM | SA 5.3.3
Install | KVM | SA 5.4.1
Install | KVM | SA 6.0.3
Install | KVM | Add VSC pair 6.0.3
Install | KVM | SA CPU pinning 6.0.3
Install | KVM | SA VNS end-to-end 6.0.3
Install | KVM | SA VNS multi-uplinks 6.0.3
Install | KVM | SA feature tests 6.0.3
Install | KVM | SA IPv6 6.0.3
Install | KVM | SA Terraform 6.0.3
Install | KVM | SA via Container 6.0.3
Install | OpenStack | HA 5.3.2
Install | OpenStack | HA 6.0.3
Install | OpenStack | SA 5.3.2
Install | OpenStack | SA 6.0.3
Install | vCenter | HA w/VCIN 6.0.3
Install | vCenter | HA w/Hybrid VCIN 6.0.3
Install | vCenter | HA 5.3.3
Install | vCenter | HA 5.4.1
Install | vCenter | HA 6.0.3
Install | vCenter | HA Custom passwords 6.0.3
Install | vCenter | SA 5.3.3
Install | vCenter | SA 5.4.1
Install | vCenter | SA 6.0.3
Install | vCenter | SA Custom passwords 6.0.3
Upgrade | KVM | Geo-redundant 5.4.1-6.0.3
Upgrade | KVM | HA 5.3.3-6.0.3
Upgrade | KVM | HA inplace 5.4.1-5.4.1U5
Upgrade | KVM | HA 5.4.1-6.0.3
Upgrade | KVM | HA hardened 5.4.1-6.0.3
Upgrade | KVM | HA inplace 6.0.3-6.0.5
Upgrade | OpenStack | HA 5.4.1-6.0.3
Upgrade | OpenStack | SA 5.4.1-6.0.3
Upgrade | vCenter | HA 5.4.1-6.0.3
Upgrade | vCenter | HA hardened 5.4.1-6.0.3
Upgrade | vCenter | HA inplace 5.4.1-5.4.1U5
Upgrade | vCenter | HA inplace 6.0.3-6.0.5
Upgrade | vCenter | SA hardened 5.3.3-6.0.3
Upgrade | vCenter | SA 5.4.1-6.0.3
Wizard Install | KVM | SA via container 6.0.3
Wizard Install | KVM | SA via CSV 6.0.3
Wizard Upgrade | KVM | SA 5.4.1-6.0.3
