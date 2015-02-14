:tocdepth: 3

**********
udb/aq_udb
**********

Overview
========

The User (Bucket) Database , or UDB, was developed to complement ``aq_pp``, allowing much more complex
analyses and queries than ``aq_pp`` could do alone.  It is a distributed, hash-based, in memory database.  The `user
bucket` part is derived from our work analyzing digitial marketing logs, where we wish to track the behavior of users
across many different log files.  For other types of logs, this 'PRIMARY KEY' can be anything.

Each node in cluster is responsible for a unique set of keys.  When a node processes data with ``aq_pp``, it looks
up which node in the cluster maintains the data for the particular record being processed, and transports it over the
network to that node.

The data for each unique key is stored using linked lists, and can be sorted on the fly if an optional sort key is
provided. After processing is completed, the data for each key is available in sorted order, in memory, and can be
very quickly queried.


Required Files
==============
For this tutorial, we provide mock data from a fictional online video streaming service.  Its library however
contains *only* the 20 highest ranked movies (according to some) made prior to 1990.

:download:`top20.csv` stores the list of movies, along with some basic data such as year made and
length of movie in minutes.

The service has two sets of logs.  :download:`viewer_logs.csv` is from the media streaming server, which is
responsible for delivering the video content. It records the date and time a movie was started, the ID of the user
and movie involved, and how long the user watched the movie. :download:`web_logs.csv` comes from the webpage where
users login to use the service.  This web page, in addition to providing
the top 20 list, also offers a recommendation for a movie tailored to that particular user.

Finally, :download:`users.csv` is a lookup table that matches user names to their IDs.

Spec files
==========

.. note::
   Essentia simplifies the use of UDB, therefore some of the following is not directly applicable.  In the Essentia
   tutorials we highlight where the differences are.

UDB requires a schema so it knows how to treat data sent to it.  An SQL analogy would be the 'CREATE TABLE' command.
UDB supports tables as well, in addition to 'vectors' and 'variables', the use of which will be clear as you proceed
through this tutorial.  First we present the spec file that will be used for this tutorial::

  @Server:
  127.0.0.1:10010

  # Table definition for movie view logs.
  @Table:viewlog
  i,tkey:time
  s,hash:userid
  s:moviename
  f:viewfraction

  # Vector: user summary
  @Vector:userstat
  s,hash:userID
  i,+add:totaltime
  s,+last:moviename


The ``@Server`` section provides the IP address and UDB ports for all UDB nodes in the cluster.  This tutorial uses just
a master node, so we use the loopback IP.

Next we define a table with 4 columns that stores a modified version of the viewing logs.  The format of the column
definition is similar to the column spec used in the ``aq_pp`` tutorial.  There is one mandatory attribute, ``hash``.
This is the primary key.  Optionally, a 'tkey' (time key) can be provided.  After data is imported, the number of
records in the table will the same as the number of valid records in the input file.  Here, we store for each movie
seen the user ID, name of the movie, and what fraction of the movie was seen before the user closed the video feed.

A vector is slightly different.  After importing data, it will have as many records as there are unique users in the
input data.  It is often used as a 'summary' of data related to a unique user.  Attributes allowed for a vector
include ``+add`` which means to store a rolling sum of a value during import, and ``+last`` to store the last value
seen during import.  In this example, we will store for each use the total number of minutes they spent watching
movies, plus the last movie they saw.


Starting UDB
------------

Since this example is simple and we are using only 1 port (the default port), we can start the server via::

  $ udbd start
  Starting udbd-10010.
  udbd-10010 (9785) started.

Populate the database
=====================

We now integrate lessons learned from the ``aq_pp`` tutorial with UDB specific flags.

.. code-block:: sh
  :linenos:

  aq_pp -f,+1 viewer_logs.csv -d s:date s:userid i:movieid i:viewtime \
        -evlc i:time 'DateToTime(date,"m.d.Y.H.M.S")' \
        -cmb+1 top20.csv i:movieid s:moviename i:year i:runningtime \
        -evlc f:viewfraction 'ToF(viewtime)/ToF(runningtime)' \
        -udb -spec movies.spec -imp viewlog -imp userstat

Line 2 uses a date to time function to convert the timestamp to a unix time.  We then use the top20 file to fetch the
movie id and movie length.  Line 4 computes the fractional viewing time, and finally the ``-udb`` switches tell
``aq_pp`` to move the records to the UDB.

Query the database
==================

We can query the contents of the UDB via the ``aq_udb`` command::

  aq_udb -spec movies.spec -exp userstat

  "time","userid","moviename","viewfraction"
  1400944370,"1003","The Wizard of Oz",0.29411764705882354
  1400937437,"1006","A Hard Day's Night",0.96551724137931039
  1400930661,"1026","The Third Man",0.967741935483871
  1400921743,"1029","The Wizard of Oz",0.58823529411764708
  1400952852,"1039","All About Eve",0.63043478260869568
  1400967558,"1049","The Adventures of Robin Hood",0.97058823529411764
  1400998502,"1049","Seven Samurai",0.98550724637681164
  1400960821,"1050","The Maltese Falcon",0.97999999999999998


  aq_udb -spec movies.spec -exp viewlog

  "userid","viewtime","moviename"
  "1003",30,"The Wizard of Oz"
  "1006",84,"A Hard Day's Night"
  "1026",90,"The Third Man"
  "1029",60,"The Wizard of Oz"
  "1039",87,"All About Eve"
  "1049",303,"Seven Samurai"
  "1050",98,"The Maltese Falcon"

Although we are not importing a lot of data in this tutorial, it should be noted that the table export provides
output user by user, where each user's records are in time order.



