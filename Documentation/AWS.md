# Deploying Nuage Networks Components in Amazon Web Services (AWS) with MetroAG (limited support)

## Support

The following components are supported for deployment on AWS:

- VSD
- VSTAT (elastic search)
- VNS Utils
- NSGv

The VSC is not currently supported for deployment in AWS.  The VSC image cannot be converted to an AMI due to the use of VxWorks as its operating system.  Using "nested virtualization" (deploying a VM inside a VM) is also not supported by AWS.  Thus, deploying the VSC as a KVM image on a hypervisor in an AWS EC2 instance has not been successful.  The VSC may be able to be deployed on the "bare metal" service soon to be released by AWS.  However, this has not yet been attempted by the MetroAG team and is not officially supported.

## Installation Steps

1. Install prerequisites
2. Upload or import Nuage AMI images
3. Setup AWS Virtual Private Cloud (VPC)
4. Configure components in build_vars.yml
5. Deploy using MetroAG

## Prerequisite installation

MetroAG uses the cloudformation Ansible module for deploying to AWS.  This module requires the python-boto and python-boto3 python libraries.  These should be installed on the MetroAG host using pip, yum or apt.

    pip install boto
    pip install boto3

OR

    yum install python-boto
    yum install python-boto3

OR

    apt-get install python-boto
    apt-get install python-boto3

## Upload or import Nuage component AMI images

AWS uses Amazon Machine Image (AMI) as the format to run instances in EC2.  An AMI for each Nuage component has to be uploaded or imported into AWS.  The AMI identifiers are provided to MetroAG for deployment.

## Setup an AWS Virtual Private Cloud

MetroAG requires a VPC to be defined and deployed in AWS before installing any Nuage components.  An example aws-example-vpc.yml is provided as a basic VPC in the examples directroy.  The VPC must define the network interfaces to be used by each component.  It should also provide connectivity between various components and Internet access (either directly or outgoing only through NAT).  It is strongly recommended to define security policies, IP addressing and DNS as well.  The following define the recommended subnets for each component.  Note that the Access subnet is expected to have direct Internet access and the management subnet has outgoing only access.

Component | Subnet1 | Subnet2
--------- | :---: | :---:
VSD | Mgmt |
VSC | Mgmt | Data
VSTAT | Mgmt |
VNS Util | Mgmt | Data
NSGv | Access | Data

## Configure components in build_vars.yml

Configuring components for AWS is very similar as other server types.  The
target_server_type is "aws" and other fields are specified as normal.  AWS does
require the following extra fields to be specified:

- aws_region: The AWS region (i.e. us-east-1)
- aws_ami_id: Identifier for the AMI image to be used for the component
- aws_instance_type: The AWS instance type for the image (i.e. t2.medium)
- aws_key_name: The name of the key pair used for access to the component
- aws_mgmt_eni/aws_data_eni/aws_access_eni: The elastic network interface identifiers from the deployed VPC for each required subnet for the component.

In addition the AWS access and secret keys can be specified as aws_access_key
and aws_secret_key in user_creds.yml.  If not specified, they will be taken
from the environment variables AWS_ACCESS_KEY and AWS_SECRET_KEY.

## Deploy using MetroAG

After satisfying all the prerequites and configuring components, MetroAG can
be issued as normal.

    ./metro-ansible install_everything

Splitting up the tasks using predeploy, deploy and postdeploy also work.

## NSGv only provision VPC

For the NSGv component, a special workflow is provided that can deploy an AWS
VPC for that component only.  The can be used when it is desired to install
NSGv in AWS only without other components.  The following configuration can
be specified for each NSGv in mynsgvs in build_vars.yml to provision the VPCs:

    provision_vpc: {
        cidr: "10.4.0.0/16",
        nsg_wan_subnet: "10.4.10.0/24",
        nsg_lan_subnet: "10.4.20.0/24",
        private_subnet: "10.4.30.0/24" }

The CIDRs for the VPC, WAN interface, LAN interface and private subnet are
required to be specified.  When provisioning a VPC in this way, the elastic
network interface identifiers aws_data_eni and aws_access_eni for the NSGv do
not need to be specified as they are discovered from the created VPC.
