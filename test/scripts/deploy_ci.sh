#!/bin/sh
set -e

cp ./test/files/setup.yml.CI setup.yml
ansible-playbook setup.yml -vvv
ansible-playbook reset_build.yml -vv
ansible-playbook build.yml -vv
./metro-ansible ci_predeploy.yml -vvvv
./metro-ansible ci_deploy.yml -vvvv
ansible-playbook reset_build.yml -vv
ansible-playbook build.yml -vv
#./metro-ansible test.yml -vvvv
