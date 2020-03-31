# Contributing to MetroAE

MetroAE is built on a community model. The code has been architected to make contribution simple and straightforward. You are welcome to join in the community to help us continuously improve MetroAE.

The following procedure is the recommended, proven way to become a contributor:

1. [Create your own fork of the nuage-metro repo and make/test your changes there](#1-create-your-own-fork)
2. [Finalize code contribution](#2-finalize-code-contribution)
3. [Create pull request (PR)](#3-create-pull-request-pr)
4. [Address comments and inquiries](#4-address-comments-and-inquiries)

## Prerequisites / Requirements

All contributions must be consistent with the design of the existing workflows.

All contrinbutions must be submitted as pull requests to the _dev_ branch, reviewed, updated, and merged into the nuage-metro repo.

You must have a github.com account and have been added as a collaborator to the nuage-metro repo.

## 1. Create Your Own Fork

1. Before you start developing code, create your own fork from the upstream MetroAE repo. [https://github.com/nuagenetworks/nuage-metro/](https://github.com/nuagenetworks/nuage-metro/)

2. Clone your own fork on your machine and switch to the _dev_ branch.

    Note: By default the fork clones into `nuage-metro`. Consider creating a separate branch, other than dev, for feature development. Alternatively, you may provide a target dir for the clone, as shown below with `metro-fork`.

```
git clone https://github.com/<your handle>/nuage-metro.git metro-fork/
cd metro-fork/
git checkout dev
```

3. Develop your code

    The manner in which you develop the code contribution depends on the extent of the changes. Are you enhancing an existing playbook or role, or are you adding one or more new roles? Making changes to what already exists is simple. Just make your changes to the files that are already there.

    Adding a new component or feature is a bit more involved. For example, if you are adding support for the installation of a new component, the following elements would be expected unless otherwise agreed upon by the repo owners:

    1. A new user-input schema for the component must be created. See the exitsing files in the `schemas` directory.
    2. A new deployment template must be created. See the existing files in the `src/deployment_templates` directory.
    3. Add to the example data. All deployment templates and examples are auto-generated. The data in `src/raw_example_data` is used by the automatic generation to populate the examples properly. Also see the examples that have been auto-generated in the `examples/` directory.
    4. Add your component and associated file references to `src/workflows.yml`.
    5. Add your schema to `src/roles/common/vars/main.yml`.
    6. Execute  `src/generate_all_from_schemas.sh` to create all the required files for your component.
    7. Create the proper roles. The following roles are required unless otherwise agreed to by the repo owners: _newcomponent-predeploy_, _newcomponent-deploy_, _newcomponent-postdeploy_, _newcomponent-health_, and _newcomponent-destroy_ should be created under `src/roles/`
    8. Create the proper playbooks to execute the roles: _newcomponent_predeploy.yml_, _newcomponent_deploy.yml_, _newcomponent_postdeploy.yml_, _newcomponent_health.yml_, and _newcomponent_destroy.yml_ should be created under `src/playbooks/with_build`
    9. Test, modify, and retest until your code is working perfectly.

4. Test all proposed contributions on the appropriate hypervisors in the `metro-fork` directory. If you choose not to provide support for one or more supported hypervisors, you must provide graceful error handling for those types.

5. All python files modified or submitted must successfully pass a `flake8 --ignore=E501` test.

6. Add a brief description of your bug fix or enhancement to `RELEASE_NOTES.md`.

7. Add your changes to git and do a local code commit:

```
git add .
git commit -m "COMMIT WITH THIS MESSAGE"
```

git tip: Use caution when using the `-am` option to turn the above two statements into one. `-am` means "add, then commit using the supplied message". The problem is that `-am` picks up only existing files that have been modified. It ignores new files that have been added and exitsing files that have been deleted.

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

Ask questions and get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).  
You may also contact us directly.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project").  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project"). 

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.
