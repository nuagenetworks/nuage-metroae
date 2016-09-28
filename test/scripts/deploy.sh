#!/bin/sh
ansible-playbook ./test/playbooks/setup.yml
ansible-playbook reset_build.yml
ansible-playbook build.yml
./metro-ansible test.yml -vvvv
