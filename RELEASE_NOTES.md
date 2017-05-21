# Metro: Release Notes

## Metro version
v2.1.2

## New features
 
## Usage Notes
1. Added new variable ansible_sudo_user_pub_key in to upgrade_vars.yml. This is required for VSD file copy operations during upgrades. 
 
## Resolved Issues
1. VSD DB backup failure during upgrades.
 
## Known Issues
 
## Known Limitations
 
1. No rollback support for VSC/VSD clustered upgrades.
1. No rollback support for VSC/VSD standalone upgrades for Vmware platform.
1. VSD health checks during the upgrade only takes in to account monit summary, not other checks.
1. No support for release specific commands to stop elastic search/vstat process on vsd.
1. No support for release specific commands to stop core process on vsd.
