This is an Ansible Role that is part of the Metro project, taking care of upgrading all VRS in a VMware environment that is managed by NuageNetworks VCenter Integration Node (VCIN).

Basically, it will 
- copy a new OVF to a webserver
- update the OVF URL in each vSphere Clusters that is used by VCIN
- run a `VCENTER_UPGRADE_VRS` job against each registered vSphere Cluster

# Further work
Further enhancements could be added to handle minor upgrades more gracefully. In the case of minor upgrades, 
- it is more appropriate to use `Upgrade Package URL` to minimize dataplane impact
- it could optionally include a rolling maintenance task



