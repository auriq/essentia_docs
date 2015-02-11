Overview
========

Essentia consists of a set of programs that operate on text data (the AQ Tools), a data scanner which catalogs and
organizes your data, and finally a resource manager to apply processing data at scale. Together, these three components
allow users to operate on multiple files across multiple computing nodes as easy as processing a single file on
a single computer.

In order to achieve this scalability, Essentia works on the cloud.  Specifically the Amazon Web Services
infrastructure.  Users not familiar with this cloud based platform may benefit from the brief AWS overview at the
in the next section, but more experienced users could skip directly to the Essentia specific topics below.

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

.. _aqoverview-label:

The AQ Tools
------------

Written in ``C`` to achieve a high level of performance, the AQ tools are able to manipulate and transform raw input
data into a format more easily handled by other AQ or third party tools.  The key programs include:

aq_pp
  The text preprocessor and Extract-Transform-Load workhorse.  It can validate data,
  filter data based on customizable criterion, do string manipulation, perform math, and merge data from other files.
  In a nutshell, it takes raw, dirty data, and outputs clean, formatted data.

udb/aq_udb
  The UDB is a distributed, hash based, in-memory database.  Each compute node in a cluster is a memory bucket for
  UDB, and each node manages a unique set of keys.  ``aq_udb`` is the command line tool used to query the database. We
  will go into more details later, but essentially this enables a map/reduce style analysis of data.


loginf
  This tool reads the contents of a data file to determine number of rows/columns, the type of each column (string,
  float, etc), and also an estimate of the number of unique values in each column.  This tool is particularly handy
  for data exploration, where the format of the data is not known precisely apriori.

.. _scanneroverview-label:

Data Organization
-----------------

Essentia defines a resource that contains data a 'datastore'.  Current datastore types that are supported by Essentia
include a local disk drive, and an AWS S3 store (cloud based storage).  Regardless of the source,
Essentia can scan the files to organize them, allowing users to quickly process only the data they need to.


Features of the Essentia Scanner include:

1. Rule based grouping of files.  Rules are glob based pattern matching, allowing considerable freedom in selecting
data categories.

2. File scanner.  Essentia will scan the files to determine their common attributes, such as column names, number,
data type, file compression, field delimiter, and so on.  For log data, it also determines the date range that the file
covers.

3. Data summary.  Once rules are established, Essentia will update a master file list each time a scan is run,
and update the category summaries.  These include number of files, combined size in MB, date range covered, and so on.

4. Smart file select.  With files categorized and scanned, it is straightforward to select a subset of the data to
process.  In particular with log data, the user only needs to provide the date range of interest.  No need to provide
full filenames.

.. _rmoverview-label:

Resource Management
-------------------

Essentia leverages the power of the cloud to scale analyses as needed.  One major advantage to using Amazon S3 as a
datastore is that the data is redundantly stored on multiple disks.  This enables multiple files to be read without
being I/O bound.

To harness that, Essentia can launch worker nodes based on AWS EC2 instances.  The master node then coordinates which
files each worker node should process.  This allows for near linear scalability in the processing of many files.