#!/bin/bash
set -e

USAGE="Usage: $0 version"

if [ $# -ne 1 ];
then
    echo "Requires exactly 1 argument"
    echo $USAGE
    exit 1
fi

cp ./test/files/build_vars_all.yml roles/reset-build/files/build_vars.yml
cp ./test/files/test_install.yml .
cp ./test/files/test_cleanup.yml .
cp ./test/files/zfb.yml .

# Get IP address of server on which script is being run
IPADDR=`ifconfig | grep netmask | grep broadcast | head -n 1 | awk '{print $2}'`

sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/TARGET_SERVER/${IPADDR}/g" roles/reset-build/files/build_vars.yml

./metro-ansible reset_build.yml -vvvv
./metro-ansible build.yml -vvvv
./metro-ansible test_install.yml -vvvv
./metro-ansible test_cleanup.yml -vvvv
