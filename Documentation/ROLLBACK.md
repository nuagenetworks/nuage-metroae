# Rollback VSD and VSC after an upgrade

Rollback playbooks allow rollback of VSD or VSC to the previous version of VSP code at certain points during or after an upgrade. For a successful VSD rollback, `preserve_vsd_for_rollback: True` flag must be set in `build_vars.yml` prior to executing the `build_upgrade.yml` playbook. This will result in metro taking backups of the disk images and the kvm configs just before the VSD decouple take place. Similarily the VSC upgrade must create a back up copy of the current cpm.tim. These are the default settings and are not exposed to the users. 

VSD/VSC health reports will be generated and placed in the reports folder on the current directory where the playbooks are run.

In addition, a copy of the upgraded VSD disk image will be preserved for forensics later on. This is controlled by the variable `rollback: True` which is set to true by default and is not exposed to the users.

## To rollback VSD deployed on KVM platform after a standalone VSD upgrade:

`./metro-ansible vsd_sa_rollback.yml`

This will delete the upgraded VSD from the disk and from KVM then restore the VSD backed up during the upgrade.

## To rollback VSC node 1 and 2 in a clustered setup on KVM:
`./metro-ansible vsc_node1_rollback.yml`

`./metro-ansible vsc_node2_rollback.yml`

This will delete current cpm.tim image from the cf1:\timos directory and replace it with the back up cpm.tim image.

## To rollback VSDs deployed on KVM platform after a clustered VSD upgrade:

`./metro-ansible vsd_ha_rollback.yml`

This will move the upgraded VSDs in to a rollback folder and bring up the VSDs from the backup folder taken just before SVD decouple. VSD rollback can be done after VSD2 and VSD3 upgrade or after all 3 VSDs were upgraded. Once the VSD vms are running , the vsd cluster will be reinitiated per https://intranet.mv.nuagenetworks.net/images/doc/0.0/current/VSP-Install-Guide/2b-vsd-monitor.html 
