#!/bin/bash
set -e

sed -i "s/TARGET_HOST/$1/g" test/archive_retriever/hosts

./archive-ansible test/archive_retriever/archive_retriever.yml -vvvv

sed -i "s/$1/TARGET_HOST/g" test/archive_retriever/hosts
