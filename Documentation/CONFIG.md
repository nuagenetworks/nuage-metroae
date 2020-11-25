# MetroAE Config

MetroAE Config is a template-driven VSD configuration tool. It utilizes the VSD API along with a set of common Feature Templates to create configuration in the VSD. The user will create a yaml or json data file with the necessary configuration parameters for the particular feature and execute simple CLI commands to push the configuration into VSD.

MetroAE Config is available via the MetroAE container. Once pulled and setup, additional documentation will be available.

## Configuration Engine Installation

MetroAE Configuration engine is provided as one of the capabilities of the MetroAE Docker container. The installation of the container is handled via the metroae script. Along with the configuration container we also require some additional data.

On a host where the configuration engine will be installed the following artifacts will be installed:

* Docker container for configuration
* Collection of configuration Templates
* VSD API Specification

### System Requirements

* Operating System: RHEL/Centos 7.4+
* Docker: Docker Engine 1.13.1+
* Network Access: Internal and Public
* Storage: At least 800MB

#### Operating system

The primary requirement for the configuration container is Docker Engine, however the installation, container operation and functionality is only tested on RHEL/Centos 7.4. Many other operating systems will support Docker Engine, however support for these is not currently provided and would be considered experimental only. A manual set of installation steps is provided for these cases.  

#### Docker Engine

The configuration engine is packaged into the MetroAE Docker container. This ensures that all package and library requirements are self-contained with no other host dependencies. To support this, Docker Engine must be installed on the host. The configuration container requirements, however, are quite minimal. Primarily, the Docker container mounts a local path on the host as a volume while ensuring that any templates and user data are maintained only on the host. The user never needs to interact directly with the container.  

#### Network Access

Currently the configuration container is hosted in an internal Docker registry and the public network as a secondary option, while the Templates and API Spec are hosted only publicly. The install script manages the location of these resources. The user does not need any further information. However, without public network access the installation will fail to complete.

#### Storage

The configuration container along with the templates requires 800MB of local disk space. Note that the container itself is ~750MB, thus it is recommended that during install a good network connection is available.

#### User Privileges

The user must have elevated privileges on the host system.

### Installation

Execute the following operations on the Docker host:

1. Install Docker Engine

    Various instructions for installing and enabling Docker are available on the Internet. One reliable source of information for Docker CE is hosted here:

    [https://docs.docker.com/engine/install/centos/](https://docs.docker.com/engine/install/centos/)

2. Add the user to the wheel and docker groups on the Docker host.

3. Move or Copy the "metroae" script from the nuage-metroae repo to /usr/bin and set permissions correctly to make the script executable.

4. Switch to the user that will operate "metroae config".

5. Setup the container using the metroae script.

    We are going to pull the image and setup the metro container in one command below. During the install we will be prompted for a location for the container data directory. This is the location where our user data, templates and VSD API specs will be installed and created and a volume mount for the container will be created. However this can occur orthogonally via "pull" and "setup" running at separate times which can be useful depending on available network bandwidth.

    `[caso@metroae-host ~]$ metroae container setup`

    The MetroAE container needs access to your user data. It gets access by internally mounting a directory from the host. We refer to this as the 'data directory'. The data directory is where you will have deployments, templates, documentation, and other useful files. You will be prompted to provide the path to a local directory on the host that will be mounted inside the container. You will be prompted during setup for this path.

    The MetroAE container can be setup in one of the following configurations:

    * Config only
    * Deploy only
    * Both config and deploy

    During setup, you will be prompted to choose one of these options.

6. Follow additional insturctions found in the documentaion that is copied to the Docker host during setup.

Complete documentation will be made available in the data directory you specify during setup. The complete documentation includes how to configure your environment, usage information for the tool, and more.
