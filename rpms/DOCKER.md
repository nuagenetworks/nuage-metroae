# Installing Metro playbooks and dependencies with docker container
To run the metro docker conatiner, first import the tar file in to the local docker images
docker import metro.tar metro:v0.0.0
metro:v0.0.0 is the docker image name

To run metro container 
docker run -it --network host --name metro-ctr -v ~/.ssh/:/root/.ssh/   -v /home/caso/nfs-data:/tmp metro:v0.0.0

Above will launch metro container based on the image imported in the previous step and map local root .ssh folder for public key access
and map a local folder with Nuage QCOW2 images to be used by the build playbooks.


After the install, rpm will place the nuage code in the /opt/nuage-metro folder. Also it will install all the pip dependencies and vmware ovftool.

Now the users can go to /opt/nuage-metro-version/ , update build_vars.yml and run the playbooks. 
Updated metro code can be downloaded via git clone.

