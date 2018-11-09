# Deploying Components with the MetroÆ Docker Container

In addition to being able to access MetroÆ via github clone, MetroÆ is now optionally available for distribution via Docker container. The Docker container version of MetroÆ as all the capabilities of the github clone, plus it delivers the following:

* All MetroÆ prerequisites are satisifed by the container. Your only requirement is that you need to run Docker.
* CLI access is provided through the `metroae` command. 
* Your data is located in the file system of the host where you are running Docker. You don't need to get inside the container.
* The Container has the option of running an API/UI server. This allows you to access MetroÆ functionality via REST API and a front-end GUI.

# Prerequisites / Requirements
* Docker must be installed on the system and running 
* Locally available image files for VCS or VNS deployments

# The metroae Command

The heart of operating using the MetroÆ container is the metroae command. It is delivered from the github repo. It is used both to manage the container and to execute MetroÆ inside the container. You can access all of the command options via `./metroae command <options>`.

## metroae Container Management Command Options

The following command options are supported by the metroae command:

* help 

    Displays the help text for the command 

* pull 

    Pulls the latest container from the docker registry
	
* setup 

    Setup will complete the steps necessary to get the MetroÆ container up and running. You will be prompted for the full paths to data and image directories that the container will use on your local disk. On Mac OS, you will also be prompted for the port the API/UI will be listening on. By default, the API/UI will be listening on port 5001. You can access the API/GUI via URL, `https://host_name_or_ip:5001`, where `host_name_or_ip` is the host name or ip address of the machine on which the container is running. This can often be just, `https://localhost:5001`. Note: Running setup multiple times will not remove your data, but it will replace the existing container.
	
* start 

    Starts the container using the settings from setup

* stop 

    Stops the running container

* status 

    Displays the container status along with container settings

* destroy 

    Stops and removes metroae container along with the container image

* upgrade-engine 

    Upgrades the container to the latest available release image. You don't need to run setup again after an upgrade.

* stop-ui 

    Stops the UI server running in the container

* start-ui 

    Starts the API/UI server in the container. You will be prompted for UI settings such as whether you want to configure a certificate and whether a password will be used to encrypt passwords. The default port used by the API/UI server is 5000, as in `https://localhost:5001`.

* status-ui 

    Displays the status of the API/UI server in the container

* unzip-files 

    Unzip Nuage Networks tar.gz files into the images directory specified during the setup operation. Use of this command requires that the tar.gz files be placed in either the data or images directory that you specified during setup. You can get the current values of the data and images directories by executing the status command.

* convert-build-vars-to-deployments 

    Converts a legacy MetroÆ 2 build_vars.yml file into a MetroÆ 3 deployment. Use of this command requires that the build_vars.yml file be present in either the data or images directory that you specified during setup. You can get the current values of the data and images directories by executing the status command.

* generate-example-from-schema 

    Generates an example for the specified schema and puts it in the examples directory under the data directory that you specified during setup. You can get the current values of the data and images directories by executing the status command.

* encrypt-credentials 

    Sets the encryption credentials for encrypting secure user data, e.g. passwords

* enable-ui-encryption 

    Sets up a TLS certificate for the UI access

* disable-ui-encryption  

    Disables TLS on the UI

* copy-ssh-id 

    Copies the container's public key into the ssh authorized_keys file on the specified server. This is required for passwordless ssh access to all target servers. Usage: `metroae copy-ssh-id user@host_or_ip`

* --list

    Lists the workflows that are supported by MetroÆ
    
* --ansible-help

    Shows the help options for the underlying Ansible engine.
    
## metroae Workflow Command Options

The MetroÆ container is designed so that you run MetroÆ workflows, e.g. install, from the command line using the metroae command. The format of the command line is:

    `metroae <workflow> [deployment] [options]`

# Troubleshooting

* SSH connection problems 

    If MetroÆ complains that it is unable to authenticate with your target server, chances are that passwordless ssh has not been configured properly. The public key of the container must be copied to the authorized_keys file on the target server. This can be accomplished using the `copy-ssh-id` command option, e.g. `./metroae copy-ssh-id user@host_name_or_ip`.

* Can't find the location of the data and image directories or the API/UI settings 

    There are two options for determining the current setup. One is to look for a file named .metroae in the user's home directory. Or you can execute the status command option, e.g. `./metroae status`.

* General errors

    In the data directory that you specified at setup, you will find metroae.log and ansible.log.

# Manually use the container without the script

These steps are currently supported for Nokia internal only

* Pulling the container 

    docker pull registry.mv.nuagenetworks.net:5000/metroae:1.0

* Running the container 

    docker run -e USER_NAME='user name for the container' -e GROUP_NAME='group name for the container' -d $networkArgs -v 'path to the data mount point':/data:Z -v 'path to images mount point':/images:Z --name metroae registry.mv.nuagenetworks.net:5000/metroae:1.0

```
        networkArgs is '--network host' for Linux host 
        networkArgs is '-p "UI Port":5001' for Mac host
```

* Executing MetroAE Commands 

    docker exec 'running container id' /source/nuage-metro/metroae playbook deployment

* Stopping the container 

    docker stop 'running container id'

* Removing the container 

    docker rm 'container id'

* Remove MetroAE image 

    docker rmi 'image id'
