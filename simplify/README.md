# A simplified structure for Metro Ansible scripts

I have been working with and contributing to Metro for a while now, and although the general concept is great and highly useful, there are some structural challenges
with the way metro is built up that make things much harder than they need to be.

## Good points
* User has a single text file to define everything about their Nuage deployment
* Support for deploy, upgrade, health checks, destroy
* Support for KVM, VMWare

## Points needing improvement
* Significant duplication of code and logic, cumbersome 'roles' structure, ,multiple inconsistent default values
* Indirect build-up of inventory and variable files means adding parameters/features affects many different files ( build/templates, build-upgrade/templates, etc. )
* Duplicate and potentially inconsistent semantics as to what the user wants to do ( playbook selected, 'operations' parameter in Yaml, tags/limits applied, etc. )
* Many conditional tasks which get skipped ( clobbered output )
* Some duplication in the user input file ( e.g. network parameters )
* Explicit configuration of things like server type and OS ( el7, el6, vcenter, etc. ) which should be implicitly discovered
* Does not provide an (optional) standard naming convention for Nuage VMs - while we could definitely use one
* Limited use of Ansible tags to select a subset of tasks to execute
* No support for building out Linux/VMWare network constructs ( bridges, bonds, vlans, etc. )

# A new start 
The files in this directory provide a starting point for some radical improvements. They would obviously need a lot more work, but the basic structure is in place.
This initial part deploys or destroys VSD and VSC VMs on RedHat hosts, based on copied code from the master branch.

* The user provides a single JSON input file ( could also be Yaml, but I dislike Yaml - any language in which whitespace is significant should be banned )
* The inventory of hosts is dynamically built up from this input file, using add_host ( for Linux servers, VMs )
* Host variables are added to each host including the global 'nuage' blob which contains all the parameters
  + Whenever new structure is added to the user's input file, this is automatically available to all hosts
* Default naming conventions for VSDs, VSCs ( vsd1.domain, vsd2.domain, etc. )
* 'mgmt_bridge' as an example of how to support per-VM custom bridge names ( simply add a variable in deploy.yml )
* A generic 'vm-host' role to install libvirt, qemu, etc., with OS specific tasks included by variable name ( not using 'when: OS==RedHat', etc. )
* A role per Nuage component ( VSD, VSC, etc. ), with reuse of common code under /common
* Optimized VSD qcow copying in case a single host is used for test environments ( dramatically reduces deployment time )
* Deployment on VMWare is inferred from the user's input ( VM host == vCenter IP? then it gets installed on VMWare, else it must be a Linux server )
  + Initially supporting a single vCenter with VM deployment guided by datastore selection, could support a pair of vCenters if needed

Code that was previously included as separate roles can become task files within these simplified roles ( e.g. vsd/tasks/healthcheck.yml ), making it much
easier to find the relevant code being executed, and avoiding the duplication of variable files across roles.