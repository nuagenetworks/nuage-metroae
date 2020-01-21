# Removing Components with MetroAE
To remove a deployment:

[1. Check existing deployment](#1-check-existing-deployment)
[2. Remove components](#2-remove-components)

## Prerequisites / Requirements

Use this procedure when you have previously deployed VSP components and would like to remove all or some of the components and start over.

## 1. Check Existing Deployment

Ensure that all components you wish to be destroyed are specified under your deployment.  See [CUSTOMIZE.md](CUSTOMIZE.md) for details about specifying components in a deployment.  If you have already used a deployment configuration to do a deploy or upgrade, the existing configuration does not need to be changed to destroy said deployment.

## 2. Remove Components

You have the option of removing the entire deployment or only specified individual components.

### Remove All Components
Remove the entire existing deployment with one command as follows:
```
metroae destroy everything
```
Note: you may alternate between `metroae install everything` and `metroae destroy everything` as needed.

### Remove Individual Components
Alternatively, you can remove individual components (VSD, VSC, VRS, etc) as needed. See VSC example below for details.
  #### Example Sequence for VSC:
  Configure components under your deployment
  Run `metroae install everything` to deploy VSD, VSC, VRS, etc.
  Discover that something needs to be changed in the VSCs
  Run **`metroae destroy vscs`** to tear down just the VSCs
  Edit `vscs.yml` in your deployment to fix the problem
  Run `metroae install vsc predeploy`, `metroae install vscs deploy`, and `metroae install vscs postdeploy` to get the VSCs up and running again.

## Questions, Feedback, and Contributing
Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).

Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project").

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
