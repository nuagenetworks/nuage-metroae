# Removing Nuage Networks Components with MetroAG
The main steps for removing a deployment are:
1. [Check existing configuration](#check-existing-configuration)
2. [Remove component(s)](#remove-component(s))  
## Prerequisites / Requirements
Use this procedure when you have previously deployed VSP components and would like to remove all or some of the components and start over.  
## 1. Check Existing Configuration
If you have previously deployed components with MetroAG `build.yml` and your configuration has not changed, you do not need to re-run `build.yml` again in order to remove components. You may proceed to step **2. Remove Component(s)**.  

If you have not previously used `build.yml` to deploy components, or your configuration has changed since, then follow the next two steps to rebuild the environment:   
1. Update `build_vars.yml` to accurately represent your existing configuration.
2. Execute the command:  
```
./metro-ansible build.yml
```  
## 2. Remove Components
You have the option of removing the entire deployment or only specified individual components.
### Remove All Components  
Remove the entire existing deployment with one command as follows:  
```
./metro-ansible destroy_everything.yml
```
Note: you may alternate between `install_everything.yml` and `destroy_everything.yml` as needed.  
### Remove Individual Components  
Alternatively, you can remove individual components (VSD, VSC, VRS, etc) as needed. See VSC example below for details.  
  #### Example Sequence for VSC:
  Configure `build_vars.yml`  
  Run `./metro-ansible build.yml`  
  Run `./metro-ansible install_everything.yml` to deploy VSD, VSC, VRS, etc.  
  Discover that something needs to be changed in the VSCs  
  Run **`./metro-ansible vsc_destroy.yml`** to tear down just the VSCs  
  Edit `build_vars.yml` to fix the problem  
  Run `./metro-ansible build.yml` to pick up the changes to `build_vars.yml`  
  Run `./metro-ansible vsc_predeploy.yml`, `./metro-ansible vsc_deploy.yml`, and `./metro-ansible vsc_postdeploy.yml` to get the VSCs up and running again.  
## Questions, Feedback, and Contributing
Ask questions and get support via email.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](CONTRIBUTING.MD) to Nuage MetroAG by submitting your own code to the project.
