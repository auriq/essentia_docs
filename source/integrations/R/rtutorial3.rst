****************************************
Aq Log Data
****************************************

Essentia's Environment
======================

In this tutorial we just want to setup a simple Essentia environment, one that runs on our local computer and scans our local 
filesystem for the aq log data data located in the ``casestudies/aq/aqlogs`` directory. 
If you are not already in the ``casestudies/aq/`` directory, please switch into it now.
We save the following commands to ``aqlog.sh``:

.. literalinclude:: ../../EssentiaPublic/casestudies/aq/aqlog.sh
   :language: bash
   :linenos:
   :emphasize-lines: 6,10,14,18,43-48

..    ess udbd stop
    ess server reset
    
    ess create database aqlogday --ports=1
    ess create vector aqlogday s,pkey:day i,+add:pagecount i,+add:hitcount 
    # Create a vector to aggregate (count) the number of pages and hits seen or used by day.
    
    ess create database aqloghour --ports=1
    ess create vector aqloghour s,pkey:hour i,+add:pagecount i,+add:hitcount 
    # Create a vector to aggregate (count) the number of pages and hits seen or used by hour.
    
    ess create database aqlogmonth --ports=1
    ess create vector aqlogmonth s,pkey:month i,+add:pagecount i,+add:hitcount 
    # Create a vector to aggregate (count) the number of pages and hits seen or used over each month of data.
    
    ess create database aqlogdayoftheweek --ports=1
    ess create vector aqlogdayoftheweek s,pkey:dayoftheweek i,+add:pagecount i,+add:hitcount 
    # Create a vector to aggregate (count) the number of pages and hits seen or used by day of the week.
    
    ess udbd start
    
    ess select local
    
    ess category add aqlogs "$HOME/*/casestudies/aq/aqlogs/*.gz" --dateformat "*-d-YMD-*" 
    
    ess summary
    
    ess stream aqlogs "2014-06-13" "2014-08-15" "aq_pp -f,+1,eok - -d %cols -filt 'status == 200 || status == 304' -eval i:hitcount '1' \
    -if -filt '(PatCmp(page, \"*.html[?,#]?*\", \"ncas\") || PatCmp(page, \"*.htm[?,#]?*\", \"ncas\") || PatCmp(page, \"*.php[?,#]?*\", \"ncas\") || PatCmp(page, \"*.asp[?,#]?*\", \"ncas\") || PatCmp(page, \"*/\", \"ncas\") || PatCmp(page, \"*.php\", \"ncas\"))' -eval i:pagecount '1' -eval s:pageurl 'page' \
    -else -eval pagecount '0' -endif -eval s:month 'TimeToDate(t,\"%B\")' -eval s:day 'TimeToDate(t,\"%d\")' -eval s:dayoftheweek 'TimeToDate(t,\"%a\")' -eval s:hour 'TimeToDate(t,\"%H\")' \
    -ddef -udb -imp aqlogday:aqlogday -imp aqloghour:aqloghour -imp aqlogmonth:aqlogmonth -imp aqlogdayoftheweek:aqlogdayoftheweek" --debug
    
    # Stream your aq logs from the startdate and enddate you specify into the following command. 
    # Then pipe the data into our preprocessor (aq_pp) and tell Essentia to use the column specification it determined. Filter on status so that you only include the 'good' http status codes that correspond to actual views.
    # Create a column that you can aggregate for each record to keep track of hits and another column to group the data by. Filter on page to eliminate any viewed files that dont have certain elements in their filename.
    # If this filter returns true, count that file as a page and save the file to a column called pageurl. If the filter returns false then the file is not counted as a page.
    # Convert the t column to a date and extract the month ("December"...), day ("01"...), dayoftheweek ("Sun"...), and hour ("00" to "23") into their respective columns.
    # Import the modified and reduced data into the four vectors in the databases you defined above so that the attributes defined there can be applied.

and then run ::

    sh aqlog.sh
        
This executes the essentia commands in ``aqlog.sh`` to load the aq logs into the UDB database. 
    
read.essentia
=============

With the environment setup, we can now use **read.essentia** to execute an essentia script that exports the data from the Essentia database in csv format and then read it into R. 

The **read.essentia** function takes one argument: ``file``, which can contain any arguments that you could typically pass to a bash script. 

The output can be saved into an R dataframe :: 

    **my_dataframe_name** <- read.essentia(file)
    
**read.essentia** requires you to store each essentia query in a bash script. Thus we save the following statement to ``aqlogday.sh``::
    
    # This statement exports the day vector from its database. 
    ess exec "aq_udb -exp aqlogday:aqlogday"
    
to export the data from vector aqlogday in the aqlogday database. Similarly we save::
    
    # This statement exports the hour vector from its database. 
    ess exec "aq_udb -exp aqloghour:aqloghour"

into ``aqloghour.sh``, ::

    # This statement exports the day-of-the-week vector from its database. 
    ess exec "aq_udb -exp aqlogdayoftheweek:aqlogdayoftheweek"

into ``aqlogdayoftheweek.sh``, and ::

    # This statement exports the month vector from its database. 
    ess exec "aq_udb -exp aqlogmonth:aqlogmonth"

into ``aqlogmonth.sh``.

Then we simply have R run::

    system("time bash aqlog.sh")
    # Run the essentia statements written in aqlog.sh. 
    # These statements load the aqlog data into four databases to get the total number of pages and 
    # hits by day, hour, month, and day-of-the-week.
    
    library(RESS)                          
    # Load Essentia's R Integration package.
    
    aqlogday <- read.essentia('aqlogday.sh')
    # Call read.essentia to execute the essentia statement written in aqlogday.sh and save it's output into to an R dataframe.
    
    aqloghour <- read.essentia('aqloghour.sh')
    # Call read.essentia to execute the essentia statement written in aqloghour.sh and save it's output into to an R dataframe.
    
    aqlogmonth <- read.essentia('aqlogmonth.sh')
    # Call read.essentia to execute the essentia statement written in aqlogmonth.sh and save it's output into to an R dataframe.
    
    aqlogdayoftheweek <- read.essentia('aqlogdayoftheweek.sh')
    # Call read.essentia to execute the essentia statement written in aqlogdayoftheweek.sh and save it's output into to an R dataframe.

We are now free to analyze this data using the massive variety of R functions and methods. To get a few quick plots of this data, we can run the R commands written in ``analyzeaqlog.R``::

    source("analyzeaqlog.R", echo=FALSE)  
    # Run the R commands written in analyzeaqlog.R to analyze the data in the dataframes we just created.
    # Turn echo to TRUE to make the output less results-oriented and easier to debug.

This creates plots of the number of pages and hits versus month, day, day of the week, and hour. 
            
Next Steps
==========

This tutorial was meant to continue to familiarize the user with Essentia's R Integration and demonstrated how to use read.essentia
to send data through Essentia's preprocessor and into R.
To see more analysis of complex datasets, please read through our :doc:`rapache` use case.
