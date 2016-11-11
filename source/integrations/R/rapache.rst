*********************
R Apache Analysis
*********************

Essentia's Environment
======================

In this case study we only utilize ``essQuery`` and ``capture.essentia``. Both functions require a ``bash`` script to be executed that sets up the Essentia environment and optionally
loads data into the UDB database.

The script and the data used in this brief demo can be found on the git repository under ``casestudies/apache``.  The script
is called ``setupapache.sh``.

In this case study we need to setup an Essentia environment on our local computer, preprocess our Apache log
data with Essentia's Data Processing tools, and then send the data into R for more advanced analysis. We save the
following commands to ``setupapache.sh``

.. literalinclude:: ../../EssentiaPublic/casestudies/apache/setupapache.sh
   :language: bash
   :linenos:
   :emphasize-lines: 5,9,13,17,23-24,39-44
   
..    ess udbd stop
    ess server reset
    
    ess create database logsapache1 --ports=1
    # Create a vector to aggregate (count) the number of pages, hits, and bytes seen or used by day.
    ess create vector vector1 s,pkey:day i,+add:pagecount i,+add:hitcount i,+add:pagebytes
    
    ess create database logsapache2 --ports=1
    # Create a vector to aggregate (count) the number of pages, hits, and bytes seen or used by hour.
    ess create vector vector2 s,pkey:hour i,+add:pagecount i,+add:hitcount i,+add:pagebytes
    
    ess create database logsapache3 --ports=1
    # Create a vector to aggregate (count) the number of pages, hits, and bytes seen or used over each month of data.
    ess create vector vector3 s,pkey:month i,+add:pagecount i,+add:hitcount i,+add:pagebytes
    
    ess create database logsapache4 --ports=1
    # Create a vector to aggregate (count) the number of pages, hits, and bytes seen or used by day of the week.
    ess create vector vector4 s,pkey:dayoftheweek i,+add:pagecount i,+add:hitcount i,+add:pagebytes
    
    ess udbd start
    
    ess select local
    # Create a category called 125accesslogs that matches any file with 125-access_log in its filename. Tell essentia that these files have a date in their filenames and that this date has in sequence a 4 digit year, 2 digit month, and 2 digit day.
    ess category add 125accesslogs "$HOME/*accesslog*125-access_log*"    
    
    ess summary
    

    # Stream your access logs from the startdate and enddate you specify into the following command. Use logcnv to specify the format of the records in the access log and convert them to .csv format. Then pipe the data into our preprocessor (aq_pp) and specify which columns you want to keep. Filter on httpstatus so that you only include the 'good' http status codes that correspond to actual views. Create a column that you can aggregate for each record to keep track of hits and another column to group the data by. Filter on accessedfile to eliminate any viewed files that dont have certain elements in their filename. If this filter returns true, count that file as a page and save the file to a column called pageurl. If the filter returns false then the file is not counted as a page. Convert the time column to a date and extract the month ("December"...), day ("01"...), dayoftheweek ("Sun"...), and hour ("00" to "23") into their respective columns. Import the modified and reduced data into the four vectors in the databases you defined above so that the attributes defined there can be applied.    
            
    ess stream 125accesslogs "2014-11-09" "2014-12-07" "logcnv -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] \"' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X \
    | aq_pp -f,eok - -d ip:ip X X i:time X s:accessedfile X i:httpstatus i:pagebytes X X -filt 'httpstatus == 200 || httpstatus == 304' -eval i:hitcount '1' \
    -if -filt '(PatCmp(accessedfile, \"*.html[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*.htm[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*.php[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*.asp[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*/\", \"ncas\") || PatCmp(accessedfile, \"*.php\", \"ncas\"))' -eval i:pagecount '1' -eval s:pageurl 'accessedfile' \
    -else -eval pagecount '0' -endif -eval s:month 'TimeToDate(time,\"%B\")' -eval s:day 'TimeToDate(time,\"%d\")' -eval s:dayoftheweek 'TimeToDate(time,\"%a\")' -eval s:hour 'TimeToDate(time,\"%H\")' \
    -ddef -udb -imp logsapache1:vector1 -udb -imp logsapache2:vector2 -udb -imp logsapache3:vector3 -udb -imp logsapache4:vector4" --debug

and then run ``sh setupapache.sh``.

Now we use the functions in the RESS package to query the database and output the results to R. 

capture.essentia
================

**capture.essentia** requires us to save the queries we want run into a file. In this case we save the following
queries in ``queryapache.sh``

.. code-block:: sh
   :emphasize-lines: 1,4 
       
    # This first query exports the data from a vector in the database that contains the counts over each month so that it can be read into an R dataframe.
    ess exec "aq_udb -exp logsapache3:vector3"
    
    # The next three statements export the day, day of the week, and hour vectors from their respective databases, ordering the output by the number of pages seen (in descending order). R will capture the output of each command into an R dataframe.
    ess exec "aq_udb -exp logsapache1:vector1 -sort,dec pagecount"
    ess exec "aq_udb -exp logsapache4:vector4 -sort,dec pagecount"
    ess exec "aq_udb -exp logsapache2:vector2 -sort.dec pagecount"

Since these are all ``ess exec`` statements and there are no ``#Rignore`` flags in any of the statement lines,
**capture.essentia** will automatically store their output into R dataframes entitled
command1, command2, command3, and command4. All we need to do now is run the following R
script telling R to use the RESS package, use **capture.essentia** on ``queryapache.sh`` to load the statements' output into
R dataframes, and run the additional analysis written in the r script ``analyzeapache.R``

.. code-block:: sh
   :emphasize-lines: 3,6 
   
    library("RESS")                     # load Essentia's R Integration package
    
    # call capture.essentia to execute the essentia statements written in queryapache.sh and save them to R dataframes command1 through command4
    capture.essentia("queryapache.sh")                      
    
    # run the R commands written in analyzeapache.R to analyze the data in the dataframes we just created. Turn echo to TRUE to make the output less results-oriented and easier to debug.
    source("analyzeapache.R", echo=FALSE)     

essQuery
========
    
We could also have chosen to run these queries using the **essQuery** function. In this case, there is no need for a separate queryapache.sh file. 
You can simply call **essQuery** on each statement we want to run. Thus the commands we need to run in R are     
    
.. code-block:: sh
   :emphasize-lines: 3,6,11   
    
    library(RESS)                       # load Essentia's R Integration package
    
    # This first query exports the data from a vector in the database that contains the counts over each month so that it can be read into R. We save the result in R as a dataframe called command1. However, you can use this output however you want for your own analysis, including piping the output directly into that analysis so that it never has to be saved.
    command1 <- essQuery("aq_udb -exp logsapache3:vector3")
    
    # The next three statements export the day, day of the week, and hour vectors from their respective databases, ordering the output by the number of pages seen (in descending order). We send the output of each command directly into R and then save it into an R dataframe.
    command2 <- essQuery("ess exec", "aq_udb -exp logsapache1:vector1 -sort,dec pagecount")
    command3 <- essQuery("ess exec", "aq_udb -exp logsapache4:vector4 -sort,dec pagecount")
    command4 <- essQuery("ess exec", "aq_udb -exp logsapache2:vector2 -sort,dec pagecount")
    
    # run the R commands written in analyzeapache.R to analyze the data in the dataframes we just created. Turn echo to TRUE to make the output less results-oriented and easier to debug.
    source("analyzeapache.R", echo=FALSE)     
    
Results
=======

The additional analysis described in ``analyzeapache.R`` ordered the data by their time segmentation (month,
day of month, day of week, and hour) and then graphed each column of counts for each dataframe. The results
are three graphs per dataframe: number of pages, hits, and bandwidth by each time segmentation.
