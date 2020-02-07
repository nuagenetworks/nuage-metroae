# Metro Automation Engine Release Notes

## Release 4.0.0

### Feature Enhancements

* Refactor metroae command to support container management; RPM no longer required.
* Introduce day-zero VSD configuration support via `metroae config` (container only)
* Add support for Multiple VSC underlay VPRNs (METROAE-1175)
* Add VSC hardening (METROAE-1183)
* Add support for VSD certificate renewal standalone procedure (MetroAE-1188)

### Resolved Issues
* Fix VSC examples to have valid system ip address (METROAE-1177)
* Fix NTP retries masking non NTP sync errors (METROAE-1153)
* Fix fallocate failure on path with symbolic link (METROAE-1167)
* Fix deprecated task and changed result format for vmware_vm_facts (METROAE-1179)
* Detect when unresolved jinja2 is present in inventory (METROAE-820)
* Check for required disk space on VSD for backup files during upgrade health check (METROAE-1182)
* Convert shell mkdir tasks to ansible file module (METROAE-1059)
* Add optional user prompt confirmation before destroying components (METROAE-868)

### Removed
* Removed obsolete os_vsd_osc_integration playbook and associated role and files.
