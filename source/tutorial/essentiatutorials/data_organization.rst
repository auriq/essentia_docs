*******************
Data Categorization
*******************

One common theme when performing data analysis is simple accounting. i.e. what files contain what data and where?
Essentia provides a framework for data classification that when, configured, can automatically handle new files as they
are placed in your data store.  It is particularly handy for log data, where new files are created daily or even hourly.
By abstracting out classes of data that share the same properties (i.e. log data from a web server with
one file per day), we can concentrate less on where the data is, and focus on analyzing it.


Getting Started
=================

This tutorial is found under ``tutorials/woodworking/`` of the git repository,
and should be run from that same directory.

In order to utilize the data in the github repository, you need to pull the repository and then select
your local machine as a datastore::

  $ ess select local


Categorization of Data
======================

'Categories' are what Essentia uses to classify data. We define categories based on file patterns.


In this case, a glob pattern of ``*browse*`` would match all of our browsing logs.  It is also helpful to specify an **absolute path** to the files.
to the data as it allows Essentia to skip irrelevant directories. We can tell Essentia to classify
these files as follows::

  $ ess category add browse "$HOME/*tutorials/woodworking/diy_woodworking/*browse*" 


The glob pattern is given, matching files are assigned to a new category we label as 'browse'. Essentia also
automatically exracts a date from the filenames so these files can be organized by time. Sometimes it is necessary to
supply a pattern to help Essentia extract a date from the filename.  This is a regular expression pattern that
uses regular expression classes such as **[:%Y:], [:%m:], and [:%d:]** to designate *year, month, and day fields*.  For example:

:2015-04-30-00-05-22-63C8146U29G91:

  ``[:%Y:]-[:%m:]-[:%d:]-[:%H:]-[:%M:]-[:%S:]-.*``
  Here the automatic extraction alone won't work since there are multiple sets of numbers that could be dates. 
  Therefore we add the ``-``'s and ``.*`` to specify the format of the date in relation to the rest of the filename. 
  Also note that we used **[:%H:], [:%M:], [:%S:]** to designate *hour, minute, and second fields*.

.. tip::
  ``ess ls -r "glob_pattern"`` can be used to list all the files that match a glob pattern.  That same pattern can
  then be used as a rule pattern. The ``-r`` lists files recursively. **Ex:** ``ess ls -r "$HOME/*browse*"``.


With some files now categorized, we can introduce the summary command to get an overview of our data::

  $ ess summary
  ------------------------------------------------------------------------
  -------------------------------- local ---------------------------------
  ------------------------------------------------------------------------
  
  ============================= File summary =============================
  Name      Count    Size       first                last
  ------  -------  -----------  -------------------  -------------------
  browse       30          1M   2014-09-01           2014-09-30 
  

We can see that our 'browse' category has a total of 30 files, takes up 1 MB of storage, and covers the month of September. 
You can also summarize a particlular category to see more information that can be particularly useful, such as how the data is delimited 
and the column specification as explained in the AQ tutorials::  

    $ ess summary browse
    Name:        browse
    Pattern:     /home/essentia/*tutorials/woodworking/diy_woodworking/*browse*
    Exclude:     None
    Date Format: auto
    Date Regex:
    Archive:
    Delimiter:   ,
    # of files:  30
    Total size:  1M Mb
    File range:  2014-09-01 - 2014-09-30
    # columns:   3
    Column Spec: S:eventDate I:userID S:articleID
    Preprocess:
    usecache:    False
    
    First few lines:
    eventDate,userID,articleID
    2014-09-12T00:00:10,8917,50
    2014-09-12T00:00:11,2410,31
    2014-09-12T00:00:11,5121,36
    2014-09-12T00:00:30,9764,35

Elements of a category can be modified. For example, we can override the column spec to treat the userID as a string
and articleID as an integer by using::

  $ ess category change columnspec browse "S:eventDate S:userID I:articleID"

.. note ::
  
  1. Column Specification(Column Spec/ColSpec) specifies how data's columns are interpretted by essentia, and coinsists of column data type, column name, and attributes/options.  For more info, please take a look at :ref:`column spec`. 
  2. The summary about the category above is a good estimate about the category, since essentia scan's a portion of the entire data to gather infomation for efficiency. It's a good practice to check what the data looks like before and after the category is defined. You can use ccommand line tools to do so.

Organizing the 'purchase' data is handled in a similar manner::

  ess category add purchase "$HOME/*tutorials/woodworking/diy_woodworking/*purchase*"
  ess category change columnspec purchase "S:purchaseDate S:userID I:articleID f:price I:refID"


.. seealso ::
  You can apply advanced configuration on category, check out :doc:`/source/reference/manuals/category-rules`


In the next tutorial (Data Processing) we show how to apply operations to files within a group en masse.

Using Category in S3
====================
In practice, sometimes we have to handle data that won't fit in our local machine. In such cases, we can connect s3 as datastore, and define category there.
We can do this in 2 steps.

1. select correct s3 bucket as datastore.
-----------------------------------------
AWS command ``aws s3 ls`` can get you a list of s3 buckets connected to your IAM user. Once you have the bucket name, you can select it as datastore with ``ess select s3://bucket-name``. 
Feel free to select our public bucket (asi-public) as a datastore, and follow along the rest. 

2. find path and create category.
---------------------------------
Once we set up the datastore, we can use ``ess ls`` command to take a look around within the datastore. Think of this command as linux ``ls``, but dedicated to the datastore. With this command, you can find out the path to data files, which is needed to define the category like we did above. 

.. img:: /source/screenshots/ess_tutorial/s3_category.png

Once you have the path, you can use the ``ess category categoryName "path"`` command same way as above to create category.


Future sessions
===============
Essentia keeps track of your datastores and categories using a series of json files located in a ``.ess`` directory on your machine. 
This allows you to access these datastores and your existing categories without providing all of the access credentials and commands needed in the initial setup.
For instance, to access asi-public again simply run the command::

    $ ess select asi-public

A typical scenario, particularly with log data, is that new files are placed on the data store on a regular basis.
After the initial category setup, all future sessions with Essentia need only select the datastore. Then, whenever an existing category is used, Essentia scans the datastore to update its cached file list, indexing new
files and removing from the index any files that were deleted.  Your previous patterns are automatically applied to sort the files into the correct categories. 

This update process can be avoided by using the 
`--usecache <../../reference/category-rules#use-cached-file-list>`_ option in the category creation step. This is paticularly useful if you don't care about the changes to your category's matching files 
or if the number of files in your repository is very large. However, Essentia's cached file list will still be updated anytime a category without the 
``--usecache`` option is used. This can cause your categories utilizing ``--usecache`` to have a different number of matching files than when you created the category, depending on what changes have been made to the repository. 

