#!/bin/sh
set -e

IPADDR=`/usr/sbin/ifconfig | grep netmask | grep broadcast | head -n 1 | awk '{print $2}'`

function run_iter {
    sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
    sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml
    ./metro-ansible reset_build.yml -vvvv
    ./metro-ansible build.yml -vvvv
}

USAGE="Usage: $0 version"

if [ $# -ne 1 ];
then
    echo "Requires exactly 1 argument"
    echo $USAGE
    exit 1
fi

cp ./test/files/build_vars_vsdonly.yml roles/reset-build/files/build_vars.yml
run_iter $1

cp ./test/files/build_vars_vsconly.yml roles/reset-build/files/build_vars.yml
run_iter $1

cp ./test/files/build_vars_vstatonlywithvsd.yml roles/reset-build/files/build_vars.yml
run_iter $1

cp ./test/files/build_vars_vrsonly.yml roles/reset-build/files/build_vars.yml
run_iter $1

cp ./test/files/build_vars_vnsonlywithvscvsd.yml roles/reset-build/files/build_vars.yml
run_iter $1

cp ./test/files/build_vars_all.yml roles/reset-build/files/build_vars.yml
run_iter $1
