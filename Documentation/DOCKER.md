# Deploying Components with the MetroÆ Docker Container

## The metroae Command
The metroae command is at the heart of interacting with the MetroÆ container. It is used both to manage the container and to execute MetroÆ inside the container. You can access all of the command options via `metroae <action | workflow> [deployment] [options]`.

### metroae Container Management Command Options

The following command options are supported by the metroae command:

**help** -displays the help text for the command

**pull** - pulls the MetroÆ container from the registry. By default, the latest container is pulled. You can also specify a valid container tag to pull another version, e.g. `metroae pull 1.0.0`.

**setup** - setup completes the steps necessary to get the MetroÆ container up and running. It prompts you for the full paths to data and image directories that the container uses on your local disk. On Mac OS, you will also be prompted for the port that the API/UI will be listening on. By default, the API/UI listens on port 5001. You can access the API/GUI via URL, `https://host_name_or_ip:5001`, where `host_name_or_ip` is the host name or ip address of the machine on which the container is running. This host name can often be just, `https://localhost:5001`. Note: Running setup multiple times replaces the existing container, but it does not remove the data on your local disk.

**start** - starts the container using the settings from setup

**stop** - stops the running container

**status** - displays the container status along with container settings

**destroy** - stops and removes the metroae container along with the container image. Use this command when you want to replace an existing container with a new one, no need to run setup again afterwards.

**upgrade-engine** - upgrades the container to the latest available release image. You don't need to run setup again after an upgrade.

**stop-ui** - stops the UI server running in the container

**start-ui** - starts the API/UI server in the container. It prompts you for UI settings, such as whether you want to configure a certificate and whether a password will be used to encrypt passwords. The default port used by the API/UI server is 5001, as in `https://localhost:5001`.

**status-ui** - displays the status of the API/UI server in the container

**unzip-files** - unzips Nuage Networks tar.gz files into the images directory specified during the setup operation. Use of this command requires that the tar.gz files be placed in either the data or images directory that you specified during setup.
See the current values of the data and images directories by executing the status command.

**convert-build-vars-to-deployments** - converts a legacy MetroÆ 2 build_vars.yml file into a MetroÆ 3 deployment. Use of this command requires that the build_vars.yml file be present in either the data or images directory that you specified during setup. You can get the current values of the data and images directories by executing the status command.

**generate-example-from-schema** - generates an example for the specified schema and puts it in the examples directory under the data directory that you specified during setup. You can get the current values of the data and images directories by executing the status command.

**encrypt-credentials** - sets the encryption credentials for encrypting secure user data, e.g. passwords

**enable-ui-encryption** - sets up a TLS certificate for the UI access

**disable-ui-encryption** - disables TLS on the UI

**copy-ssh-id** - copies the container's public key into the ssh authorized_keys file on the specified server. This key is required for passwordless ssh access to all target servers. Usage: `metroae copy-ssh-id user@host_or_ip`

**--list** - lists the workflows that are supported by MetroÆ

**--ansible-help** - shows the help options for the underlying Ansible engine

### metroae Workflow Command Options

The MetroÆ container is designed so that you run MetroÆ workflows, e.g. install, from the command line using the metroae command. The format of the command line is:

    `metroae <workflow> [deployment] [options]`

## Troubleshooting

### SSH connection problems
If MetroÆ is unable to authenticate with your target server, chances are that passwordless ssh has not been configured properly. The public key of the container must be copied to the authorized_keys file on the target server. Use the `copy-ssh-id` command option, e.g. `metroae copy-ssh-id user@host_name_or_ip`.

### Where are my data and image directories or what are my API/UI settings?
Determine the current setup by either searching for a file named .metroae in the user's home directory or by executing the status command option, e.g. `metroae status`.

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
### Execute MetroÆ Commands

    docker exec 'running container id' /source/nuage-metro/metroae playbook deployment

### Stop the container

    docker stop 'running container id'

### Remove the container

    docker rm 'container id'

### Remove MetroÆ image

    docker rmi 'image id'

## Questions, Feedback, and Contributing
Ask questions and get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroÆ site](https://devops.nuagenetworks.net/).  
You may also contact us directly.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.
