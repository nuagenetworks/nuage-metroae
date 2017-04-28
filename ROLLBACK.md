# Rollback VSD and VSC after an upgrade

These sets of playbooks allows to rollback VSD or VSC to a previous version of VSP code after an upgrade. It is assumed that preserve_vsd: True flag is set, which is the default. VSC upgrades by default will
create a back up copy of the current cpm.tim image to allow rollback. VSD/VSC health reports will be generated and palce in reports folder on the currrnet directory where the playbooks are run.


## To rollback VSD deployed on KVM platform after a standalone VSD upgrade:

`./metro-ansible vsd_sa_rollback.yml`

This will delete the upgraded VSD from the disk and from KVM then restore the VSD backed up during the upgrade. It is assumed that preserve_vsd: True flag is set, which is the default.

## To rollback VSC node 1 and 2 in a clustered setup on KVM:
`./metro-ansible vsc_ha_node1_rollback.yml`

`./metro-ansible vsc_ha_node2_rollback.yml`

This will delete current cpm.tim image from the cf1:\timos directory and replace it with back up cpm.tim image.

