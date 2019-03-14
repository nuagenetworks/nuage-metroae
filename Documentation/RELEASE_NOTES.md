# Metro Automation Engine Release Notes
## Release 3.2.0
### New Features and Enhancements
* Provide set-group capability to metro-setup script (METROAE-921)
* Fix regex of VRS el7 not to pickup VMware
* Add a log of all installs (audit.log) (METROAE-922)
* Optimize vCenter parameters
* Add CPU pinning (METROAE-586)
* Deliver container version of MetroAE via RPM (METROAE-739)
* Warn that deploying an image can take a long time (METROAE-775)
* Add host reference to vCenter (METROAE-812)
* Add support for VSP deploy on OpenStack (METROAE-842)
* Add support for NSGv bootstrap on AWS (METROAE-877)
* Add 'security_groups', 'port_name', and 'port_description' to OpenStack (METROAE-902)
* Make VSD deploy fail all when one fails (METROAE-907)
* Add NSGv postdeploy health check to ensure NSGvs are bootstrapped (METROAE-912)
* Make data_fqdn required for VNSUTIL (METROAE-904)
* Make VSC control interface params optional (METROAE-932)
### Resolved Issues
* Fix VSD branding in 5.4.1 (METROAE-929)
* Always update etc/hosts for 5.4.1 (METROAE-818)
* Lock netmiko version to 2.3.0 (METROAE-925)
* Export HTTPS_PROXY also
* Add ignore case to image names regex
* Disable cloud init vnsutil
* Remove upgrade check for NTP sync (METROAE-586)
* Deploy VSC without vsds.yml (METROAE-759)
* NTP sync failure on VSC was not marked as failure (METROAE-777)
* Fix issue where VSC could not be added to a hardened VSD (METROAE-882)
* Fix metroae setup (container) syntax (METROAE-889 and 890)
* Fix issue with convert buildvars unicode script (METROAE-898)
* Fix issue that caused undefined variable when 'datastore' was not defined (METROAE-901)
* Return 'exit 0' when checking ssh connectivity for 5.4.1 (METROAE-909)
* Add task to disable network manager on vnsutil
* Remove unwanted rpms and add docker directory to git ignore
* Add encode and decode to encrypt credentials script
* Fix bridge examples to be names not IP addresses (METROAE-930)
* Update ES upgrade for 5.4.1 (METROAE-931)
* Add support for setting VSTAT hostname (METROAE-891)
* Destroy then re-add VSC fails to copy certs from VSD (METROAE-884)
* Update VSD branding support for 5.4.1 (METROAE-929)
