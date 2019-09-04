# Metro Automation Engine Release Notes

## Release 3.3.1

### Resolved Issues
* Fixed issue with VSD Cluster failover if Primary Cluster is unreachable
* Removed support for ansible version other than 2.7.10, you must run usingn Ansible 2.7.10 (METROAE-1065)
* Fixed issue with run_wizard not reading yaml-empty deployment files correctly
* Fixed issue with run_wizard not handling integer type input entries correctly
* Fixed broken paths in nuage_health.yml
* Fixed In-place U-release upgrades, e.g. 5.4.1 > 5.4.1U5
    * Enforce In-place upgrades to be *only* accomplished via `upgrade_vsds`. Any other upgrade play will throw an error.
    * Accept upper and lowercase 'u' when specifying upgrade versions
    * Properly parse In-place upgrade version strings
    * Stop checking for image files when doing a U-release, VSD-only upgrade
* Documentation enhancements
