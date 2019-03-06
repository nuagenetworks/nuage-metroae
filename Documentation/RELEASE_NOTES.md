# Metro Automation Engine Release Notes
## Release 3.2.0
### New Features and Enhancements
* Optimize vCenter parameters
* Add CPU pinning (METROAE-586)
* Deliver container version of MetroAE via RPM (METROAE-739)
* Warn that deploying an image can take a long time (METROAE-775)
* Add host reference to vCenter (METROAE-812)
* Add support for VSP deploy on OpenStack (METROAE-842)
* Add support for NSGv bootstrap on AWS (METROAE-877)
* Add 'security_groups', 'port_name', and 'port_description' to OpenStack (METROAE-902)
* Make VSD deploy fail all when one fails (METROAE-907)
* For 5.4.1, return 'exit 0' when checking ssh connectivity (METROAE-909)
* Add NSGv postdeploy health check to ensure NSGvs are bootstrapped (METROAE-912)
### Resolved Issues
* Remove upgrade check for NTP sync (METROAE-586)
* Deploy VSC without vsds.yml (METROAE-759)
* NTP sync failure on VSC was not marked as failure (METROAE-777)
* Fix issue where VSC could not be added to a hardened VSD (METROAE-882)
* Fix metroae setup (container) syntax (METROAE-889 and 890)
* Fix issue with convert buildvars unicode script (METROAE-898)
* Fix issue that caused undefined variable when 'datastore' was not defined (METROAE-901)
* Add '0' to exit for 5.4.1 (METROAE-909)
* Add task to disable network manager on vnsutil
* Remove unwanted rpms and add docker directory to git ignore
* Remove utf-8 encoding from encrypt credentials
* Add encode and decode to encrypt credentials script
