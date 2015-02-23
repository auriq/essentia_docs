:tocdepth: 1

**************
Running on AWS
**************

The Amazon cloud is a pay as you need infrastucture, which offers general and specific computing resources,
as well as reliable data storage.  Essentia primarily uses three key AWS components:

1. Elastic Cloud Computing (EC2).  These are 'virtual machines' running on AWS servers that users can provision for
computing.  Once launched, users can log into the machines via the command line (typically `ssh`) and begin their
tasks.  The operating system Essentia uses is a form of Linux that AWS maintains.

2. Simple, Secure Storage (S3).  Essentially this is a place to store your files.  The 'simple' part of S3 is that
for most users, you can think of this as basically a hard drive that is on the cloud.  Data is secure because behind
the scenes, any files uploaded are copied to multiple drives on site in order to prevent data loss due to any failure.
It is this redundancy which also allows for scalability in reading data.  For instance, on your desktop or laptop,
if two files are trying to be read from disk at the same time, the drive has to go back and forth to where the data
is stored.  This slows down the read.  But with multiple disks, this competition can be avoided.

3. Redshift.  This is one of a few types of databases that AWS offers.  It is common in many applications,
including data warehousing.  Data stored in Redshift can be efficiently queried by standard SQL commands.   Essentia
can integrate with Redshift to clean massive amounts of raw, dirty data and insert it directly into SQL tables.

Getting started with AWS is typically free, and interested users can get more information at `the AWS web page
<http://aws.amazon.com>`_.

Scanning and categorizing your data does not require anything other than a single master node.  But the rest of
Essentia benefits greatly when worker nodes are added. This tutorial will walk you through how to launch worker
nodes in the AWS Cloud to scale up your processing.  If you
are using the desktop installer, or simply wish to use just your master node for the the remainder of the tutorials,
that is fine.  Worker nodes are not required for any of the training tutorials here.


Overview
========

Your master node needs a few things in order to spin up workers to build your Essentia cluster.

1. AWS credentials (EC2).  Typically users have a credential file in .csv format that contains the access
   keys that AWS needs to create additional EC2 instances.  Creating these keys can be done via the AWS
   console.  If you have your keys separate from a credential file, you can always create one.

   The credential file has the following form::

     User Name,Access Key Id,Secret Access Key
     **User_Name**,**Access_Key**,**Secret_Key**

   If you plan to run any of the samples scripts provided in the EssentiaPublic github repository, this credential
   file should be in the same directory as you put the github repo.


2. .pem file.  When a user creates an EC2 instance from scratch, they will be asked to indicate (or create) a special
   file that allows them to SSH into the instance.  This file will end with the '.pem' extension, and it contains one
   side of a key pair required for authentication (the ec2 instance you are trying to log into has the other half).

3. ``instance.conf``.  Finally, Essentia requires a configuration file that indicates the name of your credential and
   pem files, plus some other information about the cluster you want to create.

   The format of the included instance.conf is::

     [EC2]
     aws_credential: credential_file
     use_private_ip: False
     instance_tag: Essentia Worker Node
     instance_type:  m3.medium
     instance_count: 2
     key_name: pem_file
     security_groups: essentia-access
     username: ec2-user

   Notes:
   * The pem file entry only does not require the extension (i.e. you should use ``mykey`` instead of ``mykey.pem``)
   * Instance type and count can be overriden by essentia command line options (``--type``, ``--number``)
   * Private IP is appropriate for when you use a VPN
   * More information on setting up a security group can be found in :doc:`../aws/security-group`


Once that is configured, launching worker nodes is done via the following command::

  ess instance ec2 create [--number=] [--type=]

Terminating the cluster when done::

  ess instance ec2 terminate all




