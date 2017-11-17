# A simplified structure for Metro Ansible scripts

I have been working with and contributing to Metro for a while now, and although the general concept is great and highly useful, there are some structural challenges
with the way metro is built up that make things much harder than they need to be.

## Good points
* User has a single text file to define everything about their Nuage deployment
* Support for deploy, upgrade, health checks, destroy
* Support for KVM, VMWare

## Points needing improvement
* Significant duplication of code and logic, cumbersome 'roles' structure
* Indirect build-up of inventory and variable files means adding parameters/features affects many different files ( build/templates, build-upgrade/templates, etc. )
* Many conditional tasks which get skipped ( clobbered output )
* Some duplication in the user input file ( e.g. network parameters )

# A new start 
The files in this directory provide a starting point for some radical improvements. They would obviously need a lot more work, but the basic structure is in place.
This initial part deploys VSD VMs on RedHat hosts, based on copied code from the master branch.

* The user provides a single JSON input file ( could also be Yaml, but I dislike Yaml - any language in which whitespace is significant should be banned )
* The inventory of hosts is dynamically built up from this input file, using add_host
* Host variables are added to each host including the global 'nuage' blob which contains all the parameters
* Default naming conventions for VSDs, VSCs ( vsd1.domain, vsd2.domain, etc )
* 'mgmt_bridge' as an example of how to support per-VM custom bridge names ( simply add a variable in deploy.yml )
* A generic 'vm-host' role to install libvirt, qemu, etc., with OS specific tasks included by variable name ( not using 'when: OS==RedHat', etc. )
* A role per Nuage component ( VSD, VSC, etc. ) - needs further restructuring, e.g. to reuse VM image manipulation code across roles
* Optimized VSD qcow copying in case a single host is used for test environments ( dramatically reduces deployment time )

Code that was previously included as separate roles can become task files within these simplified roles ( e.g. vsd/tasks/healthcheck.yml ), making it much
easier to find the relevant code being executed, and avoiding the duplication of variable files across roles.