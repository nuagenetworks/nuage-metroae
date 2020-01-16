# VSD cluster failover using MetroAE

You can use this procedure to make the current `standby` VSD cluster the `active` VSD cluster. You can promote the `standby` cluster to `active` when both the `active` and `standby` clusters are in good health. Using the `vsd_force_cluser_failover` flag (see below), you can promote the `standby` cluster even when the `primary` cluster is unhealthy or unreachable.

When you use MetroAE to execute the failover procedure, the vsds.yml file in your deployment must be configured with data for 6 VSDs. The first 3 VSDs (VSDs 1-3 in the vsds.yml file) must correspond to the 3 VSDs that are currently `active` VSD cluster and the second 3 VSDs (VSDs 4-6 in the vsds.yml file) must correspond to the 3 VSDs that are currently `standby`. You can create a new deployment for the failover operation or you can re-use the same deployment that was used by MetroAE to install the active/standby cluster in the first place. It is not required that MetroAE be used to install the active/standby clusters in the first place.

Note that the deployment must be configured for the *current* active/standby situation. You can use this procedure to switch back and forth (failover and failback) your clusters, but the order of VSDs in vsds.yml must be changed between runs *or* you can create separate deployments: One for deactivating the `active` cluster and promoting the `standby` cluster to `active` and one for reversing the operation. 

When your deployment is correct, use the following command to deactivate the current `active` cluster and promote the `standby` cluster to `active`:
```
metroae vsd_cluster_failover [deployment_name]
```
If both clusters are in good shape, your failover will complete successfully. If the current `primary` cluster is in poor health or unreachable, MetroAE will print an error and quit. If you want to ignore these errors and force the current `standby` cluster to become `primary`, use following command:
```
metroae vsd_cluster_failover [deployment_name] -e vsd_force_cluster_failover=yes
```

MetroAE will also execute a health check on the current `standby` cluster. If the health check fails on the `standby` cluster, MetroAE will print an error and quit. If you want to ignore these errors and promote the `standby` cluster anyway, use the following command:
```
metroae vsd_cluster_failover [deployment_name] -e skip_health_check=true
```
Note that you can use both `vsd_force_cluster_failover` and `skip_health_check` on one command:
```
metroae vsd_cluster_failover [deployment_name] -e vsd_force_cluster_failover=yes -e skip_health_check=true
```

## Questions, Feedback, and Contributing
Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).  
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project").  

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
