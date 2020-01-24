# Bootstrapping NSGvs

MetroAE supports the bootstrap of NSGv components while deploying them.  There are two supported methods for bootstrap.

## Supported NSGv Bootstrap Methods
* MetroAE Bootstrap
* External ISO

## MetroAE Bootstrap
MetroAE can perform all of the tasks necessary to bootstrap NSGvs.  A global and per NSGv configuration will be applied to the VSD.  An ISO file is then generated and downloaded for each NSGv.  MetroAE applies each ISO to the corresponding NSGv for bootstrapping during the predeploy role.

To use MetroAE bootstrapping, specify the `bootstrap_method` parameter to be `zfb_metro` in the `nsgvs.yml` deployment file for each NSGv to be bootstrapped by MetroAE.  When using this mode, parameters within the `NSGv Zero-Factor Bootstrap` section of the deployment file must be filled out to provide the required information for the per-NSGv VSD configuration.  In addition, a second deployment file `nsgv_bootstrap.yml` containing the global VSD configuration is required to be provided.  This file contains the global VSD configuration related to bootstrapping such as defining the proxy user, NSG template and VSC infrastructure profile.

## External ISO
An NSGv may be bootstrapped using a provided 3rd-party ISO file.  In this mode, MetroAE assumes any required VSD configuration is already in place.  In the `nsgvs.yml` deployment file, specify the `bootstrap_method` parameter to be `zfb_external` for each NSGv using this mode.  The parameters `iso_path` and `iso_file` are required to provide the path and filename of the ISO file on the MetroAE host.  During the predeploy phase of the NSGv, the provided ISO will be used for bootstrapping.

## Questions, Feedback, and Contributing  
Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).  
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project").  

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
