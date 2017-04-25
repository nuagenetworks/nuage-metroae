#!/bin/bash
set -e

USAGE="Usage: $0 version"

if [ $# -ne 1 ];
then
    echo "Requires exactly 1 argument"
    echo $USAGE
    exit 1
fi

cp ./test/files/build_vars_esx.yml roles/reset_build/files/build_vars.yml
cp ./test/files/test_install_on_esx.yml .
cp ./test/files/test_cleanup_on_esx.yml .

sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml

./metro-ansible reset_build.yml -vvvv
./metro-ansible build.yml -vvvv
./metro-ansible test_install_on_esx.yml -vvvv
#./metro_ansible test_cleanup_on_esx.yml -vvvv
