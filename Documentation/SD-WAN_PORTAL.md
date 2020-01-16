# SD-WAN Portal deployment using Metro&#198;
Metro&#198; now supports the deployment of SD-WAN Portal for Nuage VNS. For more information about SD-WAN Portal and the deployment requirements, please consult the [product documentation](https://nokia.sharepoint.com/sites/vnsportal)

SD-WAN Portal deployment requires a RHEL7/CentOS 7 [image](https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-1901.qcow2) as well as docker images with the product [software](http://nuage-ps-delivery.lab.llama2.cloud/delivery/nuage-portal/)

Supported deployment:

* KVM hypervisor(s)
* SD-WAN Portal versions 6.0.1+


Currently the following workflows are supported:

* install_sdwan_portal - Deploy Portal VM(s) on KVM hypervisor and install the application
* sdwan_portal_predeploy - Prepares the HV and deploys Portal VMs
* sdwan_portal_deploy - Installs Docker-CE, SD-WAN Portal on the already prepared VMs
* sdwan_portal_postdeploy - To be updated. Includes a restart and license update task
* sdwan_portal_license_update - Copies the license file to the Portal VM(s) and restarts the Portal(s)
* sdwan_portal_destroy - Destroys Portal VMs and cleans up the files from hypervisor(s)

Example deployment files are available under examples/kvm_portal_install

### 1. Configure `common.yml`
  In your MetroAE deployment folder, create or edit the `common.yml` configuring the necessary attributes.
  Portal specific attributes include:
  * portal_fqdn_global - SD-WAN Portal Global FQDN. Typically a public (external) FQDN resolvable to the Portal endpoint on a Proxy/LB in both standalone and HA deployments. For standalone - FQDN of a single Portal node
  * vsd_port_global - Used with vsd_global_fqdn by the SD-WAN Portal to connect to the VSD cluster. Defaults to 8443. 
  * vstat_fqdn_global - ElasticSearch cluster FQDN. SD-WAN Portal accesses the ES cluster to retrieve statistics for visualization and reports. For standalone ES - FQDN of a single ES node.
  * yum_proxy - Portal is using the same Proxy for Docker to pull the images from Docker hub. Optional if using the pre-downloaded SW package.
  * portal_license_file - SD-WAN Portal license. Request through ASLM.
  * portal_ram - Amount of Portal RAM to allocate, in GB.

### 2. Configure `credentials.yml`  
  Create or edit the `credentials.yml` configuring the necessary attributes.
  Portal specific attributes include: 
  * portal_username - VSD username reserved for the Portal. (Optional)
  * portal_password - VSD password for the user configured in `portal_username`. (Optional)
  * portal_custom_username - CLI user to log in to the Portal VM
  * portal_custom_password - CLI user password to log in to the Portal VM
  * smtp_auth_username - SMTP server username used by Portal Messaging app to send Portal user management emails
  * smtp_auth_password - Password for SMTP server user.
  
### 3. Configure `portals.yml`
  Create or edit the `portals.yml` configuring the necessary attributes. For standalone deployment, only one Portal section is needed. 3 Portal sections are required for HA deployment (see example deployment file). Standard Metro&#198; attributes are used with some unique to SD-WAN Portal ones listed below:
  * password_reset_email; new_account_email; forgot_password_email - Sender address to be used in Portal user management emails
  * smtp_fqdn - SMTP server FQDN
  * smtp_port - SMTP server port
  * smtp_secure - Specifies whether user/password authentication is required. If True, configure username and password in credentials.yml
  * sdwan_portal_secure - Enables SSL for the SD-WAN Portal
  * portal_version - if using Docker hub to pull the images, specifies the tag of the Docker image
