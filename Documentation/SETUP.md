# Setting Up the Environment
You can set up the MetroAE host environment either [with a Docker container](#method-one-set-up-host-environment-using-docker-container) or [with a GitHub clone](#method-two-set-up-host-environment-using-github-clone).

## Environment

### Method One: Set up Host Environment Using Docker Container
Using a Docker container results in a similar setup as a GitHub clone, plus it delivers the following features:
* All prerequisites are satisfied by the container. Your only requirement is to run Docker engine.
* Your data is located in the file system of the host where Docker is running. You don't need to get inside the container.
* You have the option of running an API/UI server allowing you to access MetroAE functionality via REST API and a front-end GUI.
* A future release will include Day 0 Configuration capabilities.
#### System (and Other) Requirements
* Operating System: Enterprise Linux 7 (EL7) CentOS 7.4 or greater or RHEL 7.4 or greater
* Locally available image files for VCS or VNS deployments
* Docker Engine 1.13.1 or greater installed and running
* Container operations may need to be performed with elevated privileges (*root*, *sudo*)
#### Steps
##### 1. Pull the latest Docker container using the following command:
```
metroae container pull
```
##### 2. Setup the Docker container using the following command:
```
metroae container setup [path to data directory]
```
You can optionally specify the data directory path. If you don't specify the data directory on the command line, you will be prompted to enter one during setup. This path is required for container operation. The data directory is the place where docs, examples, Nuage images, and your deployment files will be kept and edited. Note that setup will create a subdirectory beneath the data directory you specify, `metroae_data`. For example, if you specify `/tmp` for your data directory path during setup, setup will create `/tmp/metroae_data` for you. Setup will copy docs, logs, and deployment files to `/tmp/metroae_data`. Inside the container itself, setup will mount `/tmp/metroae_data` as `/metroae_data/`. Therefore, when you specify path names for metroae when using the container, you should always specify the container-relative path. For example, if you copy your tar.gz files to `/tmp/metroae_data/6.0.1` on the host, this will appear as `/metroae_data/6.0.1` inside the container. When you use the unzip-files action on the container, then, you would specify a source path as `/metroae_data/6.0.1`. When you complete the nuage_unzipped_files_dir variable in common.yml, you would also specify `/metroae_data/6.0.1`. Note that you can run setup multiple times and setup will not destroy or modify the data you have on disk. If you specify the same data and imafges directories that you had specified on earlier runs, metroae will pick up the existing data. Thus you can update the container as often as you like and your deployments will be preserved.
##### 3. Start the container using the following command:
```
metroae container start
```
Note that this step is optional. Running *any* metroae command after startup will start the container for you if it is not already running.
##### 4. Copy ssh keys using the following command:
```
metroae container ssh copyid [target_server_username]@[target_server]
```
This command copies the container's public key into the ssh authorized_keys file on the specified target server. This key is required for passwordless ssh access from the container to the target servers. The command must be run once for every target server.

##### 5. **For ESXi / vCenter Only**, install ovftool and copy to metroae_data directory

When running the MetroAE Docker container, the container will need to have access to the ovftool command installed on the Docker host. The following steps are suggested:

###### 5.1. Install ovftool

Download and install the [ovftool](https://www.vmware.com/support/developer/ovf/) from VMware.

###### 5.2. Copy ovftool installation to metroae_data directory

The ovftool command and supporting files are usually installed in the /usr/lib/vmware-ovftool on the host. In order to the metroae container to be able to access these files, you must copy the entire folder to the metroae_data directory on the host. For example, if you have configured the container to use /home/user/metroae_data on your host, you would copy /usr/lib/vmware-ovftool to /home/user/metroae_data/vmware-ovftool. Note: Docker does not support following symlinks. You must copy the files as instructed.

###### 5.3. Configure the ovftool path in your deployment

The path to the ovftool is configured in your deployment in the common.yml file. Uncomment and set the variable 'vcenter_ovftool' to the container-relative path to where you copied the /usr/lib/vmware-ovftool folder. This is required because metroae will attempt to execute ovftool from within the container. From inside the container, metroae can only access paths that have been mounted from the host. In this case, this is the metroae_data directory which is mounted inside the container as '/data'. For our example, in common.yml you would set 'vcenter_ovftool: /data/vmware-ovftool/ovftool'.

##### 6. Optional: Start the UI using this command:
```
metroae gui start
```
This command will ensure that the MetroAE GUI server is running. When running, you an point your browser at `http://host:5001` to access the GUI. *THE GUI IS IN BETA!* You are free to use it, but you can expect to run into issues because it is not GA quality or supported.
##### 7. You can check the status of the container or GUI at any time using the following commands:
```
metroae container status
metroae gui status
```

That's it! Command metadata, command logs, and container setup information are stored in the newly created `/opt/metroae` directory. The `metroae` command becomes available in the `/usr/local/bin` directory. See [DOCKER.md](DOCKER.md) for specfic details of each command and container management command options. Now you're ready to [customize](CUSTOMIZE.md) for your topology.

### Method Two: Set up Host Environment Using GitHub Clone
If you prefer not to use a Docker container you can set up your environment with a GitHub clone instead.
#### System (and Other) Requirements
* Operating System: Enterprise Linux 7 (EL7) CentOS 7.4 or greater or RHEL 7.4 or greater
* Locally available image files for VCS or VNS deployments

#### Steps
##### 1. Clone Repository
If Git is not already installed on the host, install it with the following command.
```
yum install -y git
```
Clone the repo with the following command.
```
git clone https://github.com/nuagenetworks/nuage-metro.git
```
Once the nuage-metro repo is cloned, you can skip the rest of this procedure by running the MetroAE wizard, run_wizard.py. You can use the wizard to automatically handle the rest of the steps described in this document plus the steps described in [customize](CUSTOMIZE.md).
```
python run_wizard.py
```
If you don't run the wizard, please continue with the rest of the steps in this document.
##### 2. Install Packages
MetroAE code includes a setup script which installs required packages and modules. If any of the packages or modules are already present, the script does not upgrade or overwrite them. You can run the script multiple times without affecting the system. To install the required packages and modules, run the following command.
```
sudo ./setup.sh
```
The script writes a detailed log into *setup.log* for your reference. A *Setup complete!* messages appears when the packages have been successfully installed.

##### 3. **For ESXi / vCenter Only**, install additional packages

 Package  | Command
 -------- | -------
 pyvmomi  | `pip install pyvmomi`
 jmespath | `pip install jmespath`

 If you are installing VSP components in a VMware environment (ESXi/vCenter) download and install the [ovftool](https://www.vmware.com/support/developer/ovf/) from VMware. MetroAE uses ovftool for OVA operations.

##### 4. **For OpenStack Only**, install additional packages

 Module       | Command
 ------------ | -------
 shade python | `pip install shade`
 nova client  | `pip install openstackclient`

##### 5. Copy ssh keys
Communication between the MetroAE Host and the target servers (hypervisors) occurs via SSH. For every target server, run the following command to copy the current user's ssh key to the authorized_keys file on the target server:
```
ssh-copy-id [target_server_username]@[target_server]
```

##### 6. Configure NTP sync
For proper operation Nuage components require clock synchronization with NTP. Best practice is to synchronize time on the target servers that Nuage VMs are deployed on, preferrably to the same NTP server as used by the components themselves.

## Unzip Nuage Networks tar.gz files
Ensure that the required unzipped Nuage software files (QCOW2, OVA, and Linux Package files) are available for the components to be installed. Use one of the two methods below.
### Method One: Automatically
Run the command below, replacing [zipped_directory] and [nuage_unzipped_files_dir] with the actual paths:
```
metroae tools unzip images [zipped_directory] [nuage_unzipped_files_dir]
```
Note: After completing setup you will [customize](CUSTOMIZE.md) for your deployment, and you'll need to add this unzipped files directory path to `common.yml`.

### Method Two: Manually
Alternatively, you can create the directories under the [nuage_unzipped_files_dir] directory and manually copy the appropriate files to those locations as shown in the example below.

  ```
  <nuage_unzipped_files_dir>/vsd/qcow2/
  <nuage_unzipped_files_dir>/vsd/ova/ (for VMware)
  <nuage_unzipped_files_dir>/vsc/
  <nuage_unzipped_files_dir>/vrs/el7/
  <nuage_unzipped_files_dir>/vrs/ul16_04/
  <nuage_unzipped_files_dir>/vrs/vmware/
  <nuage_unzipped_files_dir>/vrs/hyperv/
  <nuage_unzipped_files_dir>/vstat/
  <nuage_unzipped_files_dir>/vns/nsg/
  <nuage_unzipped_files_dir>/vns/util/
  ```
Note: After completing setup you will customize for your deployment, and you'll need to add this unzipped files directory path to `common.yml`.

## Next Step
After you've set up your environment you're ready to [customize](CUSTOMIZE.md) for your topology.

## You May Also Be Interested in
[Encrypting Sensitive Data in MetroAE](VAULT_ENCRYPT.md)
[Deploying Components in AWS](AWS.md)

## Questions, Feedback, and Contributing
Get support via the [forums](https://devops.nuagenetworks.net/forum/) on the [MetroAE site](https://devops.nuagenetworks.net/).

Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project").

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
