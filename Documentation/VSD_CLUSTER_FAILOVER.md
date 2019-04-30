# VSD cluster failover using MetroÆ

This procedure is used to execute a VSD cluster failover for an active/standby VSD cluster pair. When executed, the active VSD cluster will be 'deactivated' to standby and the standby VSD cluster will be promoted to active. This requires that an active/standby cluster pair to be already installed with one Active HA Cluster (3 VSDs) and one Standby HA Cluster (3 VSDs). Note that MetroÆ can be used to install the initial active/standby cluster pair, a.k.a. a geo-redundant cluster.

For failover to work properly, you must have a deployment configured for all 6 VSDs, 3 for the active cluster and 3 for the standby cluster. This can be the same deployment that was used to have MetroÆ install the active/standby cluster pair. With this requirement satisfied, use the following command to deactivate the current active cluster and promote the standby cluster to active:
```
metroae vsd_cluster_failover [deployment_name]
```
Note that the first thing MetroÆ will do is check the health of the primary cluster before deactivating it. If the active cluster is unreachable or otherwise unhealthy, this check will fail and MetroÆ will quit. If you want to go ahead with the procedure anyway in order to promote the current standby cluster to active, you can tell MetroÆ to skip the health check of the active cluster using following command:
```
metroae vsd_cluster_failover [deployment_name] -e ignore_vsd_deactivation_error=yes
```

MetroÆ will also execute a health check on the current standby cluster. If the health check fails on the standby cluster, MetroÆ will quit. To override and promote the standby cluster anyway, use the following command:
```
metroae vsd_cluster_failover [deployment_name] -e skip_health_check=true
```

## Questions, Feedback, and Contributing
Ask questions and get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroÆ site](https://devops.nuagenetworks.net/).  
You may also contact us directly.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.
