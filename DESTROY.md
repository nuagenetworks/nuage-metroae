# Removing an Existing Deployment
If you have previously deployed VSP components and would like to remove the existing deployment and start over, follow the steps below.

## Check Existing Configuration
Ensure that `build_vars.yml` accurately represents your existing configuration. If it does not, follow the steps below: 
1. Edit `build_vars.yml` as needed
2. Execute the command: `./metro-ansible build.yml`  
## Remove Components
When `build_vars.yml` is accurate and you've run `./metro-ansible build.yml` you have the option of removing the entire deployment or only specified individual components.
### All Components  
Remove the entire existing deployment with one command as follows:  `./metro-ansible destroy_everything.yml`
### Individual Components  
Remove individual components (VSD, VSC, VRS, etc) as needed. See VSC example below for details.  
  #### Example Sequence for VSC:
  Configure `build_vars.yml`  
  Run `./metro-ansible build.yml`  
  Run `./metro-ansible install_everything.yml` to deploy VSD, VSC, VRS, etc.  
  Discover that something needs to be changed in the VSCs  
  Run **`./metro-ansible vsc_destroy.yml`** to tear down just the VSCs  
  Edit `build_vars.yml` to fix the problem  
  Run `./metro-ansible build.yml` to pick up the changes to `build_vars.yml`  
  Run `./metro-ansible vsc_predeploy.yml`, `./metro-ansible vsc_deploy.yml`, and `./metro-ansible vsc_postdeploy.yml` to get the VSCs up and running again.


---
Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

 You may also ask questions and get support on the [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project") mailing list.
