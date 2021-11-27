#!/usr/bin/env bash
echo "NESC OPENSTACK - METROAE"
source nesc-openstack-source.sh
status=$?

if [[ $status -ne 0 ]]; then
        echo "Setting default MetroAE NESC OpenStack authencation failure."
        exit 1
    else
        echo "Successfully added authencation. Check it."
        env | grep OS_
    fi

echo ""
echo ""
nova list
status=$?
echo ""
echo "******************************************************END OF THE LIST*****************************************************"

if [[ $status -ne 0 ]]; then
        echo "Error to list down instanses from OpenStack"
        exit 1
fi
echo "Check the list of instances and select."

read -p "Enter instance name:" nesc_instance

openstack server stop myInstance
status=$?

if [[ $status -ne 0 ]]; then
        echo "Failed to stop $nesc_instance. May be that instance is not valid."
        exit 1
fi

echo ""
echo ""
nova list
status=$?
echo ""
echo "******************************************************END OF THE LIST*****************************************************"

if [[ $status -ne 0 ]]; then
        echo "Error to list down instanses from OpenStack"
        exit 1
fi









else
        debug "${FUNCNAME[0]}: Script log is not found"
        sudo docker pull $METRO_AE_IMAGE:$MAX_CONTAINER_VERSION
        status=$?
    fi

    if [[ $status -ne 0 ]]; then
        write_to_screen_and_script_log "Attempt to pull the $MAX_CONTAINER_VERSION MetroAE container image failed. Quitting."
        exit 1
    else
        write_to_screen_and_script_log "Successfully pulled the MetroAE container image from Docker hub"
    fi
    set -e

    return $status

#1.default / user cred + error check msg
#2. list
#3. select instance
#4. do process (make diff functions)

#!/usr/bin/env bash
# To use this file type this command "source nesc-openstack-snapshot.sh"
# To use an OpenStack cloud you need to authenticate against the Identity
# service named keystone, which returns a **Token** and **Service Catalog**.
# The catalog contains the endpoints for all services the user/tenant has
# access to - such as Compute, Image Service, Identity, Object Storage, Block
# Storage, and Networking (code-named nova, glance, keystone, swift,
# cinder, and neutron).
#
# *NOTE*: Using the 3 *Identity API* does not necessarily mean any other
# OpenStack API is version 3. For example, your cloud provider may implement
# Image API v1.1, Block Storage API v2, and Compute API v2.0. OS_AUTH_URL is
# only for the Identity API served through keystone.
export OS_AUTH_URL=http://ch-dc-os-gsn-32.eecloud.nsn-net.net:5000/v3
# With the addition of Keystone we have standardized on the term **project**
# as the entity that owns the resources.
export OS_PROJECT_ID=f36f2db6bb434484b71a45aa84b9d790
export OS_PROJECT_NAME="NI_NME_SERVICES_DELIVERYAUTOMATION_CLOUD"
export OS_USER_DOMAIN_NAME="Default"
if [ -z "$OS_USER_DOMAIN_NAME" ]; then unset OS_USER_DOMAIN_NAME; fi
export OS_PROJECT_DOMAIN_ID="default"
if [ -z "$OS_PROJECT_DOMAIN_ID" ]; then unset OS_PROJECT_DOMAIN_ID; fi
# unset v2.0 items in case set
unset OS_TENANT_ID
unset OS_TENANT_NAME
# In addition to the owning entity (tenant), OpenStack stores the entity
# performing the action as the **user**.
export OS_USERNAME="NI_NME_SERVICES_DELIVERYAUTOMATION_CLOUD"
# With Keystone you pass the keystone password.
# echo "Please enter your OpenStack Password for project $OS_PROJECT_NAME as user $OS_USERNAME: "
# read -sr OS_PASSWORD_INPUT
export OS_PASSWORD="casoCASO1$"
# If your configuration has multiple regions, we set that information here.
# OS_REGION_NAME is optional and only valid in certain environments.
export OS_REGION_NAME="RegionOne"
# Don't leave a blank variable, unset it if it was empty
if [ -z "$OS_REGION_NAME" ]; then unset OS_REGION_NAME; fi
export OS_INTERFACE=public
export OS_IDENTITY_API_VERSION=3