# MetroAE Plugins

Plugins are a way for you to extend the functionality of the Metro Automation Engine without modifying MetroAE code. This allows you to create your own workflows and have them executed by MetroAE.

## Package a Plugin

To package a plugin, issue:

    ./package-plugin.sh <plugin-directory>

This will create a tarball of the plugin ready for distribution to users.

## Install a Plugin

Users who wish to install the plugin can issue:

    ./metroae plugin install <plugin-tarball-or-directory>

This should be issued from the nuage-metro repo or container.  Note that
a tarball or unzipped directory can both be installed.

## Uninstall a Plugin

To uninstall a plugin, the user can issue:

    ./metroae plugin uninstall <plugin-name>

This should be issued from the nuage-metro repo or container.  Uninstall
is by plugin name as all installed files were recorded and will be rolled back.

## Authoring Plugins

### Create Workspace

Create a base directory that is the name of the plugin.  It is best for this
not to contain spaces or special characters.  The following directories
should be contained under the base plugin directory:

- *playbooks*: Set of playbooks for user to issue to initiate plugin features.
- *roles*: Ansible roles implementing the plugin features.
- *schemas*: Set of schemas defining the deployment data required from the user.

Upon installation of the plugin, the files in the above directories will be
copied and merged into the user's codebase and become a part of the MetroAE
engine.  All file names must be unique to the plugin to prevent conflict with
the MetroAE engine itself or other plugins.

### Create Plugin Configuration

Each plugin needs a configuration file that describes the general parameters
of the plugin.  It must be called `plugin-cfg.yml` and be contained in the base
plugin directory.  The plugin configuration has the following form:

    plugin_name: demonstration
    description: |
      Plugin for demonstration purposes. Installs a VNSUtil VM using only plugin
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

- *plugin_name*: The name of the plugin and the base directory.
- *description*: Human-readable description describing the purpose of the plugin.
- *version*: Version number describing the plugin.  Should be in the form major.minor.patch
- *required_metro_version*: Minimum required version of MetroAE required for this plugin to operate.
- *schemas*: Listing of the schemas provided by the plugin to describe deployment data required from user.
    - *name*: Base file name of the schema (no extension)
    - *is_list*: Whether or not the schema describes a list of data sets or is a single object data set.
    - *required*: Whether or not the data from the schema must always be present in the user's deployment set.
    - *encrypted*: Determines whether or not the data contains encrypted fields.
- *hooks*: Describes the MetroAE hook locations where the plugin roles will be executed.
    - *location*: The name of the MetroAE hook location to execute the role.
    - *role*: The name of the role directory where tasks will be executed.
    - *tasks*: The name of the tasks file where the tasks are defined.

### Create Schema for Required User Data

MetroAE configures workflows using user data sets called `deployments`.  The
`deployments` are sets of YAML files grouped together in directories.  The
contents of which are to be filled out by the user and validated by json
schemas.  The plugin can recieve required user data from the user by defining
a set of one or more schemas for the data.  These schemas should be placed
under the `schemas` directory under the base plugin directory and then listed
in the `schemas` section of the `plugin-cfg.yml` file as described in the
above section.  Care should be taken to keep schema names unique so they do not
conflict with the MetroAE engine or other plugins.  The data from the user will
be available during the `build` role and can be used to generate the required
Ansible `inventory` for the plugin.

### Generate Plugin Inventory

Ansible requires hosts files called the `inventory` to provide the
configuration for the playbooks that are executed.  In MetroAE, the inventory
is generated dynamically during the build workflow.  Any inventory required by
the plugin must also be generated via the `build` hook.  This can be accomplished
by defining the following hook in the plugin config:

    hooks:
      - location: build
        role: common
        tasks: <plugin_device_name>-process-vars

The `<plugin_device_name>-process-vars` task file must be defined under the
common role directory under the plugin base directory and should implement the
inventory requirements for the plugin.  Any data supplied by the user that was
defined by schemas is available here.

Device specific host files can be created by the usual means of using role
templates and writing them to the host_vars directory.  The `write-host-files`
role is paricularly useful for this job.  Special care should be taken to
keep any inventory files written unique as the plugin should not conflict with
existing MetroAE infrastructure or other plugins.  The master `hosts` file
should not be directly edited by the plugin.  However, special functionality
has been added where blocks can be appened into master file by setting the
special variable `plugin_hosts`.  The contents of `plugin_hosts` will be
automatically appened into the master `hosts` file after the build hook for
the plugins have been run.  In order to play nicely with other plugins, each
plugin should append their contents rather than replace.  Example code:

    - name: Append content to plugin hosts
      set_fact:
        plugin_hosts: |
          {{ plugin_hosts }}

          {{ this_plugin_device_hosts }}

### Create Roles for Plugin

The Ansible roles can be written and where any tasks required for the plugin are
to be implemented.  The roles should all be defined under the `roles` directory
under the plugin base directory.  These roles will be merged into the MetroAE
codebase for the user during plugin installation.  As such, care should be
taken that role file names do not conflict with existing roles in MetroAE or
that of other plugins.  Although, directory names can be common and overlapping
directories will be merged rather than replaced.  Directories can be nested
under each role, this is very common such as `tasks`, `vars` or `templates`.

Roles in plugins act as any other role in Ansible.  The roles can even call
other roles from the plugin or from existing MetroAE roles.  Existing roles
in the MetroAE engine cannot be edited by a plugin.  Plugins must be exclusively
additive.  The roles can be triggered by plugin playbooks or by the hooks
functionality.

### Call Plugin Roles by Playbook or Hooks

The roles of the plugin can be called by playbooks.  Any `workflow` actions
that the user can execute from the plugin should be implemented as an Ansible
playbook and placed in the `playbooks` directory under the base plugin directory.
Care should be taken that the playbook names are unique so they do not conflict
with existing MetroAE engine playbooks or playbooks of other plugins.  The
playbooks for the plugin act as any other playbook in Ansible.  They can
contain hosts from the dynamically created plugin inventory, or existing
MetroAE hosts.  They can issue roles from the plugin itself or from existing
MetroAE roles.

Existing roles within the MetroAE engine cannot be modified by plugins.  However,
plugin roles can be issued by existing roles using hooks.  Hooks can be defined
in the `plugin-cfg.yml` file which define which role and tasks file should be
executed and the hook location where it should be executed.  The MetroAE documentation
has more information about hooks, although plugins extend the functionality to
seamlessly issue plugin roles rather than executing shell commands.

### Define Menus for Plugin Playbooks

MetroAE defines a menuing system for workflows.  The menus organize content and
provide context-specific help.  Plugins can merge their workflows to the master
menu by providing a `menu` file under the base plugin directory.  Care should
be taken that menu items do not conflict with existing MetroAE engine menus or
menus of other plugins.  The menu items are shell variables that define each
menu level.  An examlpe format is as follows:

    MENU+=(',install,demovms'  'Install Demonstration VM'  'playbook'  'demovm_predeploy'  ',install')
    MENU+=(',install,demovms,predeploy'  'Pre-deploy install step for Demonstration VM'  'playbook'    'demovm_predeploy'  ',install,demovms')

- *First item*: A comma-separated string of each level of the menu item.
- *Second item*: The context-specific help string for the menu item
- *Third item*: The action to perform.  This will almost always be `playbook` to issue a playbook.
- *Forth item*: The parameter for the action.  This will almost always be the playbook name to issue.
- *Fifth item*: The help level to show context-specific help.

### Package and Distribute Plugin

Once all of the steps of plugin development have been successfully developed, the
plugin can be packaged.  The packaging is described at the top of this document.
The result of packaging is a zipped tarball.  The tarball can be distributed to
users by any means.  The user can install or uninstall the plugin using the
procedure defined at the top of this document.
