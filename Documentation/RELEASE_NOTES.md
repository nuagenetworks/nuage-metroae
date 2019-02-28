# Metro Automation Engine Release Notes
## Release 3.1.0
### New Features and Enhancements
* Add system_name to vscs.json to allow optional customization
* Add support for VSC to talk to the data interface on AWS
* Refactor VM Deploy using ovftool with nolog
* Add known_hosts cleanup
* Remove unnecessary mode 777 settings for vstat backup
* Support non-default TLS
* Support VSD license check any time except postdeploy
* Support NSG bootstrap in AWS
* Add note about upgrade and health requiring passwordless ssh
* Add v5.3.3 to VSTAT version checks
* Consolidate common code from five places into one
* Do not error stopping of VSD services when they are already stopped
* Clarify error message when target server ssh fails
* Reduce code duplication by consolidating common vsd-deploy code from nuagex.yml, heat.yml and non_heat.yml into main.yml
* Remove configuration from vnsutil-postdeploy, add it to vnsutil-deploy
* Validate if gateway address is in correct range
### Resolved Issues
* Wait for VCIN to be ready before replicating
* Correct target server type options in schemas
* Enhance support for custom usernames for target servers
* make failure to find the root partition with guestfish an error  
* Check if iptable entry exists before adding one
* Add /etc/hosts setting on each VSD/VSTAT when they are clustered, allowing each VSD to reach the other, even in the event of a DNS failure.
* In main.yml use data_fqdn instead of mgmt fqdn when creating vnsutil certificates
* Add ability to bootstrap multiple NSGs
