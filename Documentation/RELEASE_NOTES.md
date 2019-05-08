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
* IPv6 address support on mgmt_ip and data_ip for VSD, VSC and VSTAT (METROAE-960)
* Remove "local_host" group from hosts to avoid name conflicts (METROAE-985)
* Rename 'audit.log' to 'metroae.log' (METROAE-975)
* Ansible 2.7 support (METROAE-819)
* Ansible output now in YAML format (METROAE-978)
* Improve usability of unzipped directory specification (METROAE-876)
* Add support for activation_link NSGv bootstrap type
* Minor DNS enhancements
* Support in-place, u-release upgrade of VSDs (METROAE-971)
* Add Support for post-installation security features, a.k.a. hardening (METROAE-841)
* Support to setup VSTAT VSS UI (METROAE-952)
* Do not run vsd-deploy if vsd-predeploy fails on any node (METROAE-982)
* Upgrade support for OpenStack (METROAE-995)

### Resolved Issues
* Fix VSD Upgrade procedure to check for accurate ejabberd connected user list (METROAE-958)
* Health playbooks don't support custom usernames (METROAE-968)
* Remove obsolete document reference to build_vars.yml
* Fix undefined variable error during copy portal step in unzip task (METROAE-983)
* Check data fqdn only for VNSUTIL component (METROAE-984)
* Fix VSTAT description in CUSTOMIZE.md (METROAE-974)
* vnsutil-destroy unable to retrieve file because of include of non-existent openstack.yml (METROAE-986)
* Fix incorrect doc links to unzip directory structure instructions (METROAE-988)
* Allow Python libraries to use interpreter installed in alternate locations via PATH env (METROAE-990)
* Make VSD destroy serial to prevent race condition
