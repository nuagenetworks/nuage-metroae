# Removing Components with MetroÆ
To remove a deployment:

[1. Check existing deployment](#1-check-existing-deployment)  
[2. Remove components](#2-remove-components)

## Prerequisites / Requirements

Use this procedure when you have previously deployed VSP components and would like to remove all or some of the components and start over.

## 1. Check Existing Deployment

Ensure that all components you wish to be destroyed are specified under your deployment.  See [CUSTOMIZE.md](Documentation/CUSTOMIZE.md) for details about specifying components in a deployment.  If you have already used a deployment configuration to do a deploy or upgrade, the existing configuration does not need to be changed to destroy said deployment.

## 2. Remove Components

You have the option of removing the entire deployment or only specified individual components.

### Remove All Components
Remove the entire existing deployment with one command as follows:
```
metroae destroy_everything
```
Note: you may alternate between `install_everything` and `destroy_everything` as needed.

### Remove Individual Components
Alternatively, you can remove individual components (VSD, VSC, VRS, etc) as needed. See VSC example below for details.
  #### Example Sequence for VSC:
  Configure components under your deployment  
  Run `metroae install_everything` to deploy VSD, VSC, VRS, etc.  
  Discover that something needs to be changed in the VSCs  
  Run **`metroae vsc_destroy`** to tear down just the VSCs  
  Edit `vscs.yml` in your deployment to fix the problem  
  Run `metroae vsc_predeploy`, `metroae vsc_deploy`, and `metroae vsc_postdeploy` to get the VSCs up and running again.

## Questions, Feedback, and Contributing
Ask questions and get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroÆ site](https://devops.nuagenetworks.net/).  

You may also contact us directly.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.
