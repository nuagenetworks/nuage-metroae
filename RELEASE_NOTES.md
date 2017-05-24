# Metro: Release Notes

## Metro version
v2.1.2

## New features
1. Added VSD/VSC rollback for clustered VSD upgrades on KVM platform.
 
## Usage Notes
1. Added new variable ansible_sudo_user_pub_key in to upgrade_vars.yml. This is required for VSD file copy operations during upgrades. 
 
## Resolved Issues
1. VSD DB backup failure during upgrades.
1. VSD purge timer restore failure during standalone upgrades.
 
## Known Issues
 
## Known Limitations
 
1. No rollback support for VSC/VSD clustered upgrades on Vmware platform.
1. No rollback support for VSC/VSD standalone upgrades for Vmware platform.
1. VSD health checks during the upgrade only takes in to account monit summary, not other checks.
1. No support for release specific commands to stop elastic search/vstat process on vsd.
1. No support for release specific commands to stop core process on vsd.
