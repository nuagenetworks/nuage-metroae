# Metro Automation Engine Release Notes

## Release info

* MetroAE Version 4.0.0
* Nuage Release Alignment 6.0.5
* Date of Release 31-March-2020

## Release Contents

### Feature Enhancements

* New metroae script (New command structure, extensive command-line help, eliminate RPM for container management, bnash tab-completion support, self-updating, backwards compatible)
* Muti-underlay for VSC
* VSD Disk Performance Test
* VSD RTT Cluster Test
* VSC Security Hardening
* VSD Certificate renewal
* NUH Multi-external Interfaces (METROAE-1211)
* Install Zabbix Heatlh Agents
* Separate ES standby cluster install
* Discovery Wizard for Existing configs
* VSD /etc/hosts backup/restore
* NSGv Bootstrap with multiple uplinks
* Download Container Tarball (METROAE-1210)
* VSD backup disk space check
* mkdir tasks not using file module
* Prompt before destroy
* Enhance vCenter debug output
* Eliminate redundant pre-deploy code
* Upgrade multiple VSC pairs
* Relocate reports directory
* Patch upgrade to 6.0.5 (METROAE-1322)
* Document VSD rollback procedure
* Document Terraform best-practices
* Support Ansible 2.9
* Enhance no_log: true behavior

### Resolved Issues

* VSC Examples had invalid system_ip
* NTP retries masked real errors
* fallocate didn't follow symlinks
* Removed depecated code and warnings
* jinja2 in inventory not throwing an error
* VSD active/standby failover issue
* Log-gathering script not working with container
* Presence of upgrade.yml breaking install
* Patch upgrade of non-CVSD throwing error
* nsgv_postdeploy fails when VSC username is custom (METROAE-1238)
* Sample CSV file not copied out of container (METROAE-1208)
* Skip DNS tests not working as intended
* Misc wizard bugs
* VMware Ansible modules deprecated

### Removed

* Removed obsolete os_vsd_osc_integration playbook and associated role and files
* Removed beta GUI from container for security purposes (METROAE-1319)
