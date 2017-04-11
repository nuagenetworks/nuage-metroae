# HowTo: tips and tricks for getting the most out of Nuage-Metro

## Table of contents

* [Customizing the Component Mix](Customizing the Component Mix)
* [Deploying VRS on Multiple Target Architectures](Deploying VRS on Multiple Target Architectures)
* [Deploying NSG in AWS](Deploying NSG in AWS)
* [Questions and Issues](Questions and Issues)

## Customizing the Component Mix

Nuage-Metro supports customizing the list of components the playbooks operate on.

### `build_vars.yml` defines the list

`README.md` and `BUILD.md` describe how to configure the variable in `build_vars.yml` to define the components Nuage-Metro will operate on. `build_vars.yml` contains a dictionary of configuration parameters for each component in the list. For example, to operationalize two VSCs, `build_vars.yml` would contain the following:

```
myvscs:
  - { hostname: jenkinsvsc1.example.com,
      target_server_type: "kvm",
      target_server: 135.227.181.233,
      mgmt_ip: 192.168.122.212,
      mgmt_gateway: 192.168.122.1,
      mgmt_netmask_prefix: 24,
      ctrl_ip: 192.168.100.202,
      ctrl_netmask_prefix: 24,
      vsd_fqdn: jenkinsvsd1.example.com,
      system_ip: 1.1.1.2,
      xmpp_username: jenkinsvsc1,
      vsc_static_route_list: { 0.0.0.0/1 } }
  - { hostname: jenkinsvsc2.example.com,
      target_server_type: "kvm",
      target_server: 135.227.181.233,
      mgmt_ip: 192.168.122.213,
      mgmt_gateway: 192.168.122.1,
      mgmt_netmask_prefix: 24,
      ctrl_ip: 192.168.100.203,
      ctrl_netmask_prefix: 24,
      vsd_fqdn: jenkinsvsd1.example.com,
      system_ip: 1.1.1.3,
      xmpp_username: jenkinsvsc2,
      vsc_static_route_list: { 0.0.0.0/1 } }
```

### Initializing the list

You can customize the list of components Nuage-Metro operates on by including or excluding components from `build_vars.yml`. When the build playbook is run (`./metro-ansible build.yml`), the following occurs:

* The `hosts` file is populated with the hostnames of all components in the list. The `hosts` file defines the inventory playbooks will operate on.
* The `host_vars` subdirectory is populated with variable files for each component in the list. These variable files contain configuration information specific to each component in the list.
* Various variables are set that configure the overall operation of the playbooks.

In a manner of speaking, then, `build_vars.yml` defines the list of components that Nuage-Metro will operate on. It also defines how those components will be operated on.

### Playbooks and the list

Nuage-Metro playbooks have been designed to operate on only the components that appear in the list. If you run a playbook for a component that is not in the list, the playbook will skip all tasks associated with that component and run to completion without error. Thus running the `install_everything.yml` playbook when only VRS appears in the list will deploy VRS successfully while happily ignoring the tasks for components that do not appear in the list.

### Example

As an example, let's consider using Nuage-Metro to deploy a VSD cluster by itself. The basic pattern described here applies to deploying only VSD, VSD+VSC, VSD+VSC+VRS, VSC only, VSTAT only, and a number of other combination of list components.

For deploying a VSD cluster, you must define 3 VSD entries in the `myvsds` dictionary in `build_vars.yml`. You must also have the other required definitions in place. Here is an example of the `build_vars.yml` file that deploys a cluster of 3 VSDs:

```
  nuage_zipped_files_dir: "/home/caso/metro/4.0R4/nuage-packed"
  nuage_unzipped_files_dir: "/home/caso/metro/4.0R4/nuage-unpacked"
  vsd_standalone: false
  myvsds:
    - { hostname: jenkinsvsd1.example.com,
        target_server_type: "kvm",
        target_server: 135.227.181.233,
        mgmt_ip: 192.168.122.211,
        mgmt_gateway: 192.168.122.1,
        mgmt_netmask: 255.255.255.0 }
    - { hostname: jenkinsvsd2.example.com,
        target_server_type: "kvm",
        target_server: 135.227.181.233,
        mgmt_ip: 192.168.122.212,
        mgmt_gateway: 192.168.122.1,
        mgmt_netmask: 255.255.255.0 }
    - { hostname: jenkinsvsd3.example.com,
        target_server_type: "kvm",
        target_server: 135.227.181.233,
        mgmt_ip: 192.168.122.213,
        mgmt_gateway: 192.168.122.1,
        mgmt_netmask: 255.255.255.0 }
  ansible_deployment_host: 135.227.181.233
  mgmt_bridge: "virbr0"
  data_bridge: "virbr1"
  access_bridge: "access"
  images_path: "/var/lib/libvirt/images/"
  ntp_server_list:
    - 135.227.181.232
    - 128.138.141.172
  dns_server_list:
    - 192.168.122.1
    - 128.251.10.145
  dns_domain: example.com
 ```

Some items to note in the example, above:

* `vsd_standalone` must be set to `False`. If it is True, Nuage-Metro will deploy 3 stand-alone VSDs without clustering them.

## Deploying VRS on Multiple Target Architectures

Some customer environments use a mix of Debian- and RedHat-family Linux distributions in their compute nodes, where Debian == Ubuntu and Redhat == CentOS or RHEL.

### Two build files for two architectures

Nuage-Metro supports deploying VRS onto two target architectures by supporting VRS groups in `build_vars.yml`. The following is an example of deloying VRSs on 3 target architectures using one 'build_vars.yml' file.

### Example build_vars.yml file for three VRS target architectures

```
myvrss:
  - { vrs_set_name: vrs_set_uswest1,
      vrs_os_type: u14.04,
      active_controller_ip: 192.168.122.202,
      standby_controller_ip: 192.168.122.203,
      vrs_ip_list: [
       192.168.122.101] }
  - { vrs_set_name: vrs_set_usewest2,
      vrs_os_type: el7,
      active_controller_ip: 192.168.122.202,
      standby_controller_ip: 192.168.122.203,
      vrs_ip_list: [
       192.168.122.83,
       192.168.122.238 ] }
  - { vrs_set_name: vrs_set_uswest3,
      vrs_os_type: u16.04,
      active_controller_ip: 192.168.122.202,
      standby_controller_ip: 192.168.122.203,
      vrs_ip_list: [
       192.168.122.215 ] }
```


## Deploying NSG in AWS

Metro supports the deployment of NSGs in AWS and configuring those as Network Gateways in a particular enterprise of a Nuage Networks installation.
It assumes the necessary enterprise and NSG template has been preconfigured:
It can either
- use an existing VPC, and attach the network interfaces of the NSG-AMI, or
- provision a new VPC with a set of subnets, and configure some default routing tables and security groups.

Once it has been deployed, it is up to end-user to configure the necessary VPort Bridge in a domain of choice and conifgure the necessary RedirectionTarget and Static Route to enable routing from any other Nuage-managed endpoint to this VPC.

### Pre-Configuration on AWS
As part of deploying the NSG-AMI on AWS, you need to upload the NSG-AWS image to S3 and make it available to a Region of your interest.

You also need to set up authentication credentials so the playbooks can access AWS. Credentials for this AWS account can be generated in the [IAM Console](https://console.aws.amazon.com/iam/home). You can create or use an existing user. 

The AWS account needs to be configured for Read/Write access for VPC, EC2 and CloudFormation.

The below snippet shows an Amazon IAM policy that you can assign to the AWS User/Group
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "ec2:*",
            "Effect": "Allow",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "vpc:*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "cloudformation:*",
            "Resource": "*"
        }
    ]
}
```

### Pre-configuration tasks on Ansible Deployment Host

The playbooks relies on the `boto` python library for accessing and configuring the necessary AWS resources. Of the many mechanisms that can be used to pass the AWS Account credentials, the easiest is to define them in a file called  `~/.boto` or `~/.aws/credentials`. Configure it with the `ACCESS_KEY` and `SECRET_KEY` for the Account as configured in previous step: 

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY 
```

### Configuration of `user_creds.yml`
Given that the deployment can take place against a pre-existing Nuage Networks instatllation, the API end-point and VSD credentials are stored in the top-level file `user_creds.yml`.

Example shown below:
```
myvsd:
  auth:
    api_username: csproot
    api_password: csproot
    api_enterprise: csp
    api_url: https://PUBLIC-IP:8443
```

### Example `build_vars.yml` file

Under the `examples` directory, an `build_vars.yml.nsg_ami` is located.
The relevant parameters are shown under `mynsgvs`

```
mynsgvs:
  - { 
      # Name of the NSG, will also be used as the Ansible hostname
      hostname: "l-vpc1-nsgv",
      # target_server_type needs to be configured as "aws"
      target_server_type: "aws",
      # ID of the NSG Template that will be used for the NSG-AWS
      nsg_template_id: "7971ff5b-1ecd-4410-b8cb-b3ab5141d27a",
      # Nuage Enterprise where the NSGateway will be provisioned under
      enterprise: "vns9", 
      # AWS Region
      aws_region: "eu-west-2",
      # Parameters if a pre-existing VPC is to be used to launch the NSG-AMI in. 
      # AWS ENI's need to be pre-created to attach the NSG-AMI to.
      use_vpc: { nsg_lan_eni: "eni-7aad1d37", nsg_wan_eni: "eni-dfa91992" },
      # Parameters to define the AMI and the EC2 instance type for the NSG-AMI. 
      # Optionally the Elastic IP Allocation ID can be specified. If omitted, a new Elastic IP will be requested.
      nsg_ami: { id: "ami-35a4b151", type: "t2.medium", keyname: "VPC-KeyPair", eip_allocid: "eipalloc-d39069ba" } }
  - { 
      # Name of the NSG, will also be used as the Ansible hostname
      hostname: "l-vpc2-nsgv",
      # target_server_type needs to be configured as "aws"
      target_server_type: "aws",
      # ID of the NSG Template that will be used for the NSG-AWS
      nsg_template_id: "7971ff5b-1ecd-4410-b8cb-b3ab5141d27a",
      # Nuage Enterprise where the NSGateway will be provisioned under
      enterprise: "vns9",
      # AWS Region
      aws_region: "eu-west-2",
      # Parameters if a new VPC is to be created to launch the NSG-AMI in.
      # This will also provision route-tables, and security groups
      provision_vpc: { cidr: "10.4.0.0/16", nsg_wan_subnet: "10.4.10.0/24", nsg_lan_subnet: "10.4.20.0/24", private_subnet: "10.4.30.0/24" },
      # Parameters to define the AMI and the EC2 instance type for the NSG-AMI.
      # Optionally the Elastic IP Allocation ID can be specified. If omitted, a new Elastic IP will be requested.
      nsg_ami: { id: "ami-35a4b151", type: "t2.medium", keyname: "VPC-KeyPair" } }
```




## Questions and Issues

Questions should be sent to the Metro team ([via Brian Castelli](mailto://brian.castelli@nokia.com)). Issues should be created using the github Issues feature of the Nuage-Metro repo.
