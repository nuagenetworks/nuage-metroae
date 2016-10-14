#!/bin/sh
cp ./test/files/vns_setup.yml .
ansible-playbook vns_setup.yml
ansible-playbook reset_build.yml
ansible-playbook build.yml
./metro-ansible vns_test.yml -vvvv
