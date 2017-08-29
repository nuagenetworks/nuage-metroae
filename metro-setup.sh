#!/bin/bash

LOG=./metro-setup.log

NORMAL=$(tput sgr0)
GREEN=$(tput setaf 2; tput bold)
YELLOW=$(tput setaf 3)
RED=$(tput setaf 1)


# Column number to place the status message
RES_COL=60
# Command to move out to the configured column number
MOVE_TO_COL="echo -en \\033[${RES_COL}G"
# Command to set the color to SUCCESS (Green)
SETCOLOR_SUCCESS="echo -en \\033[1;32m"
# Command to set the color to FAILED (Red)
SETCOLOR_FAILURE="echo -en \\033[1;31m"
# Command to set the color back to normal
SETCOLOR_NORMAL="echo -en \\033[0;39m"

function echo_failure() {
  $MOVE_TO_COL
  echo -n "["
  $SETCOLOR_FAILURE
  echo -n $"FAILED"
  $SETCOLOR_NORMAL
  echo -n "]"
  echo -ne "\r"
  echo " [ FAILED ]" >> $LOG
  return 1
}

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

function yellow() {
    echo -e "$YELLOW$*$NORMAL"
    echo $* >> $LOG
}

function debug() {
    if [[ $DEBUG ]]
    then
        echo ">>> $*"
    fi
}

check_retcode() {
  if [ $1 -eq 0 ]
  then
    echo_success
  else
    echo_failure
  fi
  echo
}

function print() {
  echo $*;
  echo $* >> $LOG
}

function printn() {
  echo -n $*;
  echo $* >> $LOG
}

function exists() { 
  printn "Checking if $1 exists... ";
  which "*" &> $LOG;
  check_retcode $?;
}

function check_os_type() {
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
}

yum_install() {
  printn "Installing $1... "
  yum install -y $1 >> $LOG 2>&1
  check_retcode $?
}

function main() {

  rm -f $LOG

  echo ""
  echo "Setting up Nuage Metro Automation Engine"
  echo ""

  check_os_type;
  check_os_version;

  yum_install "epel-release"
  yum_install "python2-pip"
  yum_install "python-devel.x86_64"
  yum_install "openssl-devel"
  yum_install "@Development tools"
  yum_install "sshpass"
  yum_install "git"

  echo ""
  echo "Setup complete!"
  echo ""

}

main
