# Docker container for Nuage Metro
## Overview
Docker is a tool for capturing an entire deployment environment as a disk image, 
to be easily downloaded and obtained from (public) repositories. These files can
be used to create such an image for the Metro Ansible scripts and their dependencies.

## Usage
To use the public Docker container, simply install Docker and run 'docker run nuage/metro'.
The output will explain what parameters are available; by bind-mounting the current
working directory, the container copies the Metro scripts to the host such that they can
be modified as needed. 

## Build
To build the Metro container image, simply run 'make'

## TODO
The container does not yet have the dependencies needed for vCenter deployments. It also
does not come with 'upgrade' out of the box ( though upgrade scripts can be run 
manually )
