# DEPLOY_CI

## Overview

DEPLOY_CI is used to dynamically create a deployment environment. It is specifically targeted for Metro deployments in OpenStack. At the behest of a CI server, e.g. Jenkins, one or more slave VMs are created as well as a subnet to connect them. The end result is a deployment environment that the CI server can use as target servers for Metro. This way each time a user submits a code to metro-dev or when code is merged with master branch a seperate VM is created with its own network and VSP componenets are deployed into this VM. It is intended that the environment live only as long as required, being torn down automatically after testing is complete.   

## Details

### deploy_ci.sh

Executing this script will copy the `setup.yml.CI` file to metro root folder and execute setup file, executes the reset-build and build roles - to populate files/vars required for ci-* roles to create VMs and networks in VSD and OpenStack, executes ci-predeploy role, executes ci-deploy role, executes reset-build and build role - this time to populate files/vars required to deploy VCS components and finally execute `test.yml` file - to destroy previous VCS components, if at all they exist and deploy new VCS components in to OpenStack VMs.
 
### setup.yml.CI

This setup file is responsible for creating a random hostname for CI VMs that will be deloyed in OpenStack. This hostname is populated in `build.yml.RedHat.CI.j2` build file and is copied to reset-build role files.

### ci-build role

The ci-build role is used to automatically populate a number of Ansible variable files for the operation of the metro playbooks on OpenStack. This is used to create a `hosts` file, populate a `host_vars` directory, populate a `group_vars` directory, that are consumed by ci-predeploy/deploy/destroy roles.

### ci-predeploy role

The ci-predeploy role is used to create networks in VSD and also create VM instances in OpenStack project. `ci-predeploy` calls a python script and heat templates located in `files` sub dir to create environment to be able to deploy VSP components in the VMs using metro playbooks.


### ci-deploy role

The ci-deploy role is used to install all the necessary packages (e.g. dnsmasq ,ntp, etc) required for the VMs, confgiure the connectivity between jenkins master and all the slave VMs. `ci-deploy` role is also responsible for creating a custom `build.yml` file with IP addresses from the VM network. This is achieved using jinja2 template for the build file.

### ci-destroy role

Finally the ci-desroy role will free up the resources by deleting networks in VSD and desroying the VMs in OpenStack along withthe networks.

## Reference

For reference, here is a description of the contents of the `build.yml.Redhat.CI.j2` file, with comments:

```
#    CI VMs
#    # CI VMs that will be deployed in OpenStack
#    mycis:
#          # The fqdn of this CI VM instance
#      - { hostname: This is generated randonly and automatically,
#          # The target server type is only heat
#          target_server_type: heat,
#          # Image used to deploy CI VM 
#          # Image should exist in OpenStack glance
#          ci_image: centos7,
#          # Flavor used to create VM (e.g. size of hard disk and ram, vcpus, etc)
#          # Must exist in OpenStack project     
#          ci_flavor: m1.medium}
#    OpenStack credentials for authentication
#    os_auth:
#          # The username for OpenStack project
#          username: admin
#          # Password for OpenStack project
#          password: admin
#          # OpenStack project name
#          project_name: jen
#          # OpenStack keystone url
#          auth_url: 'http://10.0.0.4:5000/v2.0'
#    # ENVIRONMENT
#    # The hostname or IP address of the ansible machine
#    ansible_deployment_host: 135.227.181.232
#    # NTP servers the CI VM ntp client should syn to
#    # One or more ntp servers are required
#    ntp_server_list:
#      - 135.227.181.232
#      - 128.138.141.172
```
