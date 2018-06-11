# Submitting Your Code and Becoming a Contributor to Nuage Metro Automation Engine
Thank you for your interest! The main steps for submitting your code to Nuage Networks Metro Automation Engine are:  
[1. Develop code on a fork](#1-develop-code-on-a-fork)  
[2. Finalize code contribution](#2-finalize-code-contribution)  
[3. Create pull request (PR)](#3-create-pull-request-pr)  
[4. Address comments and inquiries](#4-address-comments-and-inquiries)  
## Prerequisites / Requirements
All contributions must be consistent with the design of the existing **playbooks** and **roles**, which fall into the following categories:

Playbook/Role | Description
---- | ----
Predeploy | For prerequisites and getting VMs up and running. This is one of two hypervisor-dependent roles (destroy is the other). If you find yourself adding conditional execution based on the hypervisor anywhere else, it's probably a mistake.
Deploy | For installing software, upgrading the OS, and configuring the system.
Postdeploy | For component-level sanity validation.
Health | For system-level sanity validation and monitoring.
Destroy | For tear down of components and connections. This is one of two hypervisor-dependent roles (predeploy is the other). If you find yourself adding conditional execution based on the hypervisor anywhere else, it's probably a mistake.
Upgrade | For upgrading components from one release to another.
## 1. Develop Code on a Fork
1. Before you start developing code, create your own fork from the upstream Metro Automation Engine repo. [https://github.com/nuagenetworks/nuage-metro/](https://github.com/nuagenetworks/nuage-metro/)
2. Clone your own fork on your machine and switch to the _dev_ branch.  
Note: By default the fork clones into `nuage-metro`. Consider creating a separate branch, other than dev, for feature development. Alternatively, you may provide a target dir for the clone, as shown below with `metro-fork`.
```
git clone https://github.com/<your handle>/nuage-metro.git metro-fork/
cd metro-fork/
git checkout dev
```
3. Develop and test all proposed contributions on the appropriate hypervisors in the `metro-fork` directory. If you choose not to provide support for one or more supported hypervisors, you must provide graceful error handling for those types. Testing includes running the program `flake8` over all Python files. The only exception to the flake8 rules that we accept is E501, line length. For example: `flake8 --ignore=E501`.

4. If you require any new User Input Variables:
    * Extend the Metro Automation Engine variable files with sensible example values:<br> `build_vars.yml` and `user_creds.yml`.
    * Ensure that the copies of the variable files in `roles/reset-build/files/` are identical to<br>`build_vars.yml` and `user_creds.yml`.
    * Include comments with the variable specifications that explain the variable's purpose and acceptable values.
    * Variables that are almost never modified may be included in standard Ansible variable locations, e.g. `roles/<rolename>/vars/main.yml`.

5. If you are developing a new role, include a `README.md` at the base folder with a clear description, requirements, dependencies, and example playbook. See also [Ansible Galaxy](https://galaxy.ansible.com/intro) for further best practices.

6. Add a brief description of your bug fix or enhancement to `RELEASE_NOTES.md`.

7. Add your changes to git and do a local code commit:
```
git add .
git commit -m "COMMIT WITH THIS MESSAGE"
```
git tip: Don't use `-am` option to turn the above two statements into one. `-am` means "add, then commit using the supplied message". The problem is `-am` picks up only existing files that have been modified, and ignores new files that have been added. Therefore, use the two statements as shown above.
## 2. Finalize Code Contribution
1. Ensure your personal fork has the latest changes of the [*dev* branch](https://github.com/nuagenetworks/nuage-metro/tree/dev) included. Do this by by adding the upstream code as additional _remote_, fetch the newest upstream code, and _rebase_ your code:
```
git remote add upstream https://github.com/nuagenetworks/nuage-metro.git
git fetch
git rebase upstream/dev
```
This last command shows you if there are any merge-conflicts to manage, or if your tree can be successfully fast-forwarded to the latest commit of the *dev* branch with your changes on top.

2. If necessary, resolve all merge conflicts and retest your code.
3. Push your changes to your own fork:
Note: It is good practice to create feature branches on your fork, push changes from there and create PRs from there.
```
git push origin <name of the branch of your fork>
```
If you had already pushed your code in a previous step as part of development, you may need to add the `--force` parameter to this command to ensure your fork becomes fully aligned with the upstream _dev_ branch history.
## 3. Create Pull Request (PR)
After you have developed and pushed your code into your fork, you may initiate the PR process through the github site:
* Create PRs to the dev branch only. PRs on other branches (eg. the _master_ branch) will be closed without review.
* Include a summary description of the intent of your pull request.
* After you create the PR, go to the github page for the PR and check the code differences to verify that the PR contains your intended changes.

Please consider working with many smaller pull requests instead of one large pull request.
It reduces reviewing time and it gives a gradual evolution of capabilities (instead of step-wise big differences).
## 4. Address Comments and Inquiries
The repo owner will test and review your contributions. After you have addressed any comments or inquiries from the repo owner or other contributors, the repo owner will merge your PR into the `dev` branch.
## Questions and Feedback
Ask questions and get support via email.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.
