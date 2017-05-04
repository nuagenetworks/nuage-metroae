# Metro: Release Notes

## Metro version
v2.1.0

## New features
1. Preview support for VSD/VSC upgrade. See `UPGRADE.md`.
1. Preview support for upgrade rollback for standalone VSD and VSC on KVM platform.See `UPGRADE.md`.
1. Moved build variables out of `build.yml`, creating `build_vars.yml`. See `BUILD.md`.
1. Simplifed and renamed a few build variables.
1. Renamed `nuage-unpack` to `nuage-unzip` and decoupled from build. Now you run `nauge_unzip.yml` if and only if you want to unzip tar.gz files.
1. Added support for identifying the operation you are performing on each component. See `build_vars.yml`.
1. Added support to use custom hypervisor and Ansible host usernames. Default is `root`.
1. Added check to verify that NTP servers are specified using the proper format.
1. Added support for up to 6 NSGV ports and enhanced bootstrap support.
1. Added acpi support for NSGV.
1. Added support for specifying ssh keys to be used during deployment and upgrades.
1. Moved user credentials to an external file, `user_creds.yml`.
1. Added support to launch Spirent STCv test ports.
1. Added support to specify custom xmpp URL for clustered VSD deployments
1. Added support for preserving gateway purge timer during upgrades. See `UPGRADE.md`.
 
## Usage Notes
1. The biggest impact to users that have been using previous releases of Metro is the change in the way build variables are specified. You will need to save a backup copy of your existing build.yml file, get the latest code, then manually update `build_vars.yml` to the same configuration as your old `build.yml`. 
1. `nuage_unzip.yml` is now a separate step from build.
1. Added new variable vsd_fqdn_global in to build_bars.yml to be used by other components. 
 
## Resolved Issues
1. Many issues have been resolved, too many to list here.
 
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
