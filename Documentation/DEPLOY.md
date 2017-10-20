# Deploying your NuageNetworks Virtualized Services Platform

During the *DEPLOY* phase, Metro will install all the components as defined in your `build_vars.yml` file.
It assumed you have already setup your environment using the instructions in [SETUP.md](SETUP.md) and [BUILD.md](BUILD.md).
As such you would have 
* a `hosts` file in the `nuage-metro/`, which will act as the Ansible inventory file
* a dynamically generated `host_vars/` and `group_vars/` directory containing variables that will be used for each and every component in the system

## Install everything

To deploy your full envrionment, just execute

``` 
./metro-ansible install_everything.yml
``` 

## Installing solution components

To deploy just a fraction of the solution, Metro also offers more modular execution models. 

Module | Command | Description
---|---|---
DNS | `./metro-ansible install_dns.yml` | Installs a DNS server based on `named`, with a zone file containing all necessary entries for VSP
VCS | `./metro-ansible install_vcs.yml` | Installs components for Virtualized Cloud Services
VNS | `./metro-ansible install_vcs.yml` | Installs VNS component on top of a VSP
OSC (experimental) | `./metro-ansible install_osc.yml` | Installs an RDO Openstack environment that is integrated against VSD

## Limiting your installation to a particular role or host

To limit your deployment to only a particular role or solution component, Metro has a complete library of playbooks which are directly linked to each individual role. They are stored in `playbooks/` folder. 
Still, to use them, please make sure to still use the  `./metro-ansible` executable to ensure variables are set properly.

Eg. to just deploy the VSD VM-images and get them ready for VSD software installation, run:
```
./metro-ansible vsd_predeploy.yml
```

To limit your deployment to a particular host, just add `--limit` parameter:
```
./metro-ansible vsd_predeploy.yml --limit vsd1.example.com
``` 



