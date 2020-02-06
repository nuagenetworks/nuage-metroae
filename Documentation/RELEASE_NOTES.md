# Metro Automation Engine Release Notes

## Release 4.0.0

### Feature Enhancements

* Refactor metroae command to support container management; RPM no longer required.
* Introduce day-zero VSD configuration support via `metroae config` (container only)
* Add support for Multiple VSC underlay VPRNs (MetroAE-1175)

### Resolved Issues
* Fix VSC examples to have valid system ip address (MetroAE-1177)
* Fix NTP retries masking non NTP sync errors (METROAE-1153)
* Fix fallocate failure on path with symbolic link (METROAE-1167)
* Fix deprecated task and changed result format for vmware_vm_facts (METROAE-1179)
* Detect when unresolved jinja2 is present in inventory (METROAE-820)
* Check for required disk space on VSD for backup files during upgrade health check (METROAE-1182)
* Improved debugging output for vCenter ovftool commands (METROAE-981)

### Removed
* Removed obsolete os_vsd_osc_integration playbook and associated role and files.
