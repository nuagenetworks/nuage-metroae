# Hooks
Hooks are predefined locations in the code where an user can execute custom commands. The command can contain predefined Ansible variable in Jinja2 format.

## Hooks File
This file contains information about the location and the command that needs to be executed. The path to this file needs to be accessible by Ansible and it needs to be defined in the deployments file for the component under the hooks section.
The file format should be yaml.
<br>
Example of a file that executes custom script before vstat-predeploy
<br>
`location: vstat_predeploy`
<br>
`command: "command to execute at this location. Can contain Jinja2 Ansible variables (e.g echo {{ hostsvars[inventory_hostname].name }} {{ groups['vstats'][0].hostname }} "`

## Predefined Hooks locations

`VSP Hooks Locations`
<br>
<br>
vsd_predeploy<br>
vsd_deploy<br>
vsd_postdeploy<br>
vsc_predeploy<br>
vsc_deploy<br>
vsc_postdeploy<br>
vstat_predeploy<br>
vstat_deploy<br>
vstat_postdeploy<br>
vnsutil_predeploy<br>
vrs_predeploy<br>
vrs_deploy<br>
vrs_postdeploy<br>
<br>
<br>

`VNS Hooks Locations`
<br>
<br>
vsd_predeploy<br>
vsd_deploy<br>
vsd_postdeploy<br>
vsc_predeploy<br>
vsc_deploy<br>
vsc_postdeploy<br>
vstat_predeploy<br>
vstat_deploy<br>
vstat_postdeploy<br>
vnsutil_predeploy<br>
vrs_predeploy<br>
vrs_deploy<br>
vrs_postdeploy<br>
vcin_destroy<br>
vrs_destroy<br>
vsd_vns_postdeploy<br>
vnsutil_predeploy<br>
vnsutil_deploy<br>
vnsutil_postdeploy<br>
nsgv_predeploy<br>
nsgv_postdeploy<br>
vcin_deploy<br>
vcin_destroy<br>
vcin_predeploy<br>
vnsutil_deploy<br>
<br>
<br>

`Upgrade Hooks Locations`
<br>
<br>

nsgv_postdeploy<br>
nsgv_predeploy<br>
upgrade_vsds<br>
upgrade_vsds_inplace<br>
upgrade_vsds_inplace_dbbackup<br>
vcin_deploy<br>
vcin_destroy<br>
vcin_predeploy<br>
vnsutil_deploy<br>
vnsutil_postdeploy<br>
vnsutil_predeploy<br>
vrs_deploy<br>
vrs_destroy<br>
vrs_postdeploy<br>
vrs_predeploy<br>
vsc_backup<br>
vsc_deploy<br>
vsc_destroy<br>
vsc_ha_upgrade_backup_and_prep_1<br>
vsc_ha_upgrade_backup_and_prep_2<br>
vsc_ha_upgrade_deploy_1<br>
vsc_ha_upgrade_deploy_2<br>
vsc_ha_upgrade_postdeploy_1<br>
vsc_ha_upgrade_postdeploy_2<br>
vsc_postdeploy<br>
vsc_predeploy<br>
vsc_sa_upgrade_backup_and_prep<br>
vsc_sa_upgrade_deploy<br>
vsc_sa_upgrade_postdeploy<br>
vsc_vns_postdeploy<br>
vsd_deploy<br>
vsd_destroy<br>
vsd_ha_upgrade_database_backup_and_decouple<br>
vsd_ha_upgrade_deploy_2_and_3<br>
vsd_ha_upgrade_predeploy_2_and_3<br>
vsd_ha_upgrade_shutdown_2_and_3<br>
vsd_postdeploy<br>
vsd_predeploy<br>
vsd_upgrade_complete<br>
vsp_upgrade_postdeploy<br>
vstat_deploy<br>
vstat_destroy<br>
vstat_postdeploy<br>
vstat_predeploy<br>
vstat_upgrade<br>
vstat_upgrade_prep<br>
vstat_upgrade_wrapup<br>


# Skip Actions
Skip Actions define if a particular playbook should execute or not. For example defining vsd_predeploy in skip actions list will cause Ansbile to skip this playbook even when running a playbook that encapsulates vsd_predeploy in it. In this case running install_everything playbook will skip vsd_predeploy playbook.
Currently 'Skip Actions' is only limited to component pre-deploy playbooks.
