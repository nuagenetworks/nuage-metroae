# Rollback VSD and VSC after an upgrade

Rollback playbooks allow rollback of VSD or VSC to the previous version of VSP code at certain points during or after an upgrade. For a successful rollback, `preserve_vsd: True` flag must be set during upgrade, and the VSC upgrade must
create a back up copy of the current cpm.tim. These are the default settings. VSD/VSC health reports will be generated and placed in the reports folder on the current directory where the playbooks are run.

Inaddition a copy of the upgraded VSD disk image will be preserved for forensics later on. This is controlled by the variable `rollback: True` which is set to true by default.

## To rollback VSD deployed on KVM platform after a standalone VSD upgrade:

`./metro-ansible vsd_sa_rollback.yml`

This will delete the upgraded VSD from the disk and from KVM then restore the VSD backed up during the upgrade.

## To rollback VSC node 1 and 2 in a clustered setup on KVM:
`./metro-ansible vsc_ha_node1_rollback.yml`

`./metro-ansible vsc_ha_node2_rollback.yml`

This will delete current cpm.tim image from the cf1:\timos directory and replace it with the back up cpm.tim image.
