# Deploying Nuage Networks Components using Terraform and MetroÆ

Nuage Network components can be deployed using [Terraform](https://www.terraform.io/) by allowing the tool to perform the predeploy role while utilizing MetroÆ for deploy and postdeploy roles.  The predeploy role performs the steps to define and spin up VM resources.  The deploy role installs, configures and activates the Nuage Network software on the VM resources.  The postdeploy role provides health checking to ensure that the software is indeed running properly.

## Steps for Deploying using Terraform and MetroÆ
[1. Install Terraform and MetroÆ](#1-install-terraform-and-metroÆ)
[2. Customize MetroÆ Deployment](#2-customize-metroÆ-deployment)
[3. Create Terraform Configuration](#3-create-terraform-configuration)
[4. Add Terraform Provisioners and Dependencies](#4-add-terraform-provisioners-and-dependencies)
[5. Apply Using Terraform](#5-apply-using-terraform)

## 1. Install Terraform and MetroÆ
Both [Terraform](https://www.terraform.io/) and MetroÆ are required to be installed using standard installation procedures.  [Terraform](https://www.terraform.io/) can be installed via the [installation tutorial](https://learn.hashicorp.com/terraform/getting-started/install).  MetroÆ is installed via the [setup guide](SETUP.md).

## 2. Customize MetroÆ Deployment
A set of MetroÆ deployment files is required to provide configuration for MetroÆ to perform the deploy steps.  These should be written as if MetroÆ were to be performing all of the roles of the deployment using the steps described in the [customize deployment](CUSTOMIZE.md) guide.

## 3. Create Terraform Configuration
The [Terraform](https://www.terraform.io/) configuration files are required to describe the required providers and resource definitions to allocate compute nodes for components.  These can be written according to the [build infrastructure](https://learn.hashicorp.com/terraform/getting-started/build) guide.

Note that [Terraform](https://www.terraform.io/) will need to perform all of the steps that MetroÆ would have done during the predeploy role.  These include the following for most VM machine types:
- Define VM resources including number of CPU cores and memory
- Create required dependencies (i.e. disks, networks, etc.)
- Disable cloud-init for the component
- Configure networking for the component
- Set the hostname for the component
- Copy in authorized SSH keys
- Configure autostart for the VM
- Start the VM

## 4. Add Terraform Provisioners and Dependencies
[Terraform](https://www.terraform.io/) will be providing the predeploy role, however, MetroÆ will need to be triggered to perform the deploy and postdeploy roles.  This is accomplished using provisioners.

    resource "<provider>" "vsd1" {
        resource definitions...
        
        provisioner "local-exec" {
            command = "./metroae vsd_deploy"
            working_dir = "<metro-directory>/nuage-metro"
        }

        provisioner "local-exec" {
            command = "./metroae vsd_postdeploy"
            working_dir = "<metro-directory>/nuage-metro"
        }
    }

The provisioners will trigger MetroÆ to execute the deploy and postdeploy roles after the component VM is running.  Provisioners will need to be added for each component to be deployed.

MetroÆ should not be run in parallel and playbooks need to be run in the correct order (i.e. VSDs, VSCs, VSTATS...).  To ensure that this is the case, resources need to be defined using dependencies as follows.

    resource "<provider>" "vsd1" {
        resource definitions...
    }
    resource "<provider>" "vsc1" {
        resource definitions...
        depends_on = [<provider>.vsd1]
    }
    resource "<provider>" "vstat1" {
        resource definitions...
        depends_on = [<provider>.vsd1, <provider>.vsc1]
    }

## 5. Apply Using Terraform
With all of the tools installed and properly configured, [Terraform](https://www.terraform.io/) can perform the entire deployment using apply as described by [change infrastructure](https://learn.hashicorp.com/terraform/getting-started/change).

    terraform plan
    terraform apply
    
## Questions, Feedback, and Contributing
Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).
You may also contact us directly.	Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project").

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.

