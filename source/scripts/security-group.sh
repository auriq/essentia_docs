#!/bin/sh
# ESSENTIA AWS SECURITY GROUP GENERATOR
# Colin Borys, Dec 2, 2013
# AuriQ Systems Inc.
#
#
#
display_usage() {
  echo "This script requires 2 arguments:  "
  echo " group-name   : the name you wish to call this security group."
  echo " trusted-cidr : An ip address range in CIDR notation. Only matching IP"
  echo "                addresses will be able to SSH in to master or worker nodes"
  echo "\nUsage:\n$0 group-name trusted-cidr  \n"
  echo "\nExample:\n$0 essentia-group 192.168.1.0/24"
}
set -e
# if less than two arguments supplied, display usage
if [  $# -le 1 ]
then
  display_usage
  exit 1
fi

group_id=`aws ec2 create-security-group --group-name=${1} --description="Essentia Security Group" | grep -o -e "[a-z]\{2\}-[a-z0-9]\{8\}"`

# allow SSH access from places you trust.
aws ec2 authorize-security-group-ingress --group-name=${1} --protocol tcp --port 22 --cidr ${2}
# allow HTTP access from places you trust.
aws ec2 authorize-security-group-ingress --group-name=${1} --protocol tcp --port 80 --cidr ${2}


