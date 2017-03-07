#!/bin/bash
set -e

USAGE="Usage: $0 version"
VERSION="Version must be one of 4.0R4, 4.0R7"

if [ $# -ne 1 ];
then
    echo "Requires exactly 1 argument"
    echo $USAGE
    echo $VERSION
    exit 1
fi

if [[ "$1" == "4.0R4" ]]
then
    SFILE="./test/files/setup_4.0R4.yml"
elif [[ "$1" == "4.0R7" ]]
then
    SFILE="./test/files/setup_4.0R7.yml"
else
    echo $VERSION
    echo $USAGE
    exit 1
fi
echo $SFILE

cp $SFILE setup.yml
cp ./test/files/test_install.yml .
cp ./test/files/test_cleanup.yml .

./metro-ansible setup.yml -vvvv
./metro-ansible reset_build.yml -vvvv
./metro-ansible build.yml -vvvv
./metro-ansible test_install.yml -vvvv
./metro-ansible test_cleanup.yml -vvvv
