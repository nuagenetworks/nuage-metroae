# Deploying Nuage Networks Components in Amazon Web Services (AWS) with MetroAE (limited support)

## Supported Components
MetroAE supports deployment of the following components in AWS.
* VSD
* VSC (as KVM running on an AWS bare-metal instance)
* VSTAT (ElasticSearch)
* VNS Utils
* NSGv

## Main Steps for Deploying in AWS
[1. Install Libraries](#1-install-libraries)
[2. Upload or Import AMIs](#2-upload-or-import-amis)
[3. Setup Virtual Private Cloud](#3-setup-virtual-private-cloud)
[4. Setup Bare Metal Host (for VSC Only)](#4-setup-bare-metal-host-for-vsc-only)
[5. Configure Components](#5-configure-components)
[6. Deploy Components](#6-deploy-components)

## 1. Install Libraries
MetroAE uses the [cloudformation](https://docs.ansible.com/ansible/latest/modules/cloudformation_module.html) Ansible module for deploying components in AWS. This module requires the python-boto and python-boto3 python libraries. Use one of the following three methods to install these required libraries on the MetroAE host.

#### Method 1: pip

    pip install boto
    pip install boto3

#### Method 2: yum

    yum install python-boto
    yum install python-boto3

#### Method 3: apt

    apt-get install python-boto
    apt-get install python-boto3

## 2. Upload or Import AMIs
Amazon Machine Images (AMIs) are used to run instances in EC2. For each Nuage Networks component that you want to deploy (except VSC), you'll need to upload or import an AMI to AWS. The AMI identifiers are provided to MetroAE for deployment. VSC is not supported as an AMI. It must be deployed as KVM running on an AWS bare-metal instance.

## 3. Setup Virtual Private Cloud
Before installing Nuage Networks components, you must define and deploy a virtual private cloud (VPC) in AWS. An example file ([aws-example-vpc.yml](../examples/aws_vpc_examples/aws-example-vpc.yml)) of a basic VPC is provided in the [examples directory](../examples/). This VPC must define the network interfaces that will be used by each component. The VPC should also provide connectivity between various components and Internet access (either directly or outgoing only through NAT). We strongly recommend that you define security policies, IP addressing and DNS. The recommended subnets for each component are defined below. Note that the access subnet is expected to have direct Internet access and the management subnet to have outgoing only access.

Component | Subnet1 | Subnet2
--------- | :---: | :---:
VSD | Mgmt |
VSC | Mgmt | Data
VSTAT | Mgmt |
VNS Util | Mgmt | Data
NSGv | Access | Data

## 4. Setup Bare Metal Host (for VSC Only)
Deploying VSC as a standard AWS component is not supported. Because it relies on the VxWorks operating system, the VSC image cannot be converted to an AMI. Instead, you can run VSC as a KVM instance within an AWS bare-metal server. Follow the steps below to setup the bare-metal host.
#### 1. Install a Linux AMI on the server.
#### 2. Install the libvirt KVM libraries on the server.
#### 3. Start the libvirtd daemon.
#### 4. Setup network connectivity to the VSC.
The AWS bare-metal server does not support bridge interfaces, PCI passthrough, or macvtap. To make connections use the routed network option. The routed networks must be defined in libvirt on the host. Multiple addresses can be supported on a single bare-metal interface by adding secondary IP addresses via the EC2 console and using SNAT and DNAT iptables rules.

## 5. Configure Components
Configuring components for AWS is similar to configuring for other server types. See [CUSTOMIZE.md](CUSTOMIZE.md) for details on standard deployments. The configuration files for AWS deployments require a few additional specifications.
### user_creds.yml
AWS access can be specified as `aws_access_key` and secret keys can be specified as `aws_secret_key`. If AWS access is not specified, values will be taken from the environment variables `AWS_ACCESS_KEY` and `AWS_SECRET_KEY`.

### build_vars.yml
#### For Components Other than VSC
Set `target_server_type` to "aws".

AWS requires that the following fields be specified for all components, except VSC.

- aws_region: The AWS region (i.e. us-east-1)
- aws_ami_id: Identifier for the AMI image to be used for the component
- aws_instance_type: The AWS instance type for the image (i.e. t2.medium)
- aws_key_name: The name of the key pair used for access to the component
- aws_mgmt_eni/aws_data_eni/aws_access_eni: The elastic network interface identifiers from the deployed VPC for each required subnet for the component.

#### For VSC Only
VSC is not supported as a direct AWS component, but it can be deployed by specifying several fields in `build_vars.yml` as shown below.

In the `myvscs` section, set `target_server_type` to "kvm" and `target_server` to the address(es) of the bare-metal host(s).

To support routed network connectivity, specify the following fields.

- mgmt_routed_network_name: The name of the libvirt routed network defined on the bare-metal host to support the mgmt interface of the VSC.
- data_routed_network_name: The name of the libvirt routed network defined on the bare-metal host to support the data interface of the VSC.
- internal_mgmt_ip: The ip address to be assigned to the mgmt interfaces on the VSC itself. This internal address can be NATed to the real address of the bare-metal host using iptables rules.
- internal_ctrl_ip: The ip address to be assigned to the data interfaces on the VSC itself. This internal address can be NATed to the real address of the bare-metal host using iptables rules.

#### Alternative Specification for NSGv Only Deployments
If you'd like to deploy only NSGv (no other components), then MetroÆ can optionally provision a suitable VPC.  You will need to configure the nsgvs.yml file in your deployments subdirectory. For the automatic creation of a test VPC on AWS to host your NSGv, the following parameters must be provided in nsgvs.yml for each NSGv:

- provision_vpc_cidr
- provision_vpc_nsg_wan_subnet_cidr
- provision_vpc_nsg_lan_subnet_cidr
- provision_vpc_private_subnet_cidr

The CIDRs for the VPC, WAN interface, LAN interface and private subnet must be specified. When provisioning a VPC in this way, the elastic network interface identifiers `aws_data_eni` and `aws_access_eni` for the NSGv do not need to be specified as they are discovered from the created VPC. In order to bootstrap the NSGv, specify the bootstrap method as `zfb_aws`; this method assumes that a VSD is fully configured and also requires the NSGv template to be created, with the template id included in build_vars.yml

## 6. Deploy Components
After you have set up the environment and configured your components, you can use MetroAE to deploy your components with a single command.

    ./metroae install_everything

Alternatively, you can deploy individual components or perform individual tasks such as predeploy, deploy and postdeploy. See [DEPLOY.md](DEPLOY.md) for details.
