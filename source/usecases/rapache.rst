*********************
R Apache Analysis
*********************

The R Package
-----------------

In order to use R with Essentia, you must install the RESS package from C-RAN (see installation instructions). 
This package contains two R functions that can be used to capture the output of essentia commands into R, **essQuery** and **read.udb**.

* **essQuery** is used to directly query the database using a single statement. You can call essQuery multiple times to run different statements.
* **read.udb**, on the other hand, reads all of the statements in a file. Thus if you plan to run multiple statements
  that may be somewhat related to each other, it is recommended that you use **read.udb**.

Essentia's Environment
--------------------------

Both functions require an Essentia Bash script to be executed that sets up the Essentia environment and optionally loads data into the UDB database. 

In this case study we need to setup an Essentia environment on our local computer, preprocess our Apache log data with Essentia's etl tools, and then send the data into R for more advanced analysis. 
We save the following commands to setupapache.sh

.. code-block:: sh
   :emphasize-lines: 6,11,16,21,28,36
   
    ess instance local    # Tell essentia to work on your local machine.
    ess udbd stop
    
    ess spec drop database logsapache1
    ess spec create database logsapache1 --ports=1
    # Create a vector to aggregate (count) the number of pages, hits, and bytes seen or used by day.
    ess spec create vector vector1 s,pkey:day i,+add:pagecount i,+add:hitcount i,+add:pagebytes
    
    ess spec drop database logsapache2
    ess spec create database logsapache2 --ports=1
    # Create a vector to aggregate (count) the number of pages, hits, and bytes seen or used by hour.
    ess spec create vector vector2 s,pkey:hour i,+add:pagecount i,+add:hitcount i,+add:pagebytes
    
    ess spec drop database logsapache3
    ess spec create database logsapache3 --ports=1
    # Create a vector to aggregate (count) the number of pages, hits, and bytes seen or used over each month of data.
    ess spec create vector vector3 s,pkey:monthsummary i,+add:pagecount i,+add:hitcount i,+add:pagebytes
    
    ess spec drop database logsapache4
    ess spec create database logsapache4 --ports=1
    # Create a vector to aggregate (count) the number of pages, hits, and bytes seen or used by day of the week.
    ess spec create vector vector4 s,pkey:dayoftheweek i,+add:pagecount i,+add:hitcount i,+add:pagebytes
    
    ess udbd start
    
    ess datastore select ./accesslogs
    ess datastore scan
    # Create a category called 125accesslogs that matches any file with 125-access_log in its filename. Tell essentia that these files have a date in their filenames and that this date has in sequence a 4 digit year, 2 digit month, and 2 digit day.
    ess datastore rule add "*125-access_log*" "125accesslogs" "YYYYMMDD"    
    
    ess datastore probe 125accesslogs --apply
    ess datastore category change 125accesslogs compression none     # Tell essentia that the accesslogs are not compressed
    ess datastore summary
    

    # Stream your access logs from the startdate and enddate you specify into the following command. Use logcnv to specify the format of the records in the access log and convert them to .csv format. Then pipe the data into our preprocessor (aq_pp) and specify which columns you want to keep. Filter on httpstatus so that you only include the 'good' http status codes that correspond to actual views. Create a column that you can aggregate for each record to keep track of hits and another column to group the data by. Filter on accessedfile to eliminate any viewed files that dont have certain elements in their filename. If this filter returns true, count that file as a page and save the file to a column called pageurl. If the filter returns false then the file is not counted as a page. Convert the time column to a date and extract the day ("01"...), dayoftheweek ("Sun"...), and hour ("00" to "23") into their respective columns. Import the modified and reduced data into the four vectors in the databases you defined above so that the attributes defined there can be applied.    
            
    ess task stream 125accesslogs "2014-11-30" "2014-12-07" "logcnv -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] \"' s,clf,hl1:req_line1 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X \
    | aq_pp -emod rt -f,eok - -d ip:ip X X i:time X s:accessedfile X i:httpstatus i:pagebytes X X -filt 'httpstatus == 200 || httpstatus == 304' -evlc i:hitcount '1' -evlc s:monthsummary 'ToS(1)' \
    -if -filt 'accessedfile ~~~ \"*.html[?,#]?*\" || accessedfile ~~~ \"*.htm[?,#]?*\" || accessedfile ~~~ \"*.php[?,#]?*\" || accessedfile ~~~ \"*.asp[?,#]?*\" || accessedfile ~~~ \"*/\" || accessedfile ~~~ \"*.php\"' -evlc i:pagecount '1' -evlc s:pageurl 'accessedfile' \
    -else -evlc pagecount '0' -endif -evlc s:day 'TimeToDate(time,\"%d\")' -evlc s:dayoftheweek 'TimeToDate(time,\"%a\")' -evlc s:hour 'TimeToDate(time,\"%H\")' \
    -ddef -udb_imp logsapache1:vector1 -udb_imp logsapache2:vector2 -udb_imp logsapache3:vector3 -udb_imp logsapache4:vector4" --debug

and then run ``bash setupapache.sh``.

Now we use the functions in the RESS package to query the database and output the results to R. 

read.udb
---------

**read.udb** requires us to save the queries we want run into a file. In this case we save the following queries in queryapache.sh 

.. code-block:: sh
   :emphasize-lines: 1,4 
       
    # This first query exports the data from a vector in the database that contains the counts over the entire month so that it can be read into an R dataframe.
    ess task exec "aq_udb -exp logsapache3:vector3" --debug
    
    # The next three statements export the day, day of the week, and hour vectors from their respective databases, ordering the output by the number of pages seen (in descending order). R will capture the output of each command into an R dataframe.
    ess task exec "aq_udb -exp logsapache1:vector1 -sort pagecount -dec" --debug
    ess task exec "aq_udb -exp logsapache4:vector4 -sort pagecount -dec" --debug
    ess task exec "aq_udb -exp logsapache2:vector2 -sort pagecount -dec" --debug

Since these are all ``ess task exec`` statements and there's no ``#Rignore`` flag in any of the statment lines, read.udb will automatically store their output into R dataframes entitled 
command1, command2, command3, and command4. All we need to do now is run the following R script telling R to use the RESS package, use read.udb on queryapache.sh to load the statements' output into 
R dataframes, and run the additional analysis written in the r script analyzeapache.R 

.. code-block:: sh
   :emphasize-lines: 5,8 
   
    file <- "queryapache.sh"            # store queryapache.sh as file
    rscriptfile <- "analyzeapache.R"    # store apache.R as rscriptfile
    library("RESS")                     # load Essentia's R Integration package
    
    # call read.udb to execute the essentia statements written in queryapache.sh and save them to R dataframes command1 through command4
    read.udb(file)                      
    
    # run the R commands written in analyzeapache.R to analyze the data in the dataframes we just created. Turn echo to TRUE to make the output less results-oriented and easier to debug.
    source(rscriptfile, echo=FALSE)     
    remove(file, rscriptfile)

essQuery
--------
    
We could also have chosen to run these queries using the essQuery function. In this case, there is no need for a separate queryapache.sh file. 
You can simply call essQuery on each statement we want to run. Thus the commands we need to run in R are     
    
.. code-block:: sh
   :emphasize-lines: 4,7,12   
    
    rscriptfile <- "analyzeapache.R"    # store analyzeapache.R as rscriptfile
    library(RESS)                       # load Essentia's R Integration package
    
    # This first query exports the data from a vector in the database that contains the counts over the entire month so that it can be read into R. We save the result in R as a dataframe called command1. However, you can use this output however you want for your own analysis, including piping the output directly into that analysis so that it never has to be saved.
    command1 <- essQuery("aq_udb -exp logsapache3:vector3", "--debug")
    
    # The next three statements export the day, day of the week, and hour vectors from their respective databases, ordering the output by the number of pages seen (in descending order). We send the output of each command directly into R and then save it into an R dataframe.
    command2 <- essQuery("ess task exec", "aq_udb -exp logsapache1:vector1 -sort pagecount -dec", "--debug")
    command3 <- essQuery("ess task exec", "aq_udb -exp logsapache4:vector4 -sort pagecount -dec", "--debug")
    command4 <- essQuery("ess task exec", "aq_udb -exp logsapache2:vector2 -sort pagecount -dec", "--debug")
    
    # run the R commands written in analyzeapache.R to analyze the data in the dataframes we just created. Turn echo to TRUE to make the output less results-oriented and easier to debug.
    source(rscriptfile, echo=FALSE)     
    remove(rscriptfile)
    
Results
_______

The additional analysis described in analyzeapache.R ordered the data by their time segmentation (month,  day of month, day of week, and hour) 
and then graphed each column of counts for each dataframe. The results are three graphs per dataframe: number of pages, hits, and bandwidth by each time segmentation.

.. converted each count to a percent of its max value to put everything on a graphable scale of 0-100, and then graphed each column of counts in a dataframe on the same graph. 

