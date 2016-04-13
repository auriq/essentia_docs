***********************
Data Processing: Part 1
***********************

The goal of this tutorial is to highlight how to perform complex data transformation and validation operations,
and output the results either to disk or a database. 

Getting Started
===============

Again we'll use the ``tutorials/woodworking`` directory from the git repository.

Essentia treats data as a **stream**, similar to Unix pipes.  As an example, let's simply count the lines in one week of
the log files that we classified in the previous tutorial::

  $ for i in {1..7}; do gunzip ./diy_woodworking/browse_2014090${i}.gz | wc -l ; done


On some systems, you may use ``zcat`` instead of ``gunzip``.

The Essentia equivalent is::

  $ ess stream browse 2014-09-01 2014-09-07 'wc -l'

Some notes here.  The ``bash`` version is fairly straightforward in this case, but gets much more complicated if you
want to traverse dates that span weeks, months, or years.  Essentia handles the decompression of the data and
piping it to the command you specify.  All you need to do is specify the **category** and **date range** to process.

The **date range** you specify in the stream statement **MUST** match the granularity of the date you extracted from the files in your category. 
Thus, if you extracted the date, hour, and minute when you set up your category, you must specify:: 

    ess stream category "start_date hour:minute" "end_date hour:minute" command
    
Similarly, if you extracted just the date and hour when you set up your category, you must specify::

    ess stream category "start_date hour" "end_date hour" command
    
Failing to do this may lead to ``ess stream`` sending unexpected data to your command and could affect your results.

Since we are in **local** mode, each file is processed sequentially.  If we had worker nodes (i.e. the **cloud** version),
the processing would be done in parallel, with each node responsible for a subset of the files.

This tutorial continues here: :doc:`../dataprocessingtutorials/etl`. That tutorial involves more complex Data Processing examples and uses our **Data Processing (AQ) commands**.
