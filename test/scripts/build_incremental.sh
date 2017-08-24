#!/bin/sh
set -e

IPADDR=`/usr/sbin/ifconfig | grep netmask | grep broadcast | head -n 1 | awk '{print $2}'`

run_iter() {
    sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
    sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml
    sed -i "s/SERVER_TYPE/$2/g" roles/reset-build/files/build_vars.yml
    if [ $2 = vcenter ];
    then
        echo -e "\nvcenter: \n  username: administrator@vsphere.local\n  password: Alcateldc\n  datacenter: Datacenter\n  cluster: Management\n  datastore: datastore" >> roles/reset-build/files/build_vars.yml
    fi
    ./metro-ansible reset_build.yml --extra-vars "test_run=True" -vvvv
    ./metro-ansible build.yml --extra-vars "test_run=True" -vvvv
}

USAGE="Usage: $0 version <kvm|vcenter>:"

if [ $# -ne 2 ];
then
    echo "Requires exactly 2 arguments"
    echo $USAGE
    exit 1
fi

cp ./test/files/build_vars_vsdonly.yml roles/reset-build/files/build_vars.yml
run_iter $1 $2

cp ./test/files/build_vars_vsconly.yml roles/reset-build/files/build_vars.yml
run_iter $1 $2

cp ./test/files/build_vars_vstatonly.yml roles/reset-build/files/build_vars.yml
run_iter $1 $2

cp ./test/files/build_vars_vrsonly.yml roles/reset-build/files/build_vars.yml
run_iter $1 $2

cp ./test/files/build_vars_vnsonly.yml roles/reset-build/files/build_vars.yml
run_iter $1 $2

cp ./test/files/build_vars_all.yml roles/reset-build/files/build_vars.yml
run_iter $1 $2
