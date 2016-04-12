:tocdepth: 1

************************
How To Scale
************************

In this tutorial, we concentrate on using Essentia within the AWS cloud service. 
This tutorial requires one of the cloud based versions of Essentia, 
since the local install of Essentia does not have the ability to create worker nodes and construct an Essentia cluster.

==============================
Running on AWS
==============================

The Amazon cloud is a pay as you need infrastucture, which offers general and specific computing resources,
as well as reliable data storage.  Essentia primarily uses three key AWS components:

1. **Elastic Cloud Computing (EC2).**  These are 'virtual machines' running on AWS servers that users can provision for
computing.  Once launched, users can log into the machines via the command line (typically `ssh`) or via the Essentia Data Lake Manager GUI 
and begin their tasks.  The operating system Essentia uses is a form of Linux that AWS maintains.

2. **Simple, Secure Storage (S3).**  Essentially this is a place to store your files.  The 'simple' part of S3 is that
for most users, you can think of this as basically a hard drive that is on the cloud.  Data is secure because behind
the scenes, any files uploaded are copied to multiple drives on site in order to prevent data loss due to any failure.
It is this redundancy which also allows for scalability in reading data.  For instance, on your desktop or laptop,
if two files are trying to be read from disk at the same time, the drive has to go back and forth to where the data
is stored.  This slows down the read.  But with multiple disks, this competition can be avoided.

3. **Redshift.**  This is one of a few types of databases that AWS offers.  It is common in many applications,
including data warehousing.  Data stored in Redshift can be efficiently queried by standard SQL commands.   Essentia
can integrate with Redshift to clean massive amounts of raw, dirty data and insert it directly into SQL tables.

Getting started with AWS is typically free, and interested users can get more information by reading our :doc:`../../install/aws/aws-account` document. 

.. `the AWS web page <http://aws.amazon.com>`_.

Scanning and categorizing your data does not require anything other than a single master node.  But the rest of
Essentia benefits greatly when worker nodes are added. This tutorial will walk you through how to launch worker
nodes in the AWS Cloud to scale up your processing.  If you
are using the local install or simply wish to use just your master node for the the remainder of the tutorials,
that is fine.  Worker nodes are not required for any of the training tutorials here.

Launching an Essentia Cluster
==============================

If you have setup :doc:`../../install/aws/iam-role`, then all you need to do in order to spin up workers and build your Essentia cluster is run the command::

   ess cluster create [--number=NUMBER] [--type=TYPE]
   
If you have NOT setup IAM Roles yet, then you need to run the command::

   ess cluster create [--number=NUMBER] [--type=TYPE] --credentials=~/your_credential_file.csv

Alternatively, the ``credentials`` flag can be replaced with ``aws_access_key`` and ``aws_secret_access_key`` to directly enter
credentials::
     
   ess cluster create [--number=NUMBER] [--type=TYPE] --aws_access_key=YOUR_ACCESS_KEY --aws_secret_access_key=YOUR_SECRET_ACCESS_KEY

However, we recommend the use of credential files if possible. To create a credential file, simply save your access and secret access keys in the following format to a csv file with a name of your choice::

    User Name,Access Key Id,Secret Access Key
    your_user_name,your_access_key,your_secret_access_key

Parallelizing your Operations
==============================

Once the ``ess cluster create ...`` command has been run, Essentia will launch **NUMBER** of the EC2 virtual machines of type **TYPE**. 
The data and operations will be split up and parallelized across all of these 'worker' virtual machines. 
In particular:

``ess stream category start end command`` will take the files in 'category' between the dates 'start' and 'end', 
and split these files up across all of the worker virtual machines. The virtual machines will run 'command' on each file they receive.

``ess exec command`` will execute 'command' on each of the worker virtual machines.

You can use ``ess stream`` with our Data Processing command ``aq_pp`` to import the data into our :doc:`in-memory-db` to distribute the data across the memory of all of these worker virtual machines. 
It is then easy to analyze or output the data using ``ess exec`` with our Data Processing command ``aq_udb``.

Stopping or Terminating an Essentia Cluster
============================================

EC2 charges for each hour each virtual machine is used. Thus it is good practice to **stop** or **terminate** your virtural machines.

When you are done using your worker virtual machines, you can stop them by running::

  ess cluster stop
  
If you need to use those machines again you can start them by running::

  ess cluster start
  
However, if you no longer need your worker virtual machines and will not need to access those exact machines in the future, you should terminate them. To terminate an Essentia cluster run::

  ess cluster terminate
  
.. note::
   Once terminated, you will no longer have ANY access to the worker virtual machines. You will have to launch a new cluster to parallelize your operations. 




