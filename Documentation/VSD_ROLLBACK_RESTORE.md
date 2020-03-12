# Rolling Back VSD Upgrades
In certain cases, you can use MetroAE to roll-back or restore a VSD configuration outside of the normal upgrade path. 

## Use Cases

If you want to roll back a major upgrade due to failure or bugs in the code, there’s no need to worry. In any event, MetroAE has created a backup during the upgrade. You can roll back that upgrade by: 
  1. Installing new VSDs with the original version 
  2. Restoring the VSD database of that original version
  
If you have a backup that was taken in the past and your database has become corrupt or the VSD VMs are no longer functional, you can use MetroAE to redeploy the VSD VMs and restore the backup to them. 


## Prerequisites

Before rolling back a VSD configuration, you must meet the following prerequisites: 

* The upgrade you are attempting to roll back must be a major upgrade, not a patch upgrade. This procedure will not work for patch upgrades.
Example: Going from version 5.4.1 to 6.0.3 is a major upgrade. Alternatively, going from versions 5.4.1u1 to 5.4.1u7 is a patch upgrade.
* You must have configured your deployment files for the upgrade
  * The “nuage_unzipped_files_dir” variable in common.yml must be set to point to the correct location where the newer image files can be found, e.g. 6.0.3 images.
  * If the original VMs are still on the hypervisor, the VSD VM names must be set to new, unique values. If you are going to completely destroy the original VMs, you can use the same VM names.
  * The upgrade_vmname variable in vsds.yml must be configured for the new VM names for the new nodes, e.g. 6.0.3 nodes.  
* The image files for the original version must be available. In this example case, you must have the image files for 5.4.1 VSD. 
* The deployment should be configured as an installation.
* You must have run the VSD upgrade procedure past the point where the backup of the VSD has been completed. 
  * By default, you can check whether a backup is available in the “backup” subdirectory under the path you specified for the nuage_unzipped_files_dir variable in common.yml. 
  * You can also check under the path you specified for the variable metro_backup_root in upgrade.yml. The latter is an optional variable you might not have defined. If you find the backup, you can proceed with the rollback.
  
## Steps 

If all of these prerequisites and assumptions are true, perform the following steps to restore a VSD configuration: 

#### 1. Shut down all running VSDs. 
   * If the failure was early, terminate manually any VSDs from the original version that are still running.
   * Run the following command to terminate any new VSDs that are running. 
   ````
   metroae destroy vsds <deployment_name>
   ````
  
#### 2. Configure or create a new deployment as if you intend to install the original version. 
  * Set the nuage_unzipped_files_dir variable in common.yml to point to the original version images. In our example, this would be version 5.4.1.
  * Remove upgrade.yml.
  
#### 3. Run the following command to bring up new copies of the original VMs (e.g. 5.4.1).
````
metroae install vsds predeploy
````

#### 4. Manually copy (via scp) the pre-upgrade backup to /opt/vsd/data on VSD 1.


#### 5. Run the following command to start the installation of the VSD software on the VSD VM. This will also restore the backup that you copied to the first VSD.
````
metroae install vsds deploy
````

#### 6. Run the following command to run sanity and connectivity checks on the VSDs: 
````
metroae install vsds postdeploy
````


## You May Also Be Interested in


## Questions, Feedback, and Contributing
Get support via the [forums](https://devops.nuagenetworks.net/forum/) on the [MetroÆ site](https://devops.nuagenetworks.net/).

Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project").

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.

