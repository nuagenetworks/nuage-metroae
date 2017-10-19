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

## Developing and Submitting Code

### Developing your code on a fork

* Before you start your development, create your own fork from the upstream Metro repo [https://github.com/nuagenetworks/nuage-metro/](https://github.com/nuagenetworks/nuage-metro/) 
* Clone your own fork on your machine and switch to _dev_ branch
```
git clone https://github.com/<your handle>/nuage-metro.git metro-fork/
cd metro-fork/
git checkout dev
```

* Develop and test all proposed contributions on the appropriate hypervisors in the `metro-fork` directory. 
  If you choose not to provide support for one or more supported hypervisors, you must provide graceful error handling for those types.

* If you are requiring any new User Input Variable:
    * Extend the Metro variable files with sensible example values: `build_vars.yml`, `upgrade_vars.yml`, and `user_creds.yml`.
    * Ensure that the copies of the variable files in `roles/reset-build/files/` are identical to `build_vars.yml`, `upgrade_vars.yml`, and `user_creds.yml`.
    * Include comments with the variable specifications that explain the variable's purpose and acceptable values.
    * Variables that are almost never modifed may be included in standard Ansible variable locations, e.g. `vars/main.yml`.

* If you are developing a new role, ensure to include a `README.md` at the base folder with a clear desription, requirements, dependencies, and example playbook. See also the [ansible-galaxy](https://galaxy.ansible.com/intro) for further best-practices.

* Add a brief description of your bug fix or enhancement to `RELEASE_NOTES.md`.

* Add your changes to git and do a local code commit:
``` 
git add .
git commit -am "SHORT DESCRIPTION OF THIS COMMIT"
``` 

### Finalizing your code contribution

* Ensure your personal fork has the latest changes of the [*dev* branch](https://github.com/nuagenetworks/nuage-metro/tree/dev) included. Do this by by adding the upstream code as additional _remote_, fetch the newest upstream code, and _rebase_ your code:
```
git remote add upstream https://github.com/nuagenetworks/nuage-metro.git
git fetch
git rebase upstream/dev
``` 

* This last command will show you if there are any merge-conflicts to manage, or if your tree can be successfully fast-forwarded to the latest commit of the *dev* branch with your changes on top.
* If necessary, solve all merge conflicts and re-test your code.

* Push your changes to your own fork:
```
git push origin dev
``` 
In case you already pushed your code in a previous step as part of devleopment, you may have to add the `--force` parameter to this command to ensure your fork becomes fully aligned with the upstream _dev_ branch history.


### Create a Pull Request (PR)

Once you have developed and pushed your code into your fork, you may initiate the PR process through github site:
* Create PRs to the dev branch only. PRs on other branches (eg. the _master_ branch) will be closed without review.
* Include a summary description of the intent of your pull request.

Please consider to work with many smaller pull-requests instead of one large pull-request.
It reduces reviewing time and it gives a gradual evolution of capabilities (instead of step-wise big differences). 

### After You Create a Pull Request
* Before your PR is merged into the dev branch the repo owner will test and review it.
* Any comments or inquiries from the repo owner or other contributors must be addressed before the PR will be merged to the dev branch.

## Other Ways to Contribute
Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

 You may also ask questions and get support on the [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project") mailing list.
