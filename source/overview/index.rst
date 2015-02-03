Overview
========

Essentia consists of a set of programs that operate on text data (the AQ Tools), a data scanner which catalogs and
organizes your data, and finally a resource manager to apply processing data at scale. Together, these three components
allow users to operate on multiple files across multiple computing nodes as easy as processing a single file on
a single computer.

In order to achieve this scalability, Essentia works on the cloud.  Specifically the Amazon Web Services
infrastructure.  Users not familiar with this cloud based platform may benefit from the brief AWS overview at the
bottom of this page, but more experienced users could skip directly to the Essentia specific links below.

- :doc:`aqtools`
- :doc:`scanner`
- :doc:`rm`

Essentia on AWS
---------------

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

.. toctree::
   :hidden:

   aqtools
   scanner
   rm

