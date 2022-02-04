# SD-WAN Portal deployment using MetroAE
MetroAE now supports the deployment of SD-WAN Portal for Nuage VNS. For more information about SD-WAN Portal and the deployment requirements, please consult the [product documentation](https://nokia.sharepoint.com/sites/vnsportal)

SD-WAN Portal deployment requires a RHEL7/CentOS 7 [image](https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-1901.qcow2) as well as docker images with the product [software](http://nuage-ps-delivery.lab.llama2.cloud/delivery/nuage-portal/)

Supported deployment:

* KVM hypervisor(s)
* SD-WAN Portal versions 6.0.1+

Currently the following workflows are supported:

* metroae-container install portal - Deploy Portal VM(s) on KVM hypervisor and install the application
* metroae-container install portal predeploy - Prepares the HV and deploys Portal VMs
* metroae-container install portal deploy - Installs Docker-CE, SD-WAN Portal on the already prepared VMs
* metroae-container install portal postdeploy - To be updated. Includes a restart and license update task
* metroae-container install portal license - Copies the license file to the Portal VM(s) and restarts the Portal(s)
* metroae-container destroy portal - Destroys Portal VMs and cleans up the files from hypervisor(s)
* metroae-container upgrade portal - Upgrade Portal VM(s) on KVM hypervisor
* metroae-container upgrade portal preupgrade health - Performs prerequisite and health checks of a Portal VM or cluster before initiating an upgrade
* metroae-container upgrade portal shutdown - Performs database backup if necessary, Portal VM snapshot and stops all services
* metroae-container upgrade portal deploy - Performs an install of the new SD-WAN Portal version
* metroae-container upgrade portal postdeploy - Performs post-upgrade checks to verify Portal VM health, cluster status, and verify successful upgrade
* metroae-container rollback portal - In the event of an unsuccessful upgrade, Portal(s) can be rolled back to the previously installed software version.

Example deployment files are available under examples/kvm_portal_install

## Portal Install

The files required for an install of SD-WAN Portal are listed below.

### 1. Configure `common.yml` for install

  In your MetroAE deployment folder, create or edit the `common.yml` configuring the necessary attributes.
  Portal specific attributes include:

* portal_fqdn_global - SD-WAN Portal Global FQDN. Typically a public (external) FQDN resolvable to the Portal endpoint on a Proxy/LB in both standalone and HA deployments. For standalone - FQDN of a single Portal node
* vsd_port_global - Used with vsd_global_fqdn by the SD-WAN Portal to connect to the VSD cluster. Defaults to 8443.
* vstat_fqdn_global - ElasticSearch cluster FQDN. SD-WAN Portal accesses the ES cluster to retrieve statistics for visualization and reports. For standalone ES - FQDN of a single ES node.
* yum_proxy - Portal is using the same Proxy for Docker to pull the images from Docker hub. Optional if using the pre-downloaded SW package.
* portal_license_file - SD-WAN Portal license. Request through ASLM.
* portal_ram - Amount of Portal RAM to allocate, in GB.

### 2. Configure `credentials.yml` for install

  Create or edit the `credentials.yml` configuring the necessary attributes.
  Portal specific attributes include:

* portal_username - VSD username reserved for the Portal. (Optional)
* portal_password - VSD password for the user configured in `portal_username`. (Optional)
* portal_custom_username - CLI user to log in to the Portal VM
* portal_custom_password - CLI user password to log in to the Portal VM
* smtp_auth_username - SMTP server username used by Portal Messaging app to send Portal user management emails
* smtp_auth_password - Password for SMTP server user.

### 3. Configure `portals.yml` for install

  Create or edit the `portals.yml` configuring the necessary attributes. For standalone deployment, only one Portal section is needed. 3 Portal sections are required for HA deployment (see example deployment file). Standard MetroAE attributes are used with some unique to SD-WAN Portal ones listed below:

* password_reset_email; new_account_email; forgot_password_email - Sender address to be used in Portal user management emails
* smtp_fqdn - SMTP server FQDN
* smtp_port - SMTP server port
* smtp_secure - Specifies whether user/password authentication is required. If True, configure username and password in credentials.yml
* sdwan_portal_secure - Enables SSL for the SD-WAN Portal
* portal_version - if using Docker hub to pull the images, specifies the tag of the Docker image

## To install portal with Geo-Redundant Control Node (GRCN)

### Configure `portal_grcn.yml` for install

  In your MetroAE deployment folder, create or edit the `portal_grcn.yml` configuring the necessary attributes.
  Standard MetroAE attributes are used with some unique to SD-WAN Portal GRCN ones listed below:

* current_dc - Current Datacenter name (dc1 or dc2)
* other_dc_portal1_ip: Other Datacenter's Portal 1 management ip address
* other_dc_portal2_ip: Other Datacenter's Portal 2 management ip address
* other_dc_portal3_ip: Other Datacenter's Portal 3 management ip address
* other_dc_grcn_ip: Other Datacenter's GRCN management ip address

## Portal Upgrade

For upgrades of the SD-WAN Portal, example deployment files can be found under examples/kvm_portal_upgrade. The files required for upgrading SD-WAN Portal(s) are listed below:

### 1. Configure `common.yml` for upgrade

  This file can be updated for the Portal upgrade. The only change needed for the Portal upgrade is the following:

* nuage_unzipped_files_dir - Update if necessary to point to the location of the SD-WAN Portal upgrade files

### 2. Configure `upgrade.yml` for upgrade

  The `upgrade.yml` file will need to be included in order to perform the upgrade. The necessary parameter is:

* upgrade_portal - A boolean value to determine whether or not to upgrade the portals

### 3. Configure `portals.yml` for upgrade

  This file will can be updated to reflect the the version of the new SD-WAN Portal software to be installed.

* portal_version - This needs to be included to pull the Docker images from Docker Hub, but is not necessary if the upgrade images are already present on the hypervisor

## Portal Rollback

For rollbacks of the SD-WAN Portal or cluster, use the same deployment files as the initial installation and do a re-install.
