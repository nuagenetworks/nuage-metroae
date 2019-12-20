# Metro Automation Engine Release Notes

## Release 3.4.0

### Feature Enhancements

* Support bringing up vCenter VMs with interfaces disabled during upgrade (METROAE-644)
* NSG Bootstrap support for vCenter (METROAE-1045)
* Add VSD Certificate renewal procedure to VSD upgrade (METROAE-1002)
* Added REST API check to VSD health (METROAE-1005)
* Added METROAE_GROUP environment variable to set the file group of log files
* Set jinja2 version to 2.10.1
* Simplify the retrieval of vCenter UUIDs (internal enhancement)
* Added option for ovftool verbose logging based on logging level used on the playbook (METROAE-1050)
* Add DOMAIN specification to VSD interface file (METROAE-1004)
* Support VSD, VSC and VSTAT(ES) install over SSH proxy (METROAE-1046)
* Add playbook to delete VSD backup after upgrade (METROAE-1009)
* Move config.cfg setting from vsc-predeploy to vsc-deploy (METROAE-896)
* Check file permissions before running guestfish on KVM images (METROAE-752)
* Add availability zone support for OpenStack
* Add example deployment for geo-redundant VSD deployment
* Port support for CATS environment VSC, DNS, proxy, STCv
* For VSC, support VLAN ID and vprn for control interface
* For VSTAT and VNS Utils, support data network static route
* Support Nuage Utility Host(NUH) SA and HA install using MetroAE (METROAE-1062)
* Support SD-WAN Portal 6.0.1
* VNS support in wizard (METROAE-1151)
* Added support for spreadsheet/CSV input method
* Added script for collecting debug collateral
* Check certificate count before running vsd db backup (METROAE-1055)
* Added graceful restart of vsd services support (METROAE-1084)
* Added documentation for Skip and Hooks actions (METROAE-1066)
* Added documentation for deploying with Terraform and MetroÆ (METROAE-1144)

### Resolved Issues

* Set event log max age to 7 as per Nuage Upgrade procedure (METROAE-1001)
* Remove obsolete iptables traffic blocking during HA upgrade (METROAE-1051)
* Fix VSD node information to get Primary VSD information Rather than XMPP node info (METROAE-1093)
* Fixed issue with Active Standy VSTAT deploy with VSD in HA mode
* Add robustness to VSD failover procedure (METROAE-1111)
* Fix API version format in set_event_log.py (METROAE-1148)
* Remove VSC dependence on VSD config by using vsd_fqdn_global instead of primary_vsds (METROAE-1155)
* Fix to allow sd-wan portal to run without a yum proxy
* Fix VSC openstack bof config management netmask to be user defined instead of hardcoded 24
* Allow VSC mgmt_static_route_list to accept an explicit empty list "[]" in order to not configure any static routes. (METROAE-1163)

### Removed

* As previously announced, support for converting pre-3.0 build_vars conversion is removed
