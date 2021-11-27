#!/usr/bin/env bash
export OS_AUTH_URL=http://ch-dc-os-gsn-32.eecloud.nsn-net.net:5000/v3
export OS_PROJECT_ID=f36f2db6bb434484b71a45aa84b9d790
export OS_PROJECT_NAME="NI_NME_SERVICES_DELIVERYAUTOMATION_CLOUD"
export OS_USER_DOMAIN_NAME="Default"
if [ -z "$OS_USER_DOMAIN_NAME" ]; then unset OS_USER_DOMAIN_NAME; fi
export OS_PROJECT_DOMAIN_ID="default"
if [ -z "$OS_PROJECT_DOMAIN_ID" ]; then unset OS_PROJECT_DOMAIN_ID; fi

unset OS_TENANT_ID
unset OS_TENANT_NAME

export OS_USERNAME="NI_NME_SERVICES_DELIVERYAUTOMATION_CLOUD"
export OS_PASSWORD="casoCASO1$"
export OS_REGION_NAME="RegionOne"

if [ -z "$OS_REGION_NAME" ]; then unset OS_REGION_NAME; fi
export OS_INTERFACE=public
export OS_IDENTITY_API_VERSION=3