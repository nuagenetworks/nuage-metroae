# Metro Automation Engine Release Notes
## Release 3.3.0
### Feature Enhancements
* Use ovftool probe mode to validate VSD version in OVA (METROAE-1099)
* Add telnet_port to NSGv and support MetroÆ on Ubuntu (METROAE-962)
* Enhanced support for nuagex deployments
* Verify that VSC reboot was successful (METROAE-648)
* Support deployment of SDWAN Portal
* Support GEO redundant VSD cluster install (METROAE-695)
* Use DNS server to verify full FQDN (METROAE-897)
* Support for VSD active/standby cluster failover (METROAE-955)
### Resolved Issues
* Fix VSD Upgrade procedure to check for accurate ejabberd connected user list (METROAE-958)
* Health playbooks don't support custom usernames (METROAE-968)
* Remove obsolete document reference to build_vars.yml
* Fix undefined variable eror during copy portal step in unzip task (METROAE-983)
* Check data fqdn only for VNSUTIL component (METROAE-984)
