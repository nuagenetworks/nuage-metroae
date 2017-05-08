# Metro: Release Notes

## Metro version
v2.1.1

## New features
1. Preview support for upgrade rollback for standalone VSD and VSC on KVM platform.See `UPGRADE.md`.
1. Added support to specify custom xmpp URL for clustered VSD deployments
1. Added support for preserving gateway purge timer during upgrades. See `UPGRADE.md`.
1. Added vns post deploy checks to verify TLS settings for XMPP on VSD.
 
## Usage Notes
1. Added new variable vsd_fqdn_global in to build_bars.yml to be used by other components. 
 
## Resolved Issues
1. Preserving gateway purge timer during upgrades.
1. Enable TLS on all VSDs during installing VNS on clustered VSD setup.
 
## Known Issues
1. Upgrade may continue in certain cases despite the errors encountered.
1. Upgrade does not support for adding PBR to change VNI IDs of BG routes when upgrading from VSP 3.2 versions.
1. Upgrade fails when ugrading VSC on vcenter.
 
## Known Limitations
 
1. No rollback support for VSC/VSD clustered upgrades.
1. No rollback support for VSC/VSD standalone upgrades for Vmware platform.
1. VSD health checks during the upgrade only takes in to account monit summary, not other checks.
1. No support for release specific commands to stop elastic search/vstat process on vsd.
1. No support for release specific commands to stop core process on vsd.
