# MetroAE Plugins

Plugins are a way for you to extend the functionality of the Metro Automation Engine without modifying MetroAE code. This allows you to create your own workflows as Ansible roles and have them executed by MetroAE.

## Overview

The overview of the process is:

1. Create the proper files and subdirectories (see below) in a directory of your choosing
1. Package the plugin using the `package-plugin.sh` script
1. Install the plugin using the `metroae-container plugin install` command
1. Add the proper data files, if required, to your deployment directory
1. Execute your role

This process remains the same whether you are using the MetroAE Container or working with a github clone workspace. 

Note that if you are working with the MetroAE Container and you update the container, you will need to reinstall the plugin.

## Operations

MetroAE supports the following operations in support of plugins

### Package a Plugin

To package a plugin, issue:

    ./package-plugin.sh <plugin-directory>

This will create a tarball of the plugin ready for distribution to users.

### Install a Plugin

Users who wish to install the plugin can issue:

    ./metroae-container plugin install <plugin-tarball-or-directory>

This should be issued from the nuage-metro repo or container.  Note that a tarball or unzipped directory can both be installed.

### Uninstall a Plugin

To uninstall a plugin, the user can issue:

    ./metroae-container plugin uninstall <plugin-name>

This should be issued from the nuage-metro repo or container.  Uninstall is by plugin name as all installed files were recorded and will be rolled back.

## Examples

Examples of plugins can be found in the MetroAE `examples` directory. They range from `examples/plugins/simple` which contains a minimal example that does not require user input, e.g., just running a simple Ansible task, to `examples/plugins/full` which takes advantage of MetroAE's schema validation of user inputs, Ansible inventory generation, and more. You can choose the level of support your plugin requires. Ther eis also an intermediate example, `examples/plugins/medium`.

## Authoring Plugins

### Create Workspace

In any location you choose, create a base directory that has the same name as the name of the plugin.  This base directory will serve as the 'root' of your plugin development work. The directory and plugin name should not contain spaces or special characters.  The following directories should be created under the base plugin directory:

- *playbooks*: Set of playbooks for user to issue to initiate plugin features. (required)
- *roles*: Ansible roles implementing the plugin features. (optional)
- *schemas*: Set of schemas defining the deployment data required from the user. (optional)

Upon installation of the plugin, the files in the above directories will be copied and merged into the MetroAE codebase, becoming part of the MetroAE suite.  

Note that the name of the playbooks and roles need not match the name of the plugin. Note also that a single plugin can contain multiple playbooks and roles.

It is best practice that your playbook names match your role names. By convention, MetroAE has adopted the practice of naming playbooks with `_` separators and roles with `-` seperators. For example, `vsd_deploy.yml` is the name of the playbook, and `vsd-deploy` is the name of the corresponding role.  

All file names must be unique to the plugin to prevent conflict with other components of the MetroAE suite. For example, the vsd_deploy.yml playbook already exists within MetroAE. To avoid clobbering this exitsing playbook, your playbook names should be unique.

### Create Plugin Configuration

Each plugin needs a configuration file that describes the general parameters of the plugin.  It must be called `plugin-cfg.yml` and be contained in the base plugin directory.

For the `simple` form of plugin, one that does not require user input or inventory generation, the plugin configuration file can be as simple as:

```
plugin_name: simple
description: |
  Plugin for running ls
version: 1.0.0
required_metro_version: 4.1.0
schemas: []
hooks: []
```

This simple plugin has no defined schemas or hooks, and therefore no user inputs.

A more complete or `full` formm of plugin takes advantage of the many MetroAE features, such as user input validation via JSON schema, Ansible inventory generation, built-in common roles, and more.

A more complete plugin configuration has the following form:

```
plugin_name: full
description: |
  Plugin for demonstration purposes. Installs a Demo VM using only plugin
  functionality.
version: 1.0.0
required_metro_version: 4.1.0
schemas:
  - name: "demovms"
    is_list: yes
    required: no
    encrypted: no
hooks:
  - location: build
    role: common
    tasks: demovm-process-vars
```

Note that this `full` plugin configuration specifies that there will be user inputs that will be validated by a JSON schema with the name `demovms`. This implies that there will be a role created named `demovms` and a user input deployment file named `demovms.yml` that will be parsed at run time.

The specifics of the elements of the plugin configuration are as follows:

- *plugin_name*: The name of the plugin and the base directory. (required)
- *description*: Human-readable description describing the purpose of the plugin. (optional)
- *version*: Version number describing the plugin.  Should be in the form major.minor.patch (required)
- *required_metro_version*: Minimum required version of MetroAE required for this plugin to operate. (required)
- *schemas*: Listing of the schemas provided by the plugin to describe deployment data required from user. (Optional)
  - *name*: Base file name of the schema (no extension)
  - *is_list*: Whether or not the schema describes a list of data sets or is a single object data set.
  - *required*: Whether or not the data from the schema must always be present in the user's deployment set.
  - *encrypted*: Determines whether or not the data contains encrypted fields.
- *hooks*: Describes the MetroAE hook locations where the plugin roles will be executed. (optional)
  - *location*: The name of the MetroAE hook location to execute the role.
  - *role*: The name of the role directory where tasks will be executed.
  - *tasks*: The name of the tasks file where the tasks are defined.

Note that when not specified, `schemas` and `hooks` must be shown as empty lists, i.e., `hooks: []`.

### Create Schema for Required User Data

MetroAE configures workflows using user data sets called `deployments`.  The `deployments` are sets of YAML files grouped together in directories.  The contents of which are to be filled out by the user and validated by json schemas.  The plugin can recieve required user data from the user by defining a set of one or more schemas for the data.  These schemas should be placed
under the `schemas` directory under the base plugin directory and then listed in the `schemas` section of the `plugin-cfg.yml` file as described in the above section.  Care should be taken to keep schema names unique so they do not conflict with the MetroAE Suite or other plugins.  The data from the user will be available during the `build` role and can be used to generate the required Ansible `inventory` for the plugin.

A sample schema is provided in the MetroAE examples.

### Generate Plugin Inventory

In general, there are 3 categories of plugins: Those that do not require additional user inputs to be added to the inventory, those that introduce new hosts that require additional user inputs added to the inventory for those hosts, and those that do not introduce new hosts but need to add custom variables to the inventory for existing hosts.

If your plugin does not require additional user inputs, there is nothing for you to do here.

#### Generate Plugin Inventory for New Host Types

If your plugin introduces new host types that require user input, Ansible requires host_vars files called the `inventory` to provide the configuration for the playbooks that are executed.  You can find an example of this process in `examples\plugins\full`. In MetroAE, the inventory is generated dynamically during the build workflow. The build workflow is executed automatically by the `metroae` script whenever changes to the deployment files are detected. Any host_vars inventory required by the plugin must be generated by a playbook you provide. Your process-vars playbook will be executed via the `build` hook.  This can be accomplished by defining the following hook in the plugin config:

    hooks:
      - location: build
        role: common
        tasks: <plugin_device_name>-process-vars

The `<plugin_device_name>-process-vars` task file must be defined under the `roles/common` directory under the plugin base directory and should implement creating the inventory files for the plugin.  Any data supplied by the user that was defined by schemas is made available to Ansible here.

Device specific host files can be created by the usual means of using role templates and writing them to the host_vars directory.  The `write-host-files` role is paricularly useful for this job.  Special care should be taken to keep any inventory files written unique as the plugin should not conflict with existing MetroAE infrastructure or other plugins.  The master `hosts` file should not be directly edited by the plugin.  However, special functionality has been added where blocks can be appened into master file by setting the special variable `plugin_hosts`.  The contents of `plugin_hosts` will be automatically appened into the master `hosts` file after the build hook for the plugins have been run.  In order to play nicely with other plugins, each plugin should append their contents rather than replace.  Example code:

```
    - name: Append content to plugin hosts
      set_fact:
        plugin_hosts: |
          {{ plugin_hosts }}

          {{ this_plugin_device_hosts }}
```

#### Append Plugin Inventory for Existing Hosts

If your plugin does not add a new host type that requires their own custom inputs but it does require custom inputs that should be applied to an existing host type, you can append the required variables to the inventory for an existing host type. An example of this can be found in `examples\plugins\medium` folder.

In the `medium` example, a new user is added to the VSD. This new user is added via a custom variable `my_new_vsd_user` in the `newcredentials` schema file and is available for use in the custom playbooks and roles. Important thing to note here is that the process-vars playbook that you deliver with the the appending of credentials to the appropriate host_vars file as described here in the  

```
    - name: Append credentials to the component host vars
      blockinfile:
        path: "{{ inventory_dir }}/host_vars/{{ newcredentials.name }}"
        block: "{{ lookup('file', '{{ inventory_dir }}/host_vars/newcredentials') }}"
        insertafter: EOF
```

In this case, then, the Plugin will be executed with `hosts` set to the host type that the role shoudl modify, e.g., `vsds`.

### Create Roles for Plugin

The Ansible roles are where any tasks required for the plugin are to be implemented.  The roles should all be defined under the `roles` directory under the plugin base directory.  These roles will be merged into the MetroAE Suite codebase for the user during plugin installation.  As such, care should be taken that role file names do not conflict with existing roles in MetroAE or
that of other plugins.  Although, directory names can be common and overlapping directories will be merged rather than replaced.  Directories can be nested under each role, this is very common such as `tasks`, `vars` or `templates`.

Roles in plugins act as any other role in Ansible.  The roles can even call other roles from the plugin or from existing MetroAE roles.  Existing roles in the MetroAE engine cannot be edited by a plugin.  Plugins must be exclusively additive.  The roles can be triggered by plugin playbooks or by the hooks functionality.

Example roles are provided in the examples.

### Call Plugin Roles by Playbook or Hooks

The roles of the plugin can be called by playbooks.  Any `workflow` actions that the user can execute from the plugin should be implemented as an Ansible playbook and placed in the `playbooks` directory under the base plugin directory. Care should be taken that the playbook names are unique so they do not conflict with existing MetroAE engine playbooks or playbooks of other plugins.  The playbooks for the plugin act as any other playbook in Ansible.  They can contain hosts from the dynamically created plugin inventory, or existing MetroAE hosts.  They can issue roles from the plugin itself or from existing MetroAE roles.

Existing roles within the MetroAE engine cannot be modified by plugins.  However,plugin roles can be issued by existing roles using hooks.  Hooks can be defined in the `plugin-cfg.yml` file which define which role and tasks file should beexecuted and the hook location where it should be executed.  The MetroAE documentation has more information about hooks, although plugins extend the functionality to seamlessly issue plugin roles rather than executing shell commands.

### Define Menus for Plugin Playbooks

MetroAE defines a menuing system for workflows.  The menus organize content and provide context-specific help.  Plugins can merge their workflows to the master menu by providing a `menu` file under the base plugin directory.  Use of menu options is optional. Care should be taken that menu items do not conflict with existing MetroAE engine menus or menus of other plugins.  The menu items are shell variables that define each menu level.  An example format is as follows:

```
    MENU+=(',install,demovms'  'Install Demonstration VM'  'playbook'  'demovm_predeploy'  ',install')
    MENU+=(',install,demovms,predeploy'  'Pre-deploy install step for Demonstration VM'  'playbook'    'demovm_predeploy'  ',install,demovms')
```

- *First item*: A comma-separated string of each level of the menu item.
- *Second item*: The context-specific help string for the menu item
- *Third item*: The action to perform.  This will almost always be `playbook` to issue a playbook.
- *Forth item*: The parameter for the action.  This will almost always be the playbook name to issue.
- *Fifth item*: The help level to show context-specific help.

### Package and Distribute Plugin

Once all of the steps of plugin development have been successfully developed, the plugin can be packaged.  The packaging is described at the top of this document. The result of packaging is a zipped tarball.  The tarball can be distributed to users by any means.  The user can install or uninstall the plugin using the procedure defined at the top of this document.
