#!/bin/bash
set -e

USAGE="Usage: $0 target_host"

if [ $# -ne 1 ];
then
    echo "Requires exactly 1 argument"
    echo $USAGE
    exit 1
fi

sed -i "s/TARGET_HOST/$1/g" test/archive_retriever/hosts
$(which ansible-playbook) -i test/archive_retriever/archive_retriever_hosts test/archive_retriever/archive_retriever.yml -vvvv
