# Metro Automation Engine Release Notes

## Release info

* MetroAE Version 4.1.1
* Nuage Release Alignment 20.5.1, 6.0.8
* Date of Release 8-Sept-2020

## Release Contents

### Feature Enhancements

* None

### Resolved Issues

* Fix failure to properly skip copying qcow2 files when skip flag is set
* Fix VSD Active Standby Failover syntax error

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
