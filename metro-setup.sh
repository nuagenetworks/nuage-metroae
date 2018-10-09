#!/bin/bash
###############################################################################
## Metro Automation enGine Setup
##
## Script to install packages required for Nuage MetroAG. Safe to execute
## multiple times
###############################################################################

###############################################################################
# Configurable parameters
###############################################################################
LOG=./metro-setup.log

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
RES_COL=60

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
# Command to set the color back to normal
#
SETCOLOR_NORMAL="echo -en \\033[0;39m"

###############################################################################
# PrettyPrint green [ OK ] message
###############################################################################
function echo_success() {
  $MOVE_TO_COL
  echo -n "["
  $SETCOLOR_SUCCESS
  echo -n $"  OK  "
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
  echo -n $"FAILED"
  $SETCOLOR_NORMAL
  echo -n "]"
  echo -ne "\r"
  echo " [ FAILED ]" >> $LOG
  FAILED=1
  return 1
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
# Check if OS is CentOS or RHEL
###############################################################################
function check_os_type() {
  # Get the version and convert to lowercase
  ver=`rpm -q --whatprovides /etc/redhat-release | tr "[:upper:]" "[:lower:]"`
  printn "Checking OS type... "
  echo "DBG: ver=$ver" >> $LOG
  if [[ $ver == *"centos"* || $ver == *"redhat"* ]]
  then
    echo_success
  else
    echo_failure
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
# Install the yum package. Exists gracefully if package already exists
# param: packageName
###############################################################################
yum_install() {
  printn "Installing $1..."
  xargs --delimiter=\\n yum -y install < yum_requirements.txt  >> $LOG 2>&1
  check_retcode $?
}

###############################################################################
# Install a pip module. Will exit gracefully if module already exists
# param: module
###############################################################################
pip_install() {
  printn "Installing pip packages"
  pip install -r pip_requirements.txt $1 >> $LOG 2>&1
  check_retcode $?
}

###############################################################################
# Main function
###############################################################################
function main() {

  rm -f $LOG

  echo ""
  print "Setting up Nuage Metro Automation enGine"
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

  # Metro supports only RHEL/CentOS 7.x
  check_os_type;
  check_os_version;

  # yum packages
  yum_install

  #Install pip packages through modules specified in text file and exit gracefully
  pip_install

  # Check for any failures and print appropriate message
  if [[ $FAILED -ne 0 ]]
  then
    echo ""
    echo ""
    print "There appears to be some errors. Please check $LOG for details"
    echo ""
    echo ""
  else
    echo ""
    print "Setup complete!"
    echo ""
  fi
}

# Entry
main
