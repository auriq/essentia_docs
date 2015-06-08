*******************
Data Classification
*******************

One common theme when performing data analysis is simple accounting. i.e. what files contain what data and where?
Essentia provides a framework for data classification that when, configured, can automatically handle new files as they
are placed in your data store.  It is particularly handy for log data, where new files are created daily or even hourly.
By abstracting out classes of data that share the same properties (i.e. log data from a web server with
one file per day), we can concentrate less on where the data is, and focus on analyzing it.



Getting Started
===============
This tutorial is found under ``tutorials/woodworking/1-datastore.sh`` of the git repository,
and should be run from that same directory.

Essentia defines a resource that contains data a 'datastore'.  Current datastore types that are supported by Essentia
include a local disk drive, an AWS S3 store (cloud based storage), and an Azure Blob store.  To register the local 
datastore with Essentia you would enter the command::

  $ ess datastore select local

For the version of the files on our public S3 bucket, you would enter::

  $ ess datastore select s3://asi-public --credentials=~/mycredentials.csv

The ``credentials`` flag can be replace with ``aws_access_key`` and ``aws_secret_access_key`` to directly enter
credentials, though we recommend the use of credential files if possible.

For an Azure Blob datastore you would enter::

  $ ess datastore select blob://asi-public --account_name=asipublic
  
This is specifically for our public Azure container. If you wanted to access a private Azure container you would need to 
supply both the appropriate account name and the apporpriate account key as in::

  $ ess datastore select blob://private_container --account_name=associated_account --account_key=associated_key


Categorization of Data
======================

'Categories' are what Essentia uses to classify data. We define categories based on file patterns.


In this case, a glob pattern of ``*browse*`` would match all of our browsing logs.  It is also helpful to specify a path
to the data as it allows Essentia to skip irrelevant directories. We can tell Essentia to classify
these files as follows::

  $ ess datastore category add browse "$HOME/*tutorials/woodworking/diy_woodworking/*browse*" 


The glob pattern is given, matching files are assigned to a new category we label as 'browse'. Essentia also
automatically exracts a date from the filenames so these files can be organized by time. Sometimes it is necessary to
supply a pattern to help Essentia extract a date from the filename.  This is another globular pattern,
but uses Y M D to designate year, month, and day fields.  For example:

:2015-04-30-00-05-22-63C8146U29G91:

  ``Y-M-D-h-m-s-*``
  Here the automatic extraction alone won't work since there are multiple sets of numbers that could be dates. 
  Therefore we add the ``-``'s and ``*`` to specify the format of the date in relation to the rest of the filename. 
  Also note that we used h m s to designate hour, minute, and second fields.

.. tip::
  ``ess datastore ls "*browse*"`` can be used to list all the files that match a glob pattern.  That same pattern can
  then
  be used as a rule pattern.


With some files now categorized, we can introduce the summary command to get an overview of our data::

  $ ess datastore summary
  ------------------------------------------------------------------------
  -------------------------------- local ---------------------------------
  ------------------------------------------------------------------------
  
  ============================= File summary =============================
  Name      Count    Size (MB)  first                last
  ------  -------  -----------  -------------------  -------------------
  browse       30          1.9  2014-09-01 00:00:00  2014-09-30 00:00:00 
  

We can see that our 'browse' category has a total of 30 files, takes up 1.9 MB of storage, and covers the month of September. 
You can also summarize a particlular category to see more information that can be particularly useful, such as how the data is delimited 
and the column specification as explained in the AQ tutorials::  

  $ ess datastore summary browse
  Name:        browse
  Pattern:     /home/ec2-user/*tutorials/woodworking/diy_woodworking/*browse*
  Date Format: auto
  Archive:
  Delimiter:   ,
  # of files:  30
  Total size:  1.9 Mb
  File range:  2014-09-01 00:00:00 - 2014-09-30 00:00:00
  # columns:   3
  Column Spec: S:eventDate I:userID S:articleID
  
  First few lines:
  eventDate,userID,articleID
  2014-09-12T00:00:10,8917,50
  2014-09-12T00:00:11,2410,31
  2014-09-12T00:00:11,5121,36
  2014-09-12T00:00:30,9764,35


Elements of a category can be modified.  For example, we can override the column spec to treat the userID as a string
and articleID as an integer by using::

  $ ess datastore category change columnspec browse "S:eventDate S:userID I:articleID"


Organizing the 'purchase' data is handled in a similar manner::

  ess datastore category add purchase "$HOME/*tutorials/woodworking/diy_woodworking/*purchase*"
  ess datastore category change columnspec purchase "S:purchaseDate S:userID I:articleID f:price I:refID"

In the next tutorial (ETL) we show how to apply operations to files within a group en masse.

Future sessions
===============
Essentia keeps track of your datastores and categories using a series of json files located in a ``.ess`` directory on your machine. 
This allows you to access these datastores and your existing categories without providing all of the access credentials and commands needed in the initial setup.
To access asi-public again simply run the command::

    $ ess datastore select asi-public

A typical scenario, particularly with log data, is that new files are placed on the data store on a regular basis.
After the initial category setup, all future sessions with Essentia need only select the datastore and scan it to index new
files (and remove from the index any that may have been deleted).  Your previous patterns are automatically applied to sort the files into the correct categories.

