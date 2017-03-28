#!/bin/bash
set -e

USAGE="Usage: $0 version target_host"

if [ $# -ne 2 ];
then
    echo "Requires exactly 2 arguments"
    echo $USAGE
    exit 1
fi

cp ./test/files/build_vars_unzip.yml roles/reset-build/files/build_vars.yml

sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml

./metro-ansible reset_build.yml -vvvv

sed -i "s/TARGET_HOST/$2/g" ./test/nuage_unzip/nuage_unzip_hosts
sed -i "s/localhost/nuage_unzip_targets/g" nuage_unzip.yml
$(which ansible-playbook) -i ./test/nuage_unzip/nuage_unzip_hosts ./nuage_unzip.yml -vvvv
