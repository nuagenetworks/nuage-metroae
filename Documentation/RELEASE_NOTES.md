# Metro Automation Engine Release Notes
## Release 3.4.0

<<<<<<< HEAD
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
* Support SD-WANn Portal 6.0.1
* VNS support in wizard (METROAE-1151)

### Resolved Issues
* Set event log max age to 7 as per Nuage Upgrade procedure (METROAE-1001)
* Remove obsolete iptables traffic blocking during HA upgrade (METROAE-1051)
* Fix VSD node information to get Primary VSD information Rather than XMPP node info (METROAE-1093)
* Fixed issue with Active Standy VSTAT deploy with VSD in HA mode
* Add robustness to VSD failover procedure (METROAE-1111)
* Fix API version format in set_event_log.py (METROAE-1148)
=======
## Release 3.3.2

### Feature Enhancements
* Support Nuage VSD upgrade to 6.0.2 via Metro (METROAE-1121)

### Resolved Issues
* Fix VSD node information to get Primary VSD information Rather than XMPP node info (METROAE-1093)
* Fixed issue with Active Standy VSTAT deploy with VSD in HA mode
* Add option to skip DNS host resolution checks when DNS servers are not reachable from MetroAE server (METROAE-1117)
* Fix VSC backup error during HA upgrade (METROAE-1120)
* Use correct vCenter variable references (METROAE-1122)
* Fix update of /etc/hosts on VCIN nodes (METROAE-1123)
* Mysql password change errors out while running security hardening (METROAE-1126)
* Fix VSD 'Set upgrade complete flag' fails with non-default csproot password (METROAE-1116)
* Use primary group instead of username when chown of backup dir (METROAE-1118)
* Fixes for portal start up order and docker-compose.yml bug
>>>>>>> 0d0491ae8ac0a338120ed0196d4e38387b57303c
