# How to Submit Your Code and Become a Contributor to nuage-metro
Thank you for your interest! Please follow the guidelines below for contributing to the nuage-metro project.
## Playbook Design
All contributions must be consistent with the design of the existing playbooks and roles. Playbooks and roles fall into the folllowing categories:
* **Predeploy** - For prerequisites and getting VMs up and running. This is one of two hypervisor-dependent roles (destroy is the other). If you find yourself adding conditional execution based on the hypervisor anywhere else, it's probably a mistake.
* **Deploy** - For installing software, upgrading the OS, and configuring the system.
* **Postdeploy** - For component-level sanity validation.
* **Health** - For system-level sanity validation and monitoring.
* **Destroy** - For tear down of components and connections. This is one of two hypervisor-dependent roles (predeploy is the other). If you find yourself adding conditional execution based on the hypervisor anywhere else, it's probably a mistake.
* **Upgrade** - For upgrading components from one release to another.
* **Rollback** - For restoring components to their previous version if an upgrade fails.

## Submitting Code
### Before You Create a Pull Request
* Create your own fork from the [*dev* branch](https://github.com/nuagenetworks/nuage-metro/tree/dev) of nuage-metro.
* Develop and test all proposed contributions on the appropriate hypervisors.
* If you choose not to provide support for one or more supported hypervisors, you must provide graceful error handling for those types.
* Requirements for User Input Variables
 * Include all variables that can be modified by a user in one of the variable files:`build_vars.yml`, `upgrade_vars.yml`, and `user_creds.yml`.
 * Ensure that the copies of the variable files in `roles/reset-build/files/` are identical to `build_vars.yml`, `upgrade_vars.yml`, and `user_creds.yml`.
 * Include comments with the variable specifications that explain the variable's purpose and acceptable values.
 * Variables that are almost never modifed may be included in standard Ansible variable locations, e.g. `vars/main.yml`.
* Update (merge) your personal fork from the latest dev branch.
* Push your changes to your own fork.
* Add a brief description of your bug fix or enhancement to `RELEASE_NOTES.md` and to the `What's New` section of `README.md`.

### Create a Pull Request
* You may initiate PRs from your personal fork.
* Create PRs to the dev branch only. PRs on other branches (i.e. the master branch) will be closed without review.
* Include tests for new functionality.

### After You Create a Pull Request
* Before your PR is merged into the dev branch the repo owner will test and review it.
* Any comments or inquiries from the repo owner or other contributors must be addressed before the PR will be merged to the dev branch.

## Other Ways to Contribute
Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

 You may also ask questions and get support on the [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project") mailing list.
