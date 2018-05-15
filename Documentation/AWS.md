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

