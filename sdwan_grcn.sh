# tarball file.(We will have that file in testbed, no need to import that)
cp /nfs-data/20.10.R1/nuage-unpacked/vns/portal/nuage-portal-container-20.11.1-65.tar.gz /tmp/

gunzip -c /tmp/nuage-portal-container-20.11.1-65.tar.gz | docker load

#validation
docker images

#configuration script
docker run -ti --rm -v /var/run/docker.sock:/docker.sock -v /opt:/mnt:z -v /etc:/hostetc:z nuage/vnsportal-bootstrap-grcn:20.11.1-65

# check if any .beforeupgrade configuration file is preventing the service from starting
find /opt/vnsportal/ -name *.beforeupgrade

###########################
#configuring SD-WAN for Geo

#modify /opt/vnsportal/dr.sh
export OWNADDRESS=<LOCAL_GRCN_IP>
export DC1=<DC1_HA1>,<DC1_HA2>,<DC1_HA3>,<DC1_GRCN>,<DC2_GRCN>
export DC2=<DC2_HA1>,<DC2_HA2>,<DC2_HA3>,<DC2_GRCN>,<DC2_GRCN>

#Within each datacenter execute
docker run -ti --rm -v /var/run/docker.sock:/docker.sock -v /opt/vnsportal:/mnt:z nuage/vnsportal-installer:20.11.1-65

#Note: Database Security is not supported for geo-redundant deployments.
# 3
# Configure Geo-Redundant options to:
# • Enable
# • Set the datacenter ID (1|2)
# • GRCN Address for DC1
# • GRCN Address for DC2
# The SD-WAN Portal application server (tomcat) does not communicate directly with the
# GRCN.
# Do not add the GRCN addresses to /opt/vnsportal/tomcat-instance1/application.properties.

#Before starting the Nuage SD-WAN Customer Portal, ensure that the VSD is up and running.


#3.5 Control Scripts for the Nuage SD-WAN Customer Portal GRCN
#we can incude this if we need

#command for GRCN for DB cluster initialization operation
#/opt/vnsportal/cluster_bootstrap.sh <DC1|DC2>

#for normal operation or “normal mode”
#/opt/vnsportal/start.sh <DC1|DC2>

#as root user to stop the Nuage SD-WAN GRCN
#/opt/vnsportal/stop.sh

#as root user to restart
#/opt/vnsportal/restart.sh

#as root user to collect all logs, configuration, licenses for the current installation and put these files into a tar file
#/opt/vnsportal/collect.sh

########################
# Verifying Installation

docker ps -a

#If we need these sections, we can include
#3.7 Backing up Databases and Configuration Files
#3.8 Restoring Databases and Configuration Files
#3.9 Uninstalling Nuage SD-WAN Customer Portal GRCN
#3.10 Troubleshooting
#3.11 Verifying Database Cluster Health






