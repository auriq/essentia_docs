********************
In-memory Map/Reduce
********************

Overview
========

The User (Bucket) Database , or UDB, was developed to complement ``aq_pp``, allowing much more complex
analyses and queries than ``aq_pp`` could do alone.  It is a distributed, hash-based, in memory database.  The `user
bucket` part is derived from our work analyzing digital marketing logs, where we wish to track the behavior of users
across many different log files.  For other types of logs, this 'PRIMARY KEY' can be anything.

Each node in cluster is responsible for a unique set of keys.  When a node processes data with ``aq_pp``, it looks
up which node in the cluster maintains the data for the particular record being processed, and transports it over the
network to that node.

The data for each unique key is stored using linked lists, and can be sorted on the fly if an optional sort key is
provided. After processing is completed, the data for each key is available in sorted order, in memory, and can be
very quickly queried.


Getting Started
===============
As with many database systems, we need to create a database and define schemas to store the data.  We concentrate
first on the sales data::

  $ ess spec create database wood
  $ ess spec create table allsales s,hash:userid i,tkey:ptime i:articleid f:price i:refid
  $ ess spec create vector usersales s,hash:userid i,+last:articleid f,+add:total


The first line defines a database called 'wood', and within that we create two things.

Tables
------

The first is a table, which is completely analagous to a TABLE in MySQL (for example).  This table will store all of the sales data.  The
schema for this uses a variant of the column specification we saw in the ETL tutorial.

``s,hash:userid`` indicates that the first column has the label 'userid', that it stores string data,
and will be the data we hash on.  This means that the UDB will store the data in such a way that all entries for a
given user are grouped together.

``i,tkey:ptime`` will store the POSIX time as an integer.  The 'tkey' attributed tells UDB that this column stores
time data, which it can then use to sort user data in time order.


The final 3 columns are more straightforward, simply defining articles as integers and the sales price as a float.

Vectors
-------

Vectors are a bit different.  For each unique hash key, there is one vector of data.  This is commonly used to store
summary information about a key.  In this example, we want to know the total amount of money each user spent,
and we want to know the last article we imported.  The attributes '+last and +sum' accomplish this. There are many
other attributes that can be used. See the :doc:`../reference/index`.


Importing data
==============

The database servers are not running by default.  We can fire them up using::

  $ ess udbd start


We can now populate the 'allsales' table using::

  $ ess task stream purchase 2014-09-01 2014-09-30 \
  "aq_pp -f,+1,eok - -d %cols \
  -evlc i:ptime 'DateToTime(%date_col,\"%date_fmt\")'
  -evlc is:t 'ptime - DateToTime(\"2014-09-15\",\"Y.m.d\")' \
  -if -filt 't>0' \
    -evlc articleID 'articleID+1' \
  -endif \
  -imp wood:allsales

This is basically the same as the ETL example in the previous tutorial, with the addition of the
``-imp wood:allsales`` directive.

Querying the database
=====================
After executing the following, you will see a text dump of the contents of the 'allsales' table::

  $ ess task exec "aq_udb -exp wood:allsales"

.. note ::
    In 'local' mode, users can execute the aq_udb commands directly without using Essentia (``ess task exec``). However
    we recommend using the full command since it can be used immediately if worker nodes are added to the cluster.

You can note that the userids are output in groups, which is how UDB has stored the data.  However it is not in time
order per user.  Than can be done via::

  $ ess task exec "aq_udb -ord wood:allsales"

With the data sorted in time order, we can take advantage of our vector that summarizes each user::

  $ ess task exec "aq_udb -exp wood:allsales -notitle | \
                   aq_pp -f - -d s:userid X i:articleid f:total X -imp wood:usersales"

What we've done is pipe the output to another UDB import command.  Since the data is grouped by user and in time
order per user, the 'last article read' will be accurately reflected.  Take a look at the summary with another export::

  $ ess task exec "aq_udb -exp wood:usersales"


If you wish to delete the contents of a single table/vector or the entire database you can execute::

  $ ess task exec "aq_udb -clr wood:usersales"
  $ ess task exec "aq_udb -clr_all"

