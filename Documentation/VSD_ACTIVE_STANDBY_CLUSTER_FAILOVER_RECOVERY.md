# VSD active standby cluster failover recovery in Metro&#198;

This procedure is used to convert a GEO-redundant active VSD cluster to standby and standby VSD cluster to active. This requires a GEO-redundant VSD cluster to be already installed with one Active HA Cluster (3 VSDs) and one Standby HA Cluster (3 VSDs). Metro&#198 can be used to install such a setup.

In the deployments, create a deployment with 6 VSDS. First 3 belong to the current primary cluster and the next 3 belong to current standby cluster. Once this is in place, use the following command to convert active cluster to standby and vice versa.
```
metroae vsd_active_standby_failover_recovery [deployment_name]
```

## Questions, Feedback, and Contributing
Ask questions and get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroÆ site](https://devops.nuagenetworks.net/).  
You may also contact us directly.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.
