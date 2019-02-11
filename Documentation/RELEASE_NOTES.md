# Metro Automation Engine Release Notes
## Release 3.x
### New Features and Enhancements
* Optimize vCenter parameters
* Add CPU pinning (METROAE-586)
* Add host reference to vCenter (METROAE-812)
* Add support for VSP deploy on OpenStack (METROAE-842)
* Add OpenStack support for MetroÆ
### Resolved Issues
* Deploy VSC without vsds.yml (METROAE-759)
* Add '0' to exit for 5.4.1 (METROAE-909)
* Remove upgrade check for NTP sync (METROAE-586)
* Add task to disable network manager on vnsutil
* Remove unwanted rpms and add docker directory to git ignore
* Remove utf-8 encoding from encrypt credentials
* Add encode and decode to encrypt credentials script
* Fix issue with convert buildvars unicode script (METROAE-898)
