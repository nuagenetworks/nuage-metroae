#!/bin/sh
set -e

USAGE="Usage: $0 version"

if [ $# -ne 1 ];
then
    echo "Requires exactly 1 argument"
    echo $USAGE
    exit 1
fi

cp ./test/files/setup.yml.CI setup.yml
ansible-playbook setup.yml -vvvv
ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible ci_predeploy.yml -vvvv
./metro-ansible ci_deploy.yml -vvvv

#cp ./test/files/setup_4.0R4.yml .
#ansible-playbook setup_4.0R4.yml -vvvv
cp ./test/files/build_vars_4.0R4.yml.all roles/reset-build/files/build_vars.yml
cp ./test/files/test_install.yml .
cp ./test/files/test_cleanup.yml .

sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml

ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible test_install.yml -vvvv
./metro-ansible test_cleanup.yml -vvvv

./metro-ansible ci_destroy.yml -vvvv
