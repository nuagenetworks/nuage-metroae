# Contributing to MetroAE

MetroAE is built on a community model. The code has been architected to make contribution simple and straightforward. You are welcome to join in the community to help us continuously improve MetroAE.

## We Use [Github Flow](https://guides.github.com/introduction/flow/index.html), So All Code Changes Happen Through Pull Requests
Pull requests are the best way to propose changes to the codebase (we use [Github Flow](https://guides.github.com/introduction/flow/index.html)). We actively welcome your pull requests:

1. Fork the repo and create your branch from `dev`.
2. If you've added code that should be tested, add tests.
3. Make sure your code passes flake8.
4. Issue that pull request!

## Prerequisites / Requirements

  All contributions must be consistent with the design of the existing workflows.

  All contrinbutions must be submitted as pull requests to the _dev_ branch, reviewed, updated, and merged into the nuage-metroae repo.

  You must have a github.com account and have been added as a collaborator to the nuage-metroae repo.

## Contributing your code

1. Developing your code.

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

2. Test all proposed contributions on the appropriate hypervisors in the `metro-fork` directory. If you choose not to provide support for one or more supported hypervisors, you must provide graceful error handling for those types.

3. All python files modified or submitted must successfully pass a `flake8 --ignore=E501` test.

4. Add a brief description of your bug fix or enhancement to `RELEASE_NOTES.md`.

## Any contributions you make will be under the APACHE 2.0 Software License
  In short, when you submit code changes, your submissions are understood to be under the same [APACHE License 2.0](https://www.apache.org/licenses/LICENSE-2.0) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issues](https://github.com/nuagenetworks/nuage-metroae/issues)
  We use GitHub issues to track public bugs.

## Write bug reports with detail, background, and sample code

  **Great Bug Reports** tend to have:

  - A quick summary and/or background
  - Steps to reproduce
    - Be specific!
    - Give sample code if you can.
  - What you expected would happen
  - What actually happens
  - Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Use a Consistent Coding Style

  * 4 spaces for indentation rather than tabs
  * 80 character line length
  * TODO

## License
  By contributing, you agree that your contributions will be licensed under its APACHE 2.0 License.


## Questions and Feedback

Ask questions and get support on the [MetroAE site](https://devops.nuagenetworks.net/).  
You may also contact us directly.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:devops@nuagenetworks.net "send email to nuage-metro project").  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project").

## References
  This document was adapted from the open-source contribution guidelines for [Facebook's Draft](https://github.com/facebook/draft-js/blob/a9316a723f9e918afde44dea68b5f9f39b7d9b00/CONTRIBUTING.md)
