# Deploying Components with the MetroAE Docker Container

This file describes many of the details of the commands used for managing MetroAE distributed via container. For information on how to setup Docker and the MetroAE Docker container, see [SETUP.md](SETUP.md).

## The metroae Command
The metroae command is at the heart of interacting with the MetroAE container. It is used both to manage the container and to execute MetroAE inside the container. You can access all of the command options via `metroae <workflow> <component> [action] [deployment] [options]`.

### metroae Container Management Command Options

The following command options are supported by the metroae command:

**help** -displays the help text for the command

**pull** - pulls the MetroAE container from the registry. By default, the latest container is pulled. You can also specify a valid container tag to pull another version, e.g. `metroae container pull 1.0.0`.

**setup** - setup completes the steps necessary to get the MetroAE container up and running. It prompts you for the full paths to a data directory that the container uses on your local disk. The setup action will create the subdirectory `metroae_data` on disk, then mount it as `/metroae_data/` inside the container. When using the MetroAE container, you must provide paths relative to this path as seen from inside the container. For example, if you tell setup to use `/tmp` for the data directory, setup will create `/tmp/metroae_data` on your host. The setup will also mount this directory inside the container as `/metroae_data/`. If you copy your tar.gz files to `/tmp/metroae_data/images/6.0.1/` on the host, the container sees this as `/data/images/6.0.1/`. So, when using unzip or setting `nuage_unzipped_files_dir` in common.yml, you would specify `/metroae_data/images/6.0.1/` as your path.

#### Notes about setup:
The MetroAE container has support for a REST API and a beta version of the MetroAE GUI. The REST API is supported. The GUI should be considered `preview` or `experimental`. We do not recommend using the GUI for production.

By default, the API/GUI listens on port 5001. You can access the API/GUI via URL, `https://host_name_or_ip:5001`, where `host_name_or_ip` is the host name or ip address of the machine on which the container is running. This host name can often be just, `https://localhost:5001`.

Running setup multiple times replaces the existing container, but it does not remove the data on your local disk.

**metroae container start** - starts the container using the settings from setup

**metroae container stop** - stops the running container

**metroae container status** - displays the container status along with container settings

**metroae container destroy** - stops and removes the metroae container along with the container image. Use this command when you want to replace an existing container with a new one, no need to run setup again afterwards.

**metroae container update** - upgrades the container to the latest available release image. You don't need to run setup again after an upgrade.

**metroae gui stop** - stops the UI server running in the container

**metroae gui start** - starts the API/UI server in the container. It prompts you for UI settings, such as whether you want to configure a certificate and whether a password will be used to encrypt passwords. The default port used by the API/UI server is 5001, as in `https://localhost:5001`.

**metroae gui status** - displays the status of the API/UI server in the container

**metroae unzip-files** - unzips Nuage Networks tar.gz files into the images directory specified during the setup operation. Use of this command requires that the tar.gz files be placed in either the data or images directory that you specified during setup.
See the current values of the data and images directories by executing the status command.

**metroae generate-example-from-schema** - generates an example for the specified schema and puts it in the examples directory under the data directory that you specified during setup. You can get the current values of the data and images directories by executing the status command.

**metroae encrypt-credentials** - sets the encryption credentials for encrypting secure user data, e.g. passwords

**metroae gui encryption enable** - sets up a TLS certificate for the UI access

**metroae guiencryption disable** - disables TLS on the UI

**metroae copy-ssh-id** - copies the container's public key into the ssh authorized_keys file on the specified server. This key is required for passwordless ssh access to all target servers. Usage: `metroae copy-ssh-id user@host_or_ip`

**metroae --list** - lists the workflows that are supported by MetroAE

**metroae --ansible-help** - shows the help options for the underlying Ansible engine

### metroae Workflow Command Options

The MetroAE container is designed so that you run MetroAE workflows, e.g. install, from the command line using the metroae command. The format of the command line is:

    `metroae <workflow> <component> [operation] [deployment] [options]`

## Troubleshooting

### SSH connection problems
If MetroAE is unable to authenticate with your target server, chances are that passwordless ssh has not been configured properly. The public key of the container must be copied to the authorized_keys file on the target server. Use the `copy-ssh-id` command option, e.g. `metroae copy-ssh-id user@host_name_or_ip`.

### Where are my data and image directories or what are my API/UI settings?
Determine the current setup by either searching for a file named .metroae in the user's home directory or by executing the status command option, e.g. `metroae container status`.

### General errors
metroae.log and ansible.log are located in the data directory you specified during setup.

## Manually use the container without the script (Nokia internal support only)
### Pull the container

    docker pull registry.mv.nuagenetworks.net:5001/metroae:1.0

### Run the container
docker run -e USER_NAME='user name for the container' -e GROUP_NAME='group name for the container' -d $networkArgs -v 'path to the data mount point':/data:Z -v 'path to images mount point':/images:Z --name metroae registry.mv.nuagenetworks.net:5001/metroae:1.0
#### For Linux host
```
networkArgs is '--network host'
```
#### For Mac host
```
networkArgs is '-p "UI Port":5001'
```
### Execute MetroAE Commands

    docker exec 'running container id' /source/nuage-metro/metroae playbook deployment

### Stop the container

    docker stop 'running container id'

### Remove the container

    docker rm 'container id'

### Remove MetroAE image

    docker rmi 'image id'

## Questions, Feedback, and Contributing
Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project").

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
