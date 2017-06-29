# Metro: Release Notes

## Metro version
v2.1.2

## New features

1. Preview support for upgrade rollback for standalone VSD and VSC on KVM platform.See `UPGRADE.md`.
1. Added support to specify custom xmpp URL for clustered VSD deployments
1. Added support for preserving gateway purge timer during upgrades. See `UPGRADE.md`.
1. Added vns post deploy checks to verify TLS settings for XMPP on VSD.
1. Added modules to check YAML Syntax and validity of build_vars.yml.
1. Added VSD/VSC rollback for clustered VSD upgrades on KVM platform.
1. Added support for Standalone and Clustered VSTAT upgrade
1. Added support for deployments and upgrades to 5.0.x covering changes introduced in VSD 5.0.1 related to new VSD user
1. Added VSD license validation for upgrades across major versions (ex. 4.0.x to 5.0.1)
1. Added VNS support for Vmware platforms to deploy VNS utility vm and NSGv

 
## Usage Notes
1. Added new variable ansible_sudo_user_pub_key in to upgrade_vars.yml. This is required for VSD file copy operations during upgrades. 
 
## Resolved Issues
1. VSD DB backup failure during upgrades.
1. VSD purge timer restore failure during standalone upgrades.
1. VSD decouple report path is fixed. It now logs to reports folder. 
1. Added missing command to enable stats on vsd(s) when vstat is clustered
 
## Known Issues
 
## Known Limitations
 
1. No rollback support for VSC/VSD clustered upgrades on Vmware platform.
1. No rollback support for VSC/VSD standalone upgrades for Vmware platform.
1. Rollback support for VSTAT is experimental
1. VSD health checks during the upgrade only takes in to account monit summary, not other checks.
1. No support for release specific commands to stop elastic search/vstat process on vsd.
1. No support for release specific commands to stop core process on vsd.
1. Nuage Metro will not run on el6 (e.g. CentOS 6.8) hosts due to a lack of modern python-jinja2 support.
1. VSC disconnect from VSD prior 5.0.1 upgrade is not yet implemented
1. VNS support is only available for VSP version 5.0.1 and later.
1. VNS utility deployed has only a single NIC compared to KVM deployed VMs with 2 NICs.
