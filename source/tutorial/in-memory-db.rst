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




Starting UDB
============
The UDB communicates with network ports 10010-10079, with a unique UDB server daemon running for each port in use.
How many ports to use depends on the circumstance, but you want at least 1 port for each 'primary key'.  For
instance, in our woodworking example we are interested in user behavior so we will be storing data in UDB based
on the hash of the userID.  We assign one UDB server to manage that hash key.
If we wanted for some reason to maintain a set of tables that had a different primary key (say
articleID), we'd want another port for that.


Since this example is simple and we are using only userID as a primary key, we can start the server using the default
port via::

  $ udbd start
  Starting udbd-10010.
  udbd-10010 (9785) started.



Defining Schemas
================
UDB requires a schema so it knows how to treat data sent to it.  An SQL analogy would be the 'CREATE TABLE' command.
UDB supports tables as well, in addition to 'vectors' and 'variables', the use of which will be clear as you proceed
through this tutorial.


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



