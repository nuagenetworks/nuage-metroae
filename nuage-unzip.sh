#!/usr/bin/env bash
# set -ex
#
# Unzips the Nuage Networks software
#

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
    echo ""

usage
