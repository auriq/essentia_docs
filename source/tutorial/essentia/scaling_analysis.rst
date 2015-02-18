*********************
Scaling data analysis
*********************

The previous section described how to launch worker nodes, but for the remainder of the tutorial we just need a
master.  When working in such an environment, we configure Essentia in "local" mode::

  $ ess instance local

Even in local mode, we can demonstrate how easily we can apply commands meant for one file to many files of the same
category.

Tutorial
========

Essentia treats data as a 'stream', similar to Unix pipes.  As an example, lets simply count the lines in one week of
our log files::

  $ for i in {1..7}; do funzip /data/browse_2014090${i}.csv.gz | wc -l ; done


On some systems, you may use ``zcat`` instead of ``funzip``.

The Essentia equivalent is::

  $ ess task stream "2014-09-01" 2014-09-07 "wc -l"

Some notes here.  The ``bash`` version is fairly straightforward in this case, but gets much more complicated if you
want to traverse dates that span weeks, months, or years.  Also, Essentia handles the decompression of the data and
piping it to the command you specify.

Since we are running this command on the master only, each file is processed sequentially.  If we used the cloud
version, the processing would be done in parallel, with each node responsible for a subset of the files.

