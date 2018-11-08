# Deploying Components with MetroÆ Docker container

## Prerequisites / Requirements
* Docker must be installed on the system and running 
* Locally available image files for VCS or VNS deployments
 
## Supported Commands

The following commands are supported on the script

* help 

    Displays the help text for the script 

* pull 

    Pulls the latest container from docker registry
	
    example: 
```
        Retrieving MetroAE container... 
        current: Pulling from demometroae 
        b8e0383d5f94: Pull complete 
        4e09e5a4c123: Pull complete 
        5b022a14320b: Pull complete
        ca897f238a29: Pull complete
        eb0978a17d1a: Pull complete
        44a0402dc5d6: Pull complete
        a7da77b50603: Pull complete
        4545e56dc967: Pull complete
        0632cdc75860: Pull complete
        9dbaca0fcd58: Pull complete
        2e4e2973e9bd: Pull complete
        838ce4ce5585: Pull complete
        fe0cc62c15da: Pull complete
        b19de726fce8: Pull complete
        ec26d6430474: Pull complete
        dd492fe518bb: Pull complete
        e6e0fd8683b6: Pull complete
        Digest: sha256:bb489bd4595c473b2326965bcc85846b4eabf18d4a8219ba988d57b6ab0119df
```
* setup 

    Setup will help in setting up the container to access the host volumes for user data and help in configuring a UI port
	
    example: 
```
        Specify the full path to store data on the host system, metroae_data directory will be created after the provided path. If the path ends with metroae_data we are going to use the path as is: /tmp
        Specify the full path of image files on the host system, metroae_images directory will be created after the provided path. If the path ends with metroae_images we are going to use the path as is: /tmp
        Specify the REST API/UI access port for the container: 5001
```
* start 

    Starts the container and using the previous settings from setup

* stop 

    Stops the running container

* status 

    Displays the container status along with container settings

* destroy 

    Stops and removes metroae container along with the container image

* upgrade-engine 

    Upgrades the container to the latest available release image. Setup need not be run when upgrading to the latest container version

* stop-ui 

    Stops the UI server running in the container

* start-ui 

    Start the UI server in the container along with asking for UI settings like certificate that needs to be used to access the UI. The UI can be accessed on port 5001 when running the container in an Linux environment.

* status-ui 

    Displays the UI status

* unzip-files 

    Unzip Nuage Networks image file into the images mount on the host system. Requires the zip files to be placed in the data or images mount point.

* convert-build-vars-to-deployments 

    Converts the existing build vars from MetroÆ 2 version into deployments. The build vars file needs to be place in the data or images mount point for container access

* generate-example-from-schema 

    Generates an example for the specified schema and puts them in the examples directory in the data mount point

* encrypt-credentials 

    Sets the encryption credentials for encrypting the user data

* enable-ui-encryption 

    Sets up TLS certificate for the UI access

* disable-ui-encryption  

    Disables TLS on the UI

* copy-ssh-id 

    Copies docker public key into the authorized directory on the target server for password less ssh

## Running MetroÆ in the docker container 

To access MetroÆ from the command line you just need to run ./metroae playbook

# Troubleshooting

* SSH connection problems 

    Run copy-ssh-id action to copy the public key of the container over to the target server

* Location of the docker settings 

    Check the user's home directory who ran the setup action for ./metroae file which contains all the settings for the container

* Unable to access user files 

    Data mount point specified during setup is mounted as /data in the container. When defining paths in the container make sure the mount point path is replaced with /data

    example: 

        If my mount that I specified during setup is /opt, container mounts /opt as /data internally so anything that is inside the /opt directory is accessible from the container as /data

    Image mount specified during setup is mounted as /images in the container. When defining paths in the deployments make sure the mount point path is replaced with /images
    
    example: 

```
        If my mount that I specified during setup is /opt, container mounts /opt as /images internally so if I have my Nuage Networks images file the container can access them from /images 
```
* Check the metroae.log to see if there are an error logged 

# Manually Use the container without the script

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
