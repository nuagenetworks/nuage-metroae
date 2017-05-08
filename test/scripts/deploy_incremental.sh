#!/bin/sh
set -e

IPADDR=`/usr/sbin/ifconfig | grep netmask | grep broadcast | head -n 1 | awk '{print $2}'`

function run_iter {
    sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
    sed -i "s/TARGET_SERVER/$IPADDR/g" roles/reset-build/files/build_vars.yml
    ./metro-ansible reset_build.yml -vvvv
    ./metro-ansible build.yml -vvvv
    ./metro-ansible $2 -vvvv
}

USAGE="Usage: $0 version"
TESTINSTALL="test_install.yml"
TESTCLEANUP="test_cleanup.yml"
INSTALLVNS="install_vns.yml"

if [ $# -ne 1 ];
then
    echo "Requires exactly 1 argument"
    echo $USAGE
    exit 1
fi

cp ./test/files/test_install.yml .
cp ./test/files/test_cleanup.yml .
cp ./test/files/zfb.yml .

cp ./test/files/build_vars_vsdonly.yml roles/reset-build/files/build_vars.yml
run_iter $1 $TESTINSTALL

cp ./test/files/build_vars_vsconly.yml roles/reset-build/files/build_vars.yml
run_iter $1 $TESTINSTALL

cp ./test/files/build_vars_vstatonly.yml roles/reset-build/files/build_vars.yml
run_iter $1 $TESTINSTALL

cp ./test/files/build_vars_vrsonly.yml roles/reset-build/files/build_vars.yml
run_iter $1 $TESTINSTALL

cp ./test/files/build_vars_vnsonly.yml roles/reset-build/files/build_vars.yml
run_iter $1 $TESTCLEANUP

cp ./test/files/build_vars_vnsonlywithvsc.yml roles/reset-build/files/build_vars.yml
run_iter $1 $INSTALLVNS

cp ./test/files/build_vars_all.yml roles/reset-build/files/build_vars.yml
run_iter $1 $TESTCLEANUP
