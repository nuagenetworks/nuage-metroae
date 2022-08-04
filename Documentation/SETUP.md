# Setting Up the Environment

You can set up the MetroAE host environment [with a GitHub clone](#set-up-host-environment-using-github-clone).
Note that docker is required on the host in order to run MetroAE. All file paths in configuration files must be relative to the git clone folder.

## Environment

### Set up Host Environment Using GitHub Clone

#### System (and Other) Requirements

* Operating System: Enterprise Linux 7 (EL7) CentOS 7.4 or greater or RHEL 7.4 or greater
* Locally available image files for VCS or VNS deployments within the git clone folder
* Docker engine

NOTE: SElinux must be disabled or set to permissive for MetroAE to work.

#### Steps

##### 1. Clone Repository

If Git is not already installed on the host, install it with the following command.
```
yum install -y git
```

Clone the repo with the following command. NOTE: Please clone the repo in a location that can be
read by **libvirt/qemu**.
```
git clone https://github.com/nuagenetworks/nuage-metroae.git
```

Once the nuage-metroae repo is cloned, you can skip the rest of this procedure by running the MetroAE wizard. You can use the wizard to automatically handle the rest of the steps described in this document plus the steps described in [customize](CUSTOMIZE.md).
```
metroae-container wizard
```

If you don't run the wizard, please continue with the rest of the steps in this document.

##### 2. Copy ssh keys

Communication between the MetroAE Host and the target servers (hypervisors) occurs via SSH. For every target server, run the following command to copy the current user's ssh key to the authorized_keys file on the target server:
```
ssh-copy-id [target_server_username]@[target_server]
```

##### 3. Configure NTP sync

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

Alternatively, you can create the directories under the [nuage_unzipped_files_dir] directory and manually copy or unzip the appropriate files to that location. MetroAE uses `find` to locate the files under [nuage_unzipped_files_dir], so the precise location under that directory is not significant. For reference, the automatic unzip in Method One puts files in the following locations:

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
<nuage_unzipped_files_dir>/vns/nuh/
<nuage_unzipped_files_dir>/vns/util/
```

Note: After completing setup you will customize for your deployment, and you'll need to add this unzipped files directory path to `common.yml`.

## Next Steps

After you've set up your environment you're ready to [customize](CUSTOMIZE.md) for your topology.

## You May Also Be Interested in

[Encrypting Sensitive Data in MetroAE](VAULT_ENCRYPT.md)
[Deploying Components in AWS](AWS.md)

## Questions, Feedback, and Contributing

Get support via the [forums](https://devops.nuagenetworks.net/forum/) on the [MetroAE site](https://devops.nuagenetworks.net/).

Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:devops@nuagenetworks.net "send email to nuage-metro project").

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metroae/issues "nuage-metroae issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
