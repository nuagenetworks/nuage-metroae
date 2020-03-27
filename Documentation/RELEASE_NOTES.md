# Metro Automation Engine Release Notes

## Release info

* MetroAE Version 4.0.0
* Nuage Release Alignment 6.0.5
* Date of Release 31-March-2020

## Release Contents

### Feature Enhancements

* New metroae script (New command structure, extensive command-line help, eliminate RPM for container management, bnash tab-completion support, self-updating, backwards compatible)(METROAE-905)
* Muti-underlay for VSC (METROAE-1175)
* VSD Disk Performance Test (METROAE-1169)
* VSD RTT Cluster Test (METROAE-766)
* VSC Security Hardening (METROAE-1183)
* VSD Certificate renewal
* NUH Multi-external Interfaces (METROAE-1211)
* Install Zabbix Heatlh Agents
* Separate ES standby cluster install (METROAE-1081)
* Discovery Wizard for Existing configs (METROAE-1195)
* VSD /etc/hosts backup/restore (METROAE-1187)
* NSGv Bootstrap with multiple uplinks (METROAE-852)
* Download Container Tarball (METROAE-1210)
* VSD backup disk space check (METROAE-1182)
* mkdir tasks not using file module (METROAE-1059)
* Prompt before destroy (METROAE-868)
* Enhance vCenter debug output
* Eliminate redundant pre-deploy code (METROAE-801)
* Upgrade multiple VSC pairs (METROAE-490)
* Relocate reports directory (METROAE-879)
* Patch upgrade to 6.0.5 (METROAE-1322)
* Document VSD rollback procedure (METROAE-1181)
* Document Terraform best-practices (METROAE-1144)
* Support Ansible 2.9 (METROAE-1138)
* Enhance no_log: true behavior (METROAE-981)

### Resolved Issues

* VSC Examples had invalid system_ip (METROAE-1177)
* NTP retries masked real errors (METROAE-1153)
* fallocate didn't follow symlinks (METROAE-1167)
* Removed depecated code and warnings
* jinja2 in inventory not throwing an error (METROAE-820)
* VSD active/standby failover issue
* Log-gathering script not working with container (METROAE-1202)
* Presence of upgrade.yml breaking install (METROAE-1161)
* Patch upgrade of non-VSD throwing error
* nsgv_postdeploy fails when VSC username is custom (METROAE-1238)
* Sample CSV file not copied out of container (METROAE-1208)
* Skip DNS tests not working as intended (METROAE-1203)
* Misc wizard bugs (METROAE-1196)
* VMware Ansible modules deprecated (METROAE-1179)
* Fix GEO redundant VSD install issue for v6.0.X

### Removed

* Removed obsolete os_vsd_osc_integration playbook and associated role and files
* Removed beta GUI from container for security purposes (METROAE-1319)
