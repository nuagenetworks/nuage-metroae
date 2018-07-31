# Metro Automation Engine Release Notes
## Release 2.4.X
### New Features and Enhancements
* Improve integration with OpenStack controller, primarily by speeding up lab-installs of Nuage and OpenStack
* add playbook to copy qcow2 files before predeploy step, add checks in predeploy step for qcow2 existence if skipCopyImages is set
### Resolved Issues
* removed redundant check for netaddr package
