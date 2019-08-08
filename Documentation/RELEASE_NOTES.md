# Metro Automation Engine Release Notes
## Release 3.3.0
### Feature Enhancements
* Use ovftool probe mode to validate VSD version in OVA (METROAE-1099)
* Add telnet_port to NSGv and support MetroÆ on Ubuntu (METROAE-962)
* Enhanced support for nuagex deployments
* Verify that VSC reboot was successful (METROAE-648)
* Support deployment of SDWAN Portal
* Support active/standby (aka GEO redundant) VSD cluster install (METROAE-695)
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
* Make any_errors_fatal a global config item
* Support for VSD active/standby cluster failover (METROAE-955)
* Support application of standard and cluster licenses on install and upgrade for 5.3 and up (METROAE-600)
* Enhance error checking in vCenter VSD destroy (METROAE-980)
* Update instructions for using ovftool with the metroae container
* Implement check of VSC authentication from Ansible host (METROAE-999)
* Implement upgrade of GEO redundant VSD cluster (METROAE-989)
* Disable SELinux for Base CentOS image for SD-WAN portal
* Added run_wizard.py to simplify setup and deployment creation
* Support Active Standby VSTAT cluster (METROAE-853)
* Support variable number of cpu cores for all components in KVM deployments (METROAE-942)

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
* Fix health checks for VSD with custom username (METROAE-994)
* Skip monit status for processes and programs that are disabled by user
* Unzip fixes for SD-WAN portal
* Set Upgrade Complete flag on VSD for minor upgrade (METROAE-1008)
* Remove old iptables rule in VSC preupgrade (METROAE-1013)
* Update VSPK libraries to import version 5.0 (METROAE-1052)
* Update the way we get VSD version to protect against a custom user that lacks the VSD_VERSION env variable
* Made changes to accommodate 6.0.1 command line changes on VSC
