# How to become a contributor and submit your code to nuage-metro

Thank you for your interest in contributing!

The following is a set of guidelines for contributing to the nuage-metro project.

## Summary

- All contributions must be made via pull request (PR) to the *dev* branch. PRs on other branches will be closed without review.
- PRs may be initiated from your personal branch or fork.
- Your personal branch or fork must be updated (merged) from the latest dev branch prior to initiating the PR. 
- The repo owner will review your PR prior to merge into the dev branch.
- Comments from the repo owner and other contributors must be answered prior to merge to dev.
- All contributions must be tested on appropriate target servers, e.g. KVM or ESX.
- Questions and support can be found on the `nuage-metro-interest@list.nokia.com` mailing list.

## User input

All variables that can be modified by a user must be included in one of the variable files: `build_vars.yml`, `upgrade_vars.yml`, and `user_vars.yml`.
The variable specifications must include comments that explain the variable's purpose and acceptable vallues. Variables that are almost never modified may be included
in standard Ansible variable locations.

## Playbook Design

All contributions must be consistent with the deisgn of existing playbooks and roles. Specifically, playbooks and roles fall into one
of the following categories:

- Predeploy - For prerequisites and getting VMs up and running. This is one of two hypervisor-dependent roles (destroy is the other). If you find yourself adding conditional execution based on kvm or vcenter anywhere else, it's probably a mistake.
- Deploy - For installing software, upgrading the OS, and configuring the system.
- Postdeploy - For component-level sanity validation.
- Health - For system-level sanity validation and monitoring.
- Destroy - For tear down of components and connections. This is one of two hypervisor-dependent roles (predeploy is the other). If you find yourself adding conditional execution based on kvm or vcenter anywhere else, it's probably a mistake.
- Upgrade - For upgrading components from one release to another.
- Rollback - For restoring components to their previous version if an upgrade fails.

## Reporting bugs and enhancement requests

You can contribute to nuage-metro by reporting bugs you find and suggesting new features and enhancements. These should be initiated
via the Github Issues feature. You can also look for help on the `nuage-metro-interest@list.nokia.com` mailing list.
