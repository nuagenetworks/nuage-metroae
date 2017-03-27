#!/bin/bash
set -e

USAGE="Usage: $0 version"

if [ $# -ne 1 ];
then
    echo "Requires exactly 1 argument"
    echo $USAGE
    exit 1
fi

cp ./test/files/build_vars_unzip.yml roles/reset-build/files/build_vars.yml

sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml

./metro-ansible reset_build.yml -vvvv
ansible-playbook nuage_unzip.yml -u root -vvvv
