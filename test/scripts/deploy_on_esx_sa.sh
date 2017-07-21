#!/bin/bash
set -e

USAGE="Usage: $0 version testbedID"

if [ $# -ne 2 ];
then
    echo "Requires exactly 2 argument"
    echo $USAGE
    exit 1
fi

cp ./test/files/build_vars_esx_sa.yml roles/reset-build/files/build_vars.yml
cp ./test/files/test_install_on_esx.yml .
cp ./test/files/test_cleanup_on_esx.yml .

TESTBED_ID=$2
TESTBED_IP=$((TESTBED_ID+1))

sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/TESTBED_ID/$TESTBED_ID/g" roles/reset-build/files/build_vars.yml
sed -i "s/TESTBED_IP/$TESTBED_IP/g" roles/reset-build/files/build_vars.yml

./metro-ansible reset_build.yml -vvvv
./metro-ansible build.yml -vvvv
./metro-ansible test_install_on_esx.yml -vvvv
./metro_ansible test_cleanup_on_esx.yml -vvvv
