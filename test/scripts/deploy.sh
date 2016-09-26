#!/bin/sh
hostname
pwd
cp ./test/files/build.yml ./roles/reset-build/files/
cp ./test/files/test.yml .
ansible-playbook reset_build.yml
ansible-playbook build.yml
./metro-ansible test.yml -vvvv
