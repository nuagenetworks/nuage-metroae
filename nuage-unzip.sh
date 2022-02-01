#!/usr/bin/env bash
# set -ex
#
# Unzips the Nuage Networks software
#

CURRENT_DIR=`pwd`
PLAYBOOK_DIR=$CURRENT_DIR/src/playbooks

function usage {
    echo ""
    echo "Unzips the Nuage Networks software"
    echo ""
    echo "Usage:"
    echo "    " $0 "<zipped_directory>" "<unzip_directory>" "[options]"
    echo ""
    echo "    <zipped_directory>: Directory containing the downloaded zipped Nuage Networks software"
    echo "    <unzip_directory>:  Directory to write unzipped software"
    echo ""
    echo "Options:"
    echo "    -h, --help:     Displays this help."
    echo "    --user:         Unzip as a specific user (by default root)"
    echo "    --yum-proxy:    Sets a proxy address for reaching yum"
    echo ""
}

#
# Parse arguments
#
EXTRA_VARS=()
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h|--help)
    usage
    exit 1
    ;;
    --user)
    EXTRA_VARS+=("-e")
    EXTRA_VARS+=("unzip_user=$2")
    shift # past argument
    shift # past value
    ;;
    --yum-proxy)
    EXTRA_VARS+=("-e")
    EXTRA_VARS+=("yum_proxy=$2")
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

# Missing required arguments, show usage
if [[ $# -lt 2 ]]; then
    usage
    exit 1
fi

# <zipped_directory> argument
ZIPPED_DIR=$CURRENT_DIR/$1
shift

# <unzip_directory> argument
UNZIP_DIR=$CURRENT_DIR/$1
shift

$(which ansible-playbook) $PLAYBOOK_DIR/nuage_unzip.yml -e nuage_zipped_files_dir=$ZIPPED_DIR -e nuage_unzipped_files_dir=$UNZIP_DIR "${EXTRA_VARS[@]}"
