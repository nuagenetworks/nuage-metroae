# Rolling Back VSD Upgrades
In certain cases, you can use MetroAE to roll-back or restore a VSD configuration outside of the normal upgrade path. 

## Use Cases

A. If you want to rollback a major upgrade due to failure or bugs in the code, there’s no need to worry. In any event, MetroAE has created a backup during the upgrade. You can roll back that upgrade by: 
  1. Installing new VSDs with the original version 
  2. Restoring the VSD database of that original version
  
B. If you have a backup that was taken in the past and your database has become corrupt or the VSD VMs are no longer functional, you can use MetroAE to redeploy the VSD VMs and restore the backup to them. 
