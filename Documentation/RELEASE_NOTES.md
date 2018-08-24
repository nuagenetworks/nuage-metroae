# Metro Automation Engine Release Notes
## Release 2.4.X
### New Features and Enhancements
* Improve integration with OpenStack controller, primarily by speeding up lab-installs of Nuage and OpenStack
### Resolved Issues
*

## Release 3.0.0

### New Procedures and Improvements

* **Deprecation of build_vars.yml.**  There is no longer a single monolithic configuration file for MetroAG.  Configuration is specified through "deployments".  A tool is provided to convert an obsolute build_vars.yml file to a deployment.  See [Customization](Documentation/CUSTOMIZATION.md) for details on deployments.
* **Deprecation of `build`.**  The user no longer needs to issue the `build` playbook.  This will be handled automatically and seamlessly by the MetroAG tool.  MetroAG also tracks changes and will skip steps not required if configuration is unmodified.
* **Schema validation of deployment data.**  All configuration specified in a deployment is automatically validated against json-schema.org schemas.  This ensures that all required fields are set and every field has the correct syntax.  Any error will be found as early as possible and a specific error message will call out the exact problem.
* **Workflows instead of playbooks.**  In order to simplify usage, the concept of `playbook` is being replaced by a `workflow`.  The .yml extension is no longer required.  Thus, issue `vsd_deploy` instead of `vsd_deploy.yml`.  The MetroAG tool is renamed from `metro-ansible` to `metroag`.  It now supports different arguments, including `--list` which displays all supported workflows.
* **Cleanup of repo.**  The MetroAG repository has been cleaned.  Only tools useful for users are present in the root directory.  The internal workings of the tool have been moved to sub-directories like src/.
