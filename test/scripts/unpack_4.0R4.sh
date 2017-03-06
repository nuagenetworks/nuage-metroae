#!/bin/sh
set -e
cp ./test/files/setup_4.0R4.yml setup.yml
ansible-playbook setup.yml -vvvv
ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible test_unpack -vvvv
