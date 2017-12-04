#!/bin/bash

# exit on non-zero return code
set -e

#
# Start script for Nuage Metro container
#

function show_usage() {
 echo "Copyright (C) 2017 Nuage Networks, all rights reserved. Version 1.0 2017-12-04"
 echo "Usage: docker run -it --rm -v \`pwd\`:/files nuage/simplify" 
 echo "  tip: You can add '--dns:x.x.x.x' to specify a DNS server for the Ansible host (this container) to use"
 echo "  You may have to 'ssh-copy-id -i id_rsa user@target_server' to the target servers"
 echo "  To deploy a subset of servers, you can add '--limit=vstats' ( or vsds, vscs, etc. ) at the end"
 echo "  Also, you may use --tags xxxx to only execute certain tasks"
 
 exit 0
}

if [ $# == 0 ] || [ ! -d /files ]; then
 show_usage
fi

# Always copy Ansible scripts, such that users can customize if needed
cp -Rn simplify /files

# Copy sample config to root dir, if not existing
cp -n simplify/nuage.json /files

# Generate new host key if needed
mkdir -p --mode=700 ~/.ssh 
if [ ! -e /files/id_rsa ]; then
  ssh-keygen -h -f /files/id_rsa -N ''
fi

# Always re-copy, even if already done
# ssh-copy-id -i /files/id_rsa.pub root@127.0.0.1 || exit 1
cp /files/id_rsa* ~/.ssh/ && chmod 600 ~/.ssh/id_rsa*

# Clear Ansible tmp directory
[ -d /files/.ansible/tmp ] && rm -rf /files/.ansible/tmp/*

# Run Ansible playbooks
export ANSIBLE_HOST_KEY_CHECKING=False
export PARAMIKO_HOST_KEY_AUTO_ADD=True
cp /files/nuage.json /files/simplify/

echo "This is a Docker shell. Use <CTRL>-(p + q) to exit while keeping the container running - alias 'deploy' is defined for your convenience"
cat > /etc/profile.d/simplify.sh << EOF
alias deploy="cd /files/simplify && ansible-playbook --key-file=/files/id_rsa deploy.yml"
EOF
/bin/bash
exit $?
