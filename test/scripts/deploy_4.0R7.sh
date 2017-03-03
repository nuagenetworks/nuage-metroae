#!/bin/sh
set -e
cp ./test/files/setup_4.0R7.yml .
ansible-playbook setup_4.0R7.yml -vvvv
ansible-playbook reset_build.yml -vvvv
ansible-playbook build.yml -vvvv
./metro-ansible test_install.yml -vvvv
./metro-ansible test_cleanup.yml -vvvv
