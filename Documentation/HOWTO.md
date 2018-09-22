# How To Customize and Deploy Various Components

## Prerequisites / Requirements

Before working with Metro Automation Engine, please refer to [README.md](README.md), [SETUP.md](/SETUP.md), and [CUSTOMIZE.md](/CUSTOMIZE.md) for information about supported deployments and general guidelines.

## A Sample of What Metro Automation Engine Can Do  

[1. Customize the Component Mix](#1-customize-the-component-list)   
[2. Deploy VRS on Multiple Target Architecture](#2-deploy-vrs-on-multiple-target-architectures)  
[3. Deploy NSG in AWS](#3-deploy-nsg-in-aws)   

## 1. Customize the Component Mix  
Metro Automation Engine supports customizing the list of components the playbooks operate on. To operationalize two VSCs `build_vars.yml` would contain the following:  
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
      vsc_mgmt_static_route_list: [ 0.0.0.0/1, 128.0.0.1/1 ] }
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
      vsc_mgmt_static_route_list: [ 0.0.0.0/1, 128.0.0.1/1 ] }
```

### Example  
You can use Metro Automation Engine to deploy a VSD cluster by itself. The basic pattern described here applies to deploying only VSD, VSD+VSC, VSD+VSC+VRS, VSC only, VSTAT only, and a number of other combination of list components.

For deploying a VSD cluster, you must define 3 VSD entries in the `myvsds` dictionary in `build_vars.yml`. You must also have the other required definitions in place. Here is an example of the `build_vars.yml` file that deploys a cluster of 3 VSDs:

```
  nuage_zipped_files_dir: "/home/caso/metro/4.0R4/nuage-packed"
  nuage_unzipped_files_dir: "/home/caso/metro/4.0R4/nuage-unpacked"
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

## 2. Deploy VRS on Multiple Target Architectures

Some customer environments use a mix of Debian- and RedHat-family Linux distributions in their compute nodes, where Debian == Ubuntu and Redhat == CentOS or RHEL.

Metro Automation Engine supports deploying VRS onto two target architectures by supporting VRS groups in `build_vars.yml`. The following is an example of deloying VRSs on three target architectures using one 'build_vars.yml' file.

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


## 3. Deploy NSG in AWS  

Metro Automation Engine supports the deployment of NSGs in AWS and configuring those as Network Gateways in a particular enterprise of a Nuage Networks installation.
It assumes the necessary enterprise and NSG template has been preconfigured:

It can either

- use an existing VPC, and attach the network interfaces of the NSG-AMI, or
- provision a new VPC with a set of subnets, and configure some default routing tables and security groups.

After it has been deployed, it is up to the end-user to configure the necessary VPort Bridge in a domain of choice and configure the necessary RedirectionTarget and Static Route to enable routing from any other Nuage-managed endpoint to this VPC.

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
`csproot` is only one example of supported users. Other supported users include the CMS user and those with administrative privileges across all enterprises.
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
      hostname: "l-vpc2-nsgv",
      target_server_type: "aws",
      nsg_template_id: "7971ff5b-1ecd-4410-b8cb-b3ab5141d27a",
      enterprise: "vns9",
      aws_region: "eu-west-2",
      provision_vpc: { cidr: "10.4.0.0/16", nsg_wan_subnet: "10.4.10.0/24", nsg_lan_subnet: "10.4.20.0/24", private_subnet: "10.4.30.0/24" },
\      nsg_ami: { id: "ami-35a4b151", type: "t2.medium", keyname: "VPC-KeyPair" } }
```

## Questions, Feedback, and Contributing

Ask questions and get support via email.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")  

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to Nuage Metro Automation Engine by submitting your own code to the project.
