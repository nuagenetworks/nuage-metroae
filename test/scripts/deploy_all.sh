#!/bin/sh
#Running VSD installation script 
cp ./test/files/setup.yml.VSDStandalone ./setup.yml
ansible-playbook setup.yml
ansible-playbook reset_build.yml
ansible-playbook build.yml
./metro-ansible test.yml -vvvv

cp ./test/files/setup.yml.VSCOnly ./setup.yml
ansible-playbook setup.yml
ansible-playbook reset_build.yml
ansible-playbook build.yml
./metro-ansible test.yml -vvvv

cp ./test/files/setup.yml.all ./setup.yml
ansible-playbook setup.yml
ansible-playbook reset_build.yml
ansible-playbook build.yml
./metro-ansible test.yml -vvvv

