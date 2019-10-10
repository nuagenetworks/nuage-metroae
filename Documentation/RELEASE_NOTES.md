# Metro Automation Engine Release Notes

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
