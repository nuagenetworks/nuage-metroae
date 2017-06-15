# Docker container image for Nuage Metro

This directory contains an initial Dockerfile to build a container that can host the Nuage Metro environment. It contains all the dependencies and can be posted to the public Docker repository, such that getting and running Metro becomes as easy as:

docker run nuage/metro

## Instructions

When run without parameters, the container will print out usage instructions. It uses bind mounting to make the current directory accessible to the container, such that it can read a configuration file from there and unpack the Nuage sources. When no configuration file is present, a sample file is generated which can be edited to match your environment.

## Building the container

docker build -t nuage/metro --build-arg git_user=<username> --build-arg git_password=<password> .

The git username and password are used to checkout the Metro sources from git.

### Limitations and caveats

* The container currently asks for the SSH password of the Docker host, twice. This could be optimized
* There was an issue with a missing yum proxy, making it hard to use the container itself (localhost) as the ansible target in environments where a web proxy is used
* The container currently re-generates new .ssh keys every time it is run, this should be changed to store the keys in the current working dir instead
