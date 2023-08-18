# Controlling VSD Services

There are times when you need to stop, start, or restart VSD services. For example, if you have a maintenance window in which you want to move the server that hosts a VSD, MetroAE support for VSD Service manipulation will allow you to cleanly shut down VSD services before the move, then bring the VSD services up after the move. You can use the MetroAE workflows that are provided for these purposes.

## Prerequisites / Requirements

Before attempting to control the VSD services using MetroAE, you must configure a deployment with information about the VSDs. You also must have previously [set up your Nuage MetroAE environment](SETUP.md "link to SETUP documentation") and [customized the environment for your target platform](CUSTOMIZE.md "link to deployment documentation").

## Use of MetroAE Command Line

MetroAE can perform any of the following VSD service workflows using the command-line tool as follows:

    metroae-container vsd services stop [deployment] [options]
    metroae-container vsd services start [deployment] [options]
    metroae-container vsd services restart [deployment] [options]

* `deployment`: Name of the deployment directory containing configuration files.  See [CUSTOMIZE.md](CUSTOMIZE.md)
* `options`: Other options for the tool.  These can be shown using --help.  Also, any options not directed to the metroae-container tool are passed to Ansible.

Note: The VSD services workflows can be used even if you didn't use MetroAE to install or upgrade your VSD deployment.

## Questions, Feedback, and Contributing

Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:devops@nuagenetworks.net "send email to nuage-metro project").

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metroae/issues "nuage-metroae issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
