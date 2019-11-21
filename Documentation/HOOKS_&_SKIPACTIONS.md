# Hooks and Skip Actions
MetroAE allows fine-grained control of operations via its hierarchical design. You have the option to execute workflows such as `install_everything` when you just want the simplicity of allowing MetroAE to handle the details. In some situations, however, you may want to take advantage of fine-grained control such as individually executing the workflows `vsd_predeploy`, `vsd_deploy`, and `vsd_postdeploy`.

One of the reasons to take advantage of fine-grained control is so that you can execute your own scripts for verification and configuration between MetroAE's steps. Another is so that you can skip a workflow entirely, using your own tooling to bring up the VSD VM instead of using `vsd_predeploy`, for example. Hooks have been added to simplify and automate the former. Skips have been added to simplify and automate the latter. 

## Hooks
Hooks are predefined locations that preceed specific MetroAE worflows. They can be thought of as places in the code where MetroAE can execute commands on your behalf. These commands can be any executable available on the Ansible host. If the command is a script, it has access to the full range of MetroAE's Ansible variable, e.g. `echo {{ hostvars[inventory_hostname].name }}`. As you can see, your script should use standard Ansible Jinja2 variable syntax. Each predefined location comes immediately before selected low-level MetroAE workflows. Defining a command or script to run at a specific location means that the command or script will run before the workflow is executed.

### Hooks File
A Hooks file is a YAML file that contains the name of the MetroAE workflow that is the location of the hook and the command or script that will be executed before the workflow is executed. The path to a Hooks file is specified in the optional `hooks` section of the deployment file for the component being operated on, e.g. `vsds.yml`.

Here is an example of a Hooks file that specifies a script to execute prior to running the `vstat_predeploy` workflow:
```
`location: vstat_predeploy`
`command: "/tmp/myfiles/myscript.sh"`
```
!! Can we specify more than one command per location? !!
!! What happens if the command or script fails? !!

### Workflow Hook Locations
The following Nuage component workflows have hook support.

#### Installation Workflow Hook Locations
```
vsd_predeploy
vsd_deploy
vsd_postdeploy
vsc_predeploy
vsc_deploy
vsc_postdeploy
vstat_predeploy
vstat_deploy
vstat_postdeploy
vnsutil_predeploy
vnsutil_deploy
vnsutil_postdeploy
nsgv_predeploy
nsgv_postdeploy
vsd_vns_postdeploy
vsc_vns_postdeploy
vcin_predeploy
vcin_deploy
vcin_destroy
vrs_predeploy
vrs_deploy
vrs_postdeploy
vrs_destroy
```

#### Upgrade Workflow Hook Locations
```
upgrade_vsds
upgrade_vsds_inplace
upgrade_vsds_inplace_dbbackup
vsc_ha_upgrade_backup_and_prep_1
vsc_ha_upgrade_backup_and_prep_2
vsc_ha_upgrade_deploy_1
vsc_ha_upgrade_deploy_2
vsc_ha_upgrade_postdeploy_1
vsc_ha_upgrade_postdeploy_2
vsc_sa_upgrade_backup_and_prep
vsc_sa_upgrade_deploy
vsc_sa_upgrade_postdeploy
vsd_ha_upgrade_database_backup_and_decouple
vsd_ha_upgrade_deploy_2_and_3
vsd_ha_upgrade_predeploy_2_and_3
vsd_ha_upgrade_shutdown_2_and_3
vsd_upgrade_complete
vsp_upgrade_postdeploy
vstat_upgrade
vstat_upgrade_prep
vstat_upgrade_wrapup
```

## Skip Actions
A Skip Action is invoked when you want a particular workflow to be skipped. For example, defining `vsd_predeploy` in the skip actions list for a component will cause MetroAE to skip this workflow even when running a workflow that encapsulates it, e.g. `install_vsds`. In such a case, running `install_everything` or `install_vsds` will skip the `vsd_predeploy` workflow.

Note: In the current release, Skip Actions are supported for the following workflows:
```
Insert workflow list here...
```
