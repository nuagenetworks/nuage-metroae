# Metro Automation Engine Release Notes

## Release 3.3.1

### Resolved Issues
* Fixed issue with VSD Cluster failover if Primary Cluster is unreachable
* Remove support for ansible version other than 2.7.10 (METROAE-1065)
* Fixed issue with wizard not reading yaml-empty deployment files correctly
* Fixed issue with integer type input entries into run_wizard
* Fixed paths in nuage_health.yml
* Limit in-place, U-release upgrades to only upgrade_vsds
