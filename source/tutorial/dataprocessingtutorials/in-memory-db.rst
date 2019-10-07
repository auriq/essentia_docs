******************
In-memory Database
******************


Overview
========

The User (Bucket) Database , or UDB, was developed to complement ``aq_pp``, allowing much more complex
analyses and queries than ``aq_pp`` could do alone.  It is a distributed, hash-based, in memory database.  The `user
bucket` part is derived from our work analyzing digital marketing logs, where we wish to track the behavior of users
across many different log files.  For other types of logs, this 'PRIMARY KEY' can be anything.

Each node in a cluster is responsible for a unique set of keys.  When a node processes data with ``aq_pp``, it looks
up which node in the cluster maintains the data for the particular record being processed, and transports it over the
network to that node.

The data for each unique key is stored using linked lists, and can be sorted on the fly if an optional sort key is
provided. After processing is completed, the data for each key is available in sorted order, in memory, and can be
very quickly queried.

Additionally, the database can be thought of and used as a map/reduce engine. We include an example at the end of
this tutorial.

.. contents:: Table of Contents
   :depth: 3

Getting Started
===============
If you are not already in the ``tutorials/woodworking`` directory used in the previous tutorials, switch into it now.
Our first step is to setup the database to store our data.
As with many database systems, we need to create a database and define schemas.  We concentrate
first on the :ref:`sales data <purchase_data>`::

  $ ess create database wood
  $ ess create table allsales s,pkey:userid i,tkey:ptime i:articleid f:price i:refid
  $ ess create vector usersales s,pkey:userid i,+last:articleid f,+add:total


The first line defines a database called 'wood', and within that we create two things.

Tables
------

The first is a table, which is completely analagous to a TABLE in MySQL (for example).  This table will store all of the sales data.  The
schema for this uses a variant of the column specification we saw in the Data Processing tutorial.

``s,pkey:userid`` indicates that the first column has the label 'userid', that it stores string data,
and will be the data we hash on.  This means that the UDB will store the data in such a way that all entries for a
given user are grouped together.

``i,tkey:ptime`` will store the POSIX time as an integer.  The 'tkey' attributed tells UDB that this column stores
time data, which it can then use to sort user data in time order.


The final 3 columns are more straightforward, simply defining articles as integers and the sales price as a float.

Vectors
-------

Vectors are a bit different.  For each unique hash key, there is one vector of data.  This is commonly used to store
summary information about a key.  In this example, we want to know the total amount of money each user spent,
and we want to know the last article we imported.  The attributes '+add' and '+last' accomplish this. 

There are many other attributes that can be used. For a full list, please see :doc:`../../reference/tables/index`.


Importing data
==============

The database servers are not running by default.  We can fire them up using::

  $ ess udbd start


We can now populate the 'allsales' table using::

  $ ess stream purchase 2014-09-01 2014-09-30 \
  "aq_pp -f,+1,eok - -d %cols \
  -eval i:ptime 'DateToTime(purchaseDate,\"Y.m.d.H.M.S\")' \
  -eval is:t 'ptime - DateToTime(\"2014-09-15\",\"Y.m.d\")' \
  -if -filt 't>0' \
    -eval articleID 'articleID+1' \
  -endif \
  -imp wood:allsales"

This is basically the same as the :ref:`Data Processing example in the previous tutorial <Cleaning_purchase_data>`, with the addition of the
``-imp wood:allsales`` directive.  As with the Data Processing tutorial, ``ess stream`` command is used to stream the ``purchase`` category data into ``aq_pp``, in which the data will be processed. The ``eok`` means to ignore errors (but still report
them).  In this case, a message will be triggered for some of the data because it was designed to have corrupted
fields.  Finally, ``-imp wood:allsales`` is used to import the processed data into ``allsales`` table, within ``wood`` database, as defined above.

Querying the database
=====================
After executing the following, you will see a text dump of the contents of the 'allsales' table::

  $ ess exec "aq_udb -exp wood:allsales"

.. note ::
    In 'local' mode (running in a single computer), users can execute the aq_udb commands directly without using Essentia (``ess exec``). However,
    we recommend using the full command since it can be used immediately if worker nodes are added to the cluster.

You can note that the records are output in groups of same userids, which is how UDB has stored the data.  However, it is not ordered by time within same user.
This can be done by::

  $ ess exec "aq_udb -ord wood:allsales"

``-ord`` option used here sort the record internally, and does not display any output. You can use ``-exp`` option to display the result.

With the data sorted in time order, we can take advantage of our vector that summarizes each user::

  $ ess exec "aq_udb -exp wood:allsales -o,notitle - | \
                   aq_pp -f - -d s:userid X i:articleid f:total X -imp wood:usersales"

What we've done is pipe the output to another UDB import command.  Since the data is grouped by user and in time
order per user, the 'last article read' will be accurately reflected.  Take a look at the summary with another export::

  $ ess exec "aq_udb -exp wood:usersales -sort,dec total -top 10"

Here we have added additional options to sort the output by decending total money spent,
and limiting to the top 10 users.

If you wish to delete the contents of a single table/vector or the entire database you can execute::

  $ ess exec "aq_udb -clr wood:usersales"
  $ ess exec "aq_udb -clr wood"


Map/Reduce, Essentia Style
==========================

The intent of this section is not to teach how the Map/Reduce algorithm works, but rather demonstrate how Essentia can
be used in a manner similar to it.  Beginner tutorials on Map/Reduce almost always demonstrate the 'Word Count'
problem, so it should be conceptually familiar to many.  But if not, the problem is as follows:
We have a large number of files containing text, and wish to count the occurrence of words in this collection of documents.

In a Hadoop implemenation of Map/Reduce, the files are moved onto the Hadoop cluster.  Then a JAVA program is written
to provide 'map' and 'reduce' classes.  The MAP task scans a file (or part of a file) and EMITS a key-value pair of
``{word:1}``.  The key in this pair is mapped to a particular node on the cluster,
meaning that any given node will be responsible for a unique set of keys.  Since the data and MAP tasks are
distributed across the cluster, processing will be fast.


At the end of the MAP phase, dictionaries of the form ``{word:[1,1,1,1]}`` will exist. In the REDUCE phase,
each node goes through the list of keys it is responsible for and outputs a new key-value pair in the form of
``{word:sum}``, which is the result we want.

Essentia is not dissimilar in how it would approach this problem, except we leverage common UNIX tools rather than write
JAVA code to handle the task.  Here is a fully worked example, using the text from the book "A Tale of Two Cities" by
Charles Dickens.  You will find it under ``tutorials/map-reduce`` in the git repository.


.. code-block:: sh
   :linenos:
   :emphasize-lines: 3,5,6

   ess server reset
   ess create database mapreduce
   ess create vector wordcount s,pkey:word i,+add:count
   ess udbd restart
   cat pg98.txt | tr -s '[[:punct:][:space:]]' '\n' | \
                  aq_pp -d s:word -eval i:count 1 -imp mapreduce:wordcount
   aq_udb -exp mapreduce:wordcount -sort,dec count -top 10


Since this is just a single file, we have elected to use the raw ``aq_pp`` rather than wrapping inside of an
Essentia statement (``stream``).  The first line cleans out any old schemas (if they
existed).  The next 2 lines simply setup the schema, with the vector really acting as
an on-the-fly 'REDUCER'.  We then restart the UDB to wipe out any previous content from earlier tutorials.

At this point UDB is ready to accept input.  We use a very common UNIX tool ``tr`` to tokenize input data based on
spaces or punctuation, and then pipe it to ``aq_pp`` which emits a ``{word:1}`` to UDB.

The vector takes care of counting the occurrence of each word on the fly.  Finally, we use aq_udb to output the top 10
most common words.

Advantages over HADOOP
----------------------

For certain applications, Essentia can be much faster than Hadoop when a map/reduce algorithm is called for.  In
particular:

1. Data can be dealt with in its raw form.  No need to move it onto the Hadoop filesystem.
2. Fast. Because it is in-memory, Essentia can perform some operations much more quickly.
3. Low dev time.  No need for lengthy JAVA code.

Altogether, a user can go from raw data to results much more quickly using Essentia for many applications where
Hadoop would normally be used.
