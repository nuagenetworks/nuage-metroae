* Description
This role deploys and configures the Nuage Neutron plugin and associated packages on an installed openstack controller.

This includes the deployment of 
- nuage-openstack-neutron (ML2 plugin)
- nuage-openstack-horizon (dashboard extensions)
- nuage-openstack-heat: heat resource extensions
- nuage-openstack-neutronclient

It will also add the `csp` user to the CMS Group.


* Tested platforms
This role has been verified to be working with Nuage versions:
- 5.2.2

It has been tested in following openstack configurations:
- Openstack Pike, installed using `packstack --allinone`
