#!/bin/bash
###############################################################################
## Metro Automation Engine Setup
##
## Script to install packages required for Nuage Metro Automation Engine. Safe
## to execute multiple times
###############################################################################

###############################################################################
# Configurable parameters
###############################################################################
LOG=./setup.log

###############################################################################
# Global variables
###############################################################################
#
# Flag for final state. Gets set if there is a failure in installing any of
# the required components
#
FAILED=0

#
# Column number to place the status message
#
RES_COL=72

#
# Command to move out to the configured column number
#
MOVE_TO_COL="echo -en \\033[${RES_COL}G"

#
# Command to set the color to SUCCESS (Green)
#
SETCOLOR_SUCCESS="echo -en \\033[1;32m"

#
# Command to set the color to FAILED (Red)
#
SETCOLOR_FAILURE="echo -en \\033[1;31m"

#
# Command to set color to SKIPPED (Cyan)
#
SETCOLOR_SKIPPED="echo -en \\033[1;36m"

#
# Command to set the color back to normal
#
SETCOLOR_NORMAL="echo -en \\033[0;39m"

#
# Directories
#
CURRENT_DIR=`pwd`
INVENTORY_DIR=$CURRENT_DIR/src/inventory

###############################################################################
# Command usage
###############################################################################
function usage {
  echo ""
  echo "Setup for Nuage Networks Metro Automation Engine (MetroAE)"
  echo ""
  echo "Installs all required libraries for MetroAE.  See README.md for"
  echo "more information."
  echo ""
  echo "Usage:"
  echo "    setup.sh [options]"
  echo ""
  echo "Options:"
  echo "    -h, --help:            Displays this help."
  echo "    --set-group <group>:   Sets the ownership of inventory and logs to specified"
  echo "                           group so that other users in the group can access"
  echo "                           these files."
}

###############################################################################
# PrettyPrint green [ OK ] message
###############################################################################
function echo_success() {
  $MOVE_TO_COL
  echo -n "["
  $SETCOLOR_SUCCESS
  echo -n $" OK  "
  $SETCOLOR_NORMAL
  echo -n "]"
  echo -ne "\r"
  echo " [ OK ]" >> $LOG
  return 0
}

###############################################################################
# PrettyPrint red [ FAILED ] message. Also sets the FAILED global variable
###############################################################################
function echo_failure() {
  $MOVE_TO_COL
  echo -n "["
  $SETCOLOR_FAILURE
  echo -n $" ERR "
  $SETCOLOR_NORMAL
  echo -n "]"
  echo -ne "\r"
  echo " [ FAILED ]" >> $LOG
  FAILED=1
  return 1
}

###############################################################################
# PrettyPrint Cyan [ SKIPPED ] message
###############################################################################
function echo_skipped() {
  $MOVE_TO_COL
  echo -n "["
  $SETCOLOR_SKIPPED
  echo -n $" SKIP"
  $SETCOLOR_NORMAL
  echo -n "]"
  echo -ne "\r"
  echo " [ SKIPPED ]" >> $LOG
  return 0
}

###############################################################################
# Check the passed in return value and print success or failure
# param: return_code
###############################################################################
check_retcode() {
  if [ $1 -eq 0 ]
  then
    echo_success
  else
    echo_failure
  fi
  echo
}

###############################################################################
# Print a message on STDOUT and $LOG
# param: message
###############################################################################
function print() {
  echo $*;
  echo $* >> $LOG
}
###############################################################################
# Print a message on STDOUT without newline. Print the message in $LOG
# param: message
###############################################################################
function printn() {
  echo -n $*;
  echo $* >> $LOG
}

###############################################################################
# Check if an executable exists
# param: executable
###############################################################################
function exists() {
  printn "Checking if $1 exists... ";
  which "*" &> $LOG;
  check_retcode $?;
}

###############################################################################
# Check if user executing the script has root privileges
###############################################################################
function check_user_privilege() {
  printn "Checking user privileges... ";
  if [[ $UID -ne 0 ]]
  then
    echo_failure
  else
    echo_success
  fi
  echo
}

###############################################################################
# Check if OS is release 7.x
###############################################################################
function check_os_version() {
  printn "Checking OS version... "
  ver=`rpm -q --whatprovides /etc/redhat-release | tr "[:upper:]" "[:lower:]"`
  echo "DBG: ver=$ver" >> $LOG
  if [[ $ver == *"7."* ]]
  then
    echo_success
  else
    echo_failure
  fi
  echo
}

###############################################################################
# Export HTTPS_PROXY for yum updates if set in /etc/yum.conf
###############################################################################
set_https_proxy() {
  printn "Setting HTTP_PROXY from /etc/yum.conf... "
  # The ^proxy is to skip any commened proxy config line
  grep_out=`grep ^proxy /etc/yum.conf`
  if [ -z "$grep_out" ]
  then
    echo_skipped
  else
    https_proxy=`grep ^proxy /etc/yum.conf | cut -d= -f2`
    export HTTP_PROXY=$https_proxy
    export HTTPS_PROXY=$https_proxy
    print "($https_proxy)"
    echo_success
  fi
}

###############################################################################
# Install the yum packages defined in yum_requirements.txt when 'yum'
# is available on the OS.
# Exits gracefully if package already exists
###############################################################################
yum_install() {
    if hash yum 2>/dev/null; then
        IFS=$'\n'
        for i in $(cat yum_requirements.txt)
        do
            unset IFS
            printn "Installing $i..."
            yum -y install "$i" >> $LOG 2>&1
            check_retcode $?
        done
    fi
}

###############################################################################
# Install the apt packages defined in apt_requirements.txt when 'apt'
# is available on the OS.
# Exits gracefully if package already exists
###############################################################################
apt_install() {
    if hash apt 2>/dev/null; then
        IFS=$'\n'
        for i in $(cat apt_requirements.txt)
        do
            unset IFS
            printn "Installing $i..."
            apt -y install "$i" >> $LOG 2>&1
            check_retcode $?
        done
    fi
}

###############################################################################
# Install the pip modules defined in pip_requirements.txt.
# Exits gracefully if module already exists
###############################################################################
pip_install() {
    IFS=$'\n'
    for i in $(cat pip_requirements.txt)
    do
        unset IFS
        printn "Installing $i..."
        pip install "$i" >> $LOG 2>&1
        check_retcode $?
    done
}

###############################################################################
# Main function
###############################################################################
function main() {

  rm -f $LOG

  echo ""
  print "Setting up Nuage Metro Automation Engine"
  echo ""

  # Make sure script is being run as root or with sudo
  check_user_privilege

  # Exit gracefully if there is not enouch privilages
  if [[ $FAILED -ne 0 ]]
  then
    echo ""
    echo ""
    print "This script has to be run as root or with root privileges. Try again as root or with sudo"
    echo ""
    echo ""
    exit 1
  fi

  # set HTTP_PROXY
  set_https_proxy

  # yum packages
  yum_install

  # apt packages
  apt_install

  # pip packages
  pip_install

  # Check for any failures and print appropriate message
  if [[ $FAILED -ne 0 ]]
  then
    echo ""
    echo ""
    print "There appears to be some errors. Please check $LOG for details"
    echo ""
    echo ""
    exit 1
  else
    echo ""
    print "Setup complete!"
    echo ""
    exit 0
  fi
}

#
# Arg processing
#
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h|--help)
    usage
    exit 0
    ;;
    --set-group)
    GROUP="$2"
    touch ansible.log
    chgrp $GROUP ansible.log
    touch metroae.log
    chgrp $GROUP metroae.log
    chgrp -R $GROUP $INVENTORY_DIR
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

# Entry
main
