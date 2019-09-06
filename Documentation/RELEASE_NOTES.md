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
* Support Nuage Utility Host(NUH) SA and HA install using MetroAE (METROAE-1062)

### Resolved Issues
* Set event log max age to 7 as per Nuage Upgrade procedure (METROAE-1001)
* Remove obsolete iptables traffic blocking during HA upgrade (METROAE-1051)
* Fixes issue with VSD Cluster failover if Primary Cluster is unreachable
* Remove support for ansible version other than 2.7.10 (METROAE-1065)
