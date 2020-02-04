# Metro Automation Engine Release Notes

## Release 4.0.0

### Feature Enhancements

* Refactor metroae command to support container management; RPM no longer required.
* Introduce day-zero VSD configuration support via `metroae config` (container only)
* Add support for Multiple VSC underlay VPRNs (MetroAE-1175)

### Resolved Issues
* Fix VSC examples to have valid system ip address (MetroAE-1177)
* Fix deprecated task and changed result format for vmware_vm_facts (METROAE-1179)

### Removed
* Removed obsolete os_vsd_osc_integration playbook and associated role and files.
