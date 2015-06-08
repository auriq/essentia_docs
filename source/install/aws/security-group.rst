AWS Security Groups
-------------------

Security groups define a firewall used to restrict access to AWS resources.
Essentia typically requires 3 firewall settings:

1. SSH (port 22) access to the master node (so you can log into it)
2. SSH access between master node and workers (so master can relay commands)
3. TCP 10010-10079 ports between master and workers for the UDB database.

Covering every organization or user's security preferences or requirements is
beyond the scope of this article.  We present here a simple setup sufficient
for many users.  For more complex configurations, please do contact us.

The strategy is to create an empty security group in order to determine its
ID.  We will then add a rule to allow SSH access to a specific IP
address (typically the system you will access the master node from), and then
allow port 22 and 10010-10079 access to other instances that have the same
security group ID.

Configure via AWS Console
~~~~~~~~~~~~~~~~~~~~~~~~~

#. Log into Amazon AWS services on a web browser and navigate to EC2.￼
#. On the left menu, select “Security Groups”.
#. Click on “Create Security Group” button.
#. Enter a name for the Security group name (example: essentia-access).
#. Enter a description for the current security group (example: Essentia
   Access).
#. Select the VPC the instance belongs to, or “No VPC”.
#. Click on the "Create" button.
#. This will create a security group.  You can look it up in your list of
   security groups.  Do so and note the Group-ID assigned to it.  It will be
   in the form of "sg-XXXXXXXX"
#. Click on this group and select "Inbound"
#. Click on the “Edit” button.
#. Click on the menu arrow for the Type of traffic and choose SSH.
#. Choose where you want to allow access from.  "My IP" (the computer you are
   sitting at), "Anywhere" or "Custom IP".  The 'anywhere' setting is
   strongly discouraged.
#. Click on the “Add Rule” button.
#. Again select SSH access, but in the Source field select Custom IP and enter
   the security group IP.
#. For the final rule, choose “Custom TCP Rule” under the “Type” column.
#. Enter “10010-10079″ in the Port Range column of the current rule.
#. Choose “Custom IP” under the Source column, and type in the security group
   ID.
#. Click the “Save” button on the lower right corner.

This security group will be used by both the master node and all workers.

Setup via the AWS Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Users with the AWS CLI installed may find :download:`this script <../scripts/security-group.sh>` useful.
Simply save it in a file, and execute it using ``sh security-group.sh``

.. code-block:: sh

  #!/bin/sh
  # ESSENTIA AWS SECURITY GROUP GENERATOR
  # Colin Borys, Dec 2, 2014
  # AuriQ Systems Inc.
  #
  display_usage() {
    echo "This script requires 2 arguments:  "
    echo " group-name   : the name you wish to call this security group."
    echo " trusted-cidr : An ip address range in CIDR notation. Only matching"
    echo "                IP addresses will be able to SSH into Essentia nodes"
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

  group_id=`aws ec2 create-security-group --group-name=${1} \
            --description="Essentia Security Group" | grep -o -e "[a-z]\{2\}-[a-z0-9]\{8\}"`
  # allow SSH access from places you trust.
  aws ec2 authorize-security-group-ingress --group-name=${1} --protocol tcp --port 22 --cidr ${2}
  # Allow UDB and SSH communication between ec2 instances of this same group
  aws ec2 authorize-security-group-ingress --group-name=${1} \
                                           --protocol tcp --port 10010-10079 \
                                           --source-group ${group_id}
  aws ec2 authorize-security-group-ingress --group-name=${1} \
                                           --protocol tcp --port 22 \
                                           --source-group ${group_id}
  # allow SSH access from places you trust.
  aws ec2 authorize-security-group-ingress --group-name=${1} --protocol tcp \
                                           --port 22 --cidr ${2}

￼