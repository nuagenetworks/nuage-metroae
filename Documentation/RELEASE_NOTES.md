# Metro Automation Engine Release Notes

## Release 3.0.0

### New Procedures and Improvements

* **Removal of build_vars.yml**  There is no longer a single monolithic configuration file for MetroÆ.  Configuration is specified through *deployments*.  A tool is provided to convert an obsolete build_vars.yml file to a deployment.  See [CUSTOMIZE.md](Documentation/CUSTOMIZE.md) for details on deployments.
* **Removal of `build`**  The user no longer needs to issue the `build` playbook. This will be handled automatically and seamlessly by the MetroÆ tool. MetroÆ also tracks changes and will skip steps not required if configuration is unmodified.
* **Schema validation of deployment data**  All configuration specified in a deployment is automatically validated against json-schema.org schemas. This ensures that all required fields are set and every field has the correct syntax. Any error will be found as early as possible and a specific error message will call out the exact problem.
* **Workflows instead of playbooks**  To simplify usage, the concept of a `playbook` is being replaced by a `workflow`. The .yml extension is no longer required. Thus, issue `vsd_deploy` instead of `vsd_deploy.yml`. The MetroÆ tool is renamed from `metro-ansible` to `metroae`. It now supports different arguments, including `--list` which displays all supported workflows.
* **Cleanup of repo**  The MetroÆ repository has been cleaned. Only tools useful for users are present in the root directory. The internal workings of the tool have been moved to sub-directories like src/.

### Unsupported Components/Operations
The following components/operations are not supported in the beta release.
* dns
* gmv
* mesos
* nsgv bootstrap (install is supported)
* stcv
* vsr
* vrs-vm
* osc-integration
* AWS-based VSTAT upgrade
* upgrade of VRS through VCIN
