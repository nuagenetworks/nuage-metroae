# Deploying Nuage Networks Components in OpenStack with MetroAG 

The following components/roles are supported by MetroAG in OpenStack.
### Deploy VSD (Standalone or Cluster)
To deploy VSD in OpenStack you must upload VSD qcow2 image to glance. You must also create network and a flavor that is inline with the VSD resource requirements. (refer to VSP Install Guide).
### Deploy VSC (Single or pair)
To deploy VSC in OpenStack you must upload VSC qcow2 image to glance. You must also create mgmt, control networks and a flavor that is inline with VSC resource requirements. (refer to VSP Install Guide).
### Deploy VSTAT (Standalone or Cluster)
To deploy VSTAT (Elastic Search VM) you must upload VSTAT qcow2 image to glance. You must also create network and a flavor that is inline with VSTAT resource requirements (refer to VSP Install Guide).
### Customizing build_vars.yml
Please refer to an [example](../examples/build_vars_openstack_static_ip.yml) build_vars.yml for OpenStack environment.
### Running playbooks
Refer to [README.md](/README.md) for the organization of playbooks.
All the above roles/components can be run individually with `./metro-ansible <playbook>.yml` command.
## Questions, Feedback, and Contributing
Ask questions and get support via email.
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to Nuage MetroAG by submitting your own code to the project.
