#!/bin/sh
#Running VSD installation script 
set -e

cp ./test/files/setup.yml.VSDStandalone ./setup.yml
ansible-playbook setup.yml
ansible-playbook reset_build.yml
ansible-playbook build.yml
./metro-ansible test_install.yml -vvvv

cp ./test/files/setup.yml.VSCOnly ./setup.yml
ansible-playbook setup.yml
ansible-playbook reset_build.yml
ansible-playbook build.yml
./metro-ansible test_install.yml -vvvv

cp ./test/files/setup.yml ./setup.yml
ansible-playbook setup.yml
ansible-playbook reset_build.yml
ansible-playbook build.yml
./metro-ansible test_cleanup.yml -vvvv

