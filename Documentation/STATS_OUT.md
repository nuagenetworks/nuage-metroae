# Installing Nuage Networks Components as a Stats-Out Deployment with MetroAE

## Restrictions
MetroAE supports the installation of a stats-out deployment with the following restrictions:
* VSP version 20.10 or later
* New installation only, no migration
* No support for upgrade of stats-out components

## Installed Components
MetroAE will install a 3 node VSD cluster as is standard in HA deployments.  In addition,
an additional 3 nodes of stats VSDs are installed for stats-out.  Similarly, MetroAE will
install a standard 3 node cluster of VSTATs (ElasticSearch) and an additional 3 nodes of
data VSTATS for stats-out.  If the stats_out_proxy provided is the same as the NUH
internal_ip address, then the NUH will be configured to be used for stats-out.

## Configure Components
Configuring components for stats-out is similar to configuring for other deployments. See
[CUSTOMIZE.md](CUSTOMIZE.md) for details on standard deployments.

### common.yml
Within the common.yml deployment file the following fields should be configured:
* stats_out = Set to true when installing a stats-out deployment.
* stats_out_proxy = Set to the IP address of the proxy to be used between stats-out components.

### vsds.yml
Within the vsds.yml deployment file, 6 entries for VSDs are expected to be
configured when deploying stats-out.  The first 3 are the standard VSD cluster.
The last 3 define the stats VSDs.  In all other ways, VSDs are configured as
they normally would be in any deployment.

### vstats.yml
Within the vstats.yml deployment file, 6 entries for VSTATs (ElasticSearch) are
expected to be configured when deploying stats-out.  The first 3 are the
standard VSTAT cluster.  The last 3 define the data VSTATs.  In all other ways,
VSTATs are configured as they normally would be in any deployment.

## Questions, Feedback, and Contributing
Get support via the [forum](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:devops@nuagenetworks.net "send email to nuage-metro project").

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metroae/issues "nuage-metroae issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
