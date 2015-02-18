*******************
Data Classification
*******************

While the AQ tools provide efficient processing of files, they alone are insufficient for dealing with *many* files.
In large part this is due simply to data accounting. i.e. what files contain what data and where?

Essentia provides a framework for data classification that when configured, can automatically add new files as they
are placed in your data store.  It is particularly handy for log data, where new files are created daily or even hourly.

Description of Tutorial Data
============================

In this and the remaining Essentia tutorials, we will be using a synthetic set of log files collected from a
fictional DIY woodworking web site.  This web site offers detailed construction plans for many items.  Users can
browse part of the article for free, but must pay to obtain the full plan. It is a new service,
and in order to determine how best to price the items, the site randomized the prices for each
set of plans over a 1 month period (prices range from 1 to 6 dollars).

There are two sets of log files.  The first have a filename in the form of ``browse_YYYYMMDD.csv.gz`` and contain the
browsing records of all users who visited the site on a given day.  The files have three columns of data:

:eventDate:
    is a timestamp of when the user visited a page.
:userID:
    is a numerical ID matched to a unique user.
:articleID:
    is a unique identifier for each of the articles offered


The second set of logs record all purchases, and have 5 columns of data:

:purchaseDate:
    time and date article was purchased
:userID:
    User that purchased article
:articleID:
    ID of the article purchased
:price:
    price user paid for the article
:refID:
    ID of the article seen just prior to the one being purchased.


Tutorial
========

The first thing Essentia needs to know is where to look for the data.  Assuming we dumped all the files on our hard
drive in the ``/data`` directory, the command to register the store with Essentia is::

  $ ess datastore select /data

For the version of the files on our public S3 bucket, you would enter::

  $ ess datastore select s3://asi-public/diy_woodworking --credentials=~/mycredentials.csv

The ``credentials`` flag can be replace with ``aws_access_key`` and ``aws_secret_access_key`` to directly enter
credentials, though we recommend the use of credential files if possible.

Next we will scan the contents of the datastore::

  $ ess datastore scan
  Essentia (INFO)	 : Cross referencing current index with file list at source.
  Essentia (INFO)	 : - Adding 60 entries to fileindex.
  Essentia (INFO)	 : Applying 2 rules to 60 files.

'Rules' are what Essentia uses to classify data.  There are two system rules: 'default' matches a file if no other
other rule catches it, and 'ignore' is a special rule that can be used to exclude files.  For the rest,
we need to define rules based on file patterns.


In this case, a glob pattern of ``*browse*`` would match all of our browsing logs.  We can tell Essentia to classify
these files as follows::

  $ ess datastore rule add "*browse*" browse YYYYMMDD


The glob pattern is given, matching files are assigned to a new category we label as 'browse',
and finally we supply a pattern that can be used to extract a date from the filename.  It is regex based,
but uses Y M D to designate year, month, and day fields.  Some examples:

:file_2014-06-09_out.zip:

  ``YYYY-MM-DD``

:account12345678_20140609.csv:

  ``YYYYMMDD.csv``
  Here 'YYYYMMDD' alone won't work since there is another 8 digit number, therefore we add the '.csv'.  In fact, just '.' would have been sufficient.

.. tip::
  ``ess datastore ls "*browse*"`` can be used to list all the files that match a glob pattern.  That same pattern can
  then
  be used as a rule pattern.

A future version of Essentia will automatically determine the date from the filename (if present),
but for now it must be explicitly given.

With some files now categorized, we can introduce the summary command to get an overview of our data::

  $ ess datastore summary
  ========================================================================
  ============================= Local://data =============================
  ========================================================================

  Name       Count    Size (MB)    Comp.    Delim.    dateCol    dateFmt    TZ  first       last
  -------  -------  -----------  -------  --------  ---------  ---------  ----  ----------  ----------
  default       30            0
  ignore         0
  browse        30            1                                                 2014-09-01  2014-09-30

  Name      columnSpec
  ------  ------------
  browse

  Name    Example file
  ------  ----------------------------
  browse  /data/browse_20140930.csv.gz

    priority  filePattern    categoryName    dateFormat
  ----------  -------------  --------------  ------------
           1  *browse*       browse          YYYYMMDD


We can see that our 'browse' category has files covering the month of September, but a lot of the other information
is blank.  In particular, Essentia needs to know the compression format, how the data is delimited,
and the column specification as explained in the AQ tutorials.  Optional but highly useful for log based data are
knowing which column stores the time stamp, and the format of the timestamp.

This information can be all be gleaned manually, but we prove a 'probe' which will scan one of the log files to
determine the information::

  $ ess datastore probe browse --apply
  Essentia (INFO)	 : scanning /data/browse_20140924.csv.gz
  Essentia (INFO)	 : scan complete. 25 records found
  Essentia (INFO)	 : examining file
  S:eventDate I:userID I:articleID
  Essentia (INFO)	 : file examination complete.
  Summary for /data/browse_20140924.csv.gz
  compression  : gzip
  delimiter    : csv
  dateColumn   : eventDate
  example date : 2014-09-24T00:00:04
  tz           : None
  column spec  : S:eventDate I:userID I:articleID


The ``--apply`` switch tells Essentia to update the database with the information it found.

Elements of a category can be modified.  For example, we can override the column spec to treat the userID as a string
by using::

  $ ess datastore category change columnSpec "S:eventDate S:userID I:articleID"


Databases
---------

Essentia keeps track of your files, categories, and rules using a database. It is a simple sqlite3 database stored in
a file called ``.auriq.db``.  For datastores on your local disk, the index file is stored in the directory where the
data is stored.  For S3 based stores, the index is initially cached in your ``.conf`` subdirectory (relative to your
working directory).  It can be pushed on the S3 store by using::

  $ ess datastore push

The next time you select this datastore (i.e. in a future session), this index file will be pulled from S3 into your
``.conf`` directory.  You can make changes and optionally push it back.

To completely delete the index file, use::

 $ ess datastore purge


Future sessions
---------------

A typical scenario, particularly with log data, is that new files are placed on the data store on a regular basis.
After the initial setup, all future sessions with Essentia need only select the datastore and scan it to index new
files (and remove from the index any that may have been deleted).  The rules are automatically applied.

