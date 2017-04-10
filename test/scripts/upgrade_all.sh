#!/bin/bash
set -e

USAGE="Usage: $0 current version upgrade version"

if [ $# -ne 2 ];
then
    echo "Requires exactly 2 arguments: current and upgrade versions"
    echo $USAGE
    exit 1
fi

cp ./test/files/build_vars.yml.clustered_vsd roles/reset-build/files/build_vars.yml
cp ./test/files/upgrade_vars.yml.clustered_vsd roles/reset-build/files/upgrade_vars.yml
cp ./test/files/test_install.yml .
cp ./test/files/test_cleanup.yml .

sed -i "s/VERSION/$1/g" roles/reset-build/files/build_vars.yml
sed -i "s/VERSION/$2/g" roles/reset-build/files/upgrade_vars.yml

# generate build vars for deployment
./metro-ansible reset_build.yml -vvvv
./metro-ansible build.yml -vvvv
# run the VSP deployment
./metro-ansible test_install.yml -vvvv
#delete any vsd backups and reports from previous jobs
rm -rf /tmp/backup
rm -rf ./reports/
# create build vars required for upgrade
./metro-ansible build_upgrade.yml -vvvv
# run the VSP upgrade
./metro-ansible vsp_upgrade.yml -vvvv
# clean up the whole setup except vrss
./metro-ansible test_cleanup.yml -vvvv
