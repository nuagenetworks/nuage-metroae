#!/bin/sh
cp ./test/files/setup.yml .
ansible-playbook setup.yml
ansible-playbook reset_build.yml
ansible-playbook build.yml
./metro-ansible test.yml -vvvv
