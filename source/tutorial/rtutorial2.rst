****************************
R Integration - Access Log Data
****************************

The R Package
=============

In order to use R with Essentia, you must install the RESS package from C-RAN. Open R and then run::

   install.packages("RESS")


This package contains three R functions that can be used to capture the output of Essentia commands into
R.

* **read.essentia** takes an Essentia script and captures the output csv data into R, where you can save the output to a dataframe or stream it directly into additional analysis. The output can only contain the csv formatted data that you want to read into R.
* **essQuery** is used to directly query the database using a single statement. You can call **essQuery** multiple times to run different statements. You can save the output to a dataframe or stream it directly into additional analysis.
* **capture.essentia**, on the other hand, takes a file containing any number of Essentia commands and captures the output of the specified statements into R dataframes. Thus if you plan to run multiple statements that may be somewhat related to each other, you may want to use **capture.essentia**.

Essentia's Environment
======================

All three functions require an Essentia Bash script to be executed that sets up the Essentia environment and optionally loads data into the UDB database. Thus they require you to run ::

    sh **load_script_name**.sh

In this tutorial we just want to setup a simple Essentia environment, one that runs on our local computer and scans our local 
filesystem for the apache access log data data located in the ``casestudies/apache/accesslogs`` directory. 
If you are not already in the ``casestudies/apache/accesslogs`` directory, please switch into it now.
We save the following commands to :download:`my_setup_script.sh <../../scripts/my_setup_script.sh>`::

    ess udbd stop
    ess server reset
    
    ess create database logsapache1 --ports=1
    ess create vector vector1 s,pkey:timeseg i,+add:pagecount i,+add:hitcount i,+add:pagebytes
    # Create a vector to aggregate (count) the number of pages, hits, and bytes seen or used by the user-specified time segment.
    
    ess udbd start
    
    ess select local
    ess category add 125accesslogs "$HOME/*accesslog*125-access_log*"
    
    ess summary
    
    ess stream 125accesslogs $1 ${2} "logcnv -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] \"' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X \
    | aq_pp -emod rt -f,eok - -d ip:ip X X i:time X s:accessedfile X i:httpstatus i:pagebytes X X -filt '$5' -eval i:hitcount '1' \
    -if -filt '(PatCmp(accessedfile, \"$4\", \"ncas\") || PatCmp(accessedfile, \"*.htm[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*.php[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*.asp[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*/\", \"ncas\") || PatCmp(accessedfile, \"*.php\", \"ncas\"))' -eval i:pagecount '1' -eval s:pageurl 'accessedfile' \
    -else -eval pagecount '0' -endif -eval s:timeseg 'TimeToDate(time,\"${3}\")' -ddef -udb_imp logsapache1:vector1" --debug
    
    # Stream your access logs from the startdate and enddate you specify into the following command. Use logcnv to specify the format of the records in the access log and convert them to .csv format.
    # Then pipe the data into our preprocessor (aq_pp) and specify which columns you want to keep. Filter on httpstatus so that you only include the 'good' http status codes that correspond to actual views.
    # Create a column that you can aggregate for each record to keep track of hits and another column to group the data by. Filter on accessedfile to eliminate any viewed files that dont have certain elements in their filename.
    # If this filter returns true, count that file as a page and save the file to a column called pageurl. If the filter returns false then the file is not counted as a page.
    # Convert the time column to a date and extract the desired time segment. Import the modified and reduced data into the vector in the database you defined above so that the attributes defined there can be applied.

and then run ::

    sh my_setup_script.sh 2014-11-30 2014-12-07 %d "*.html[?,#]?*" "httpstatus == 200 || httpstatus == 304"
    
This substitutes four parameters into the script my_setup_script.sh and then executes the essentia commands in my_setup_script.sh to load the access logs into the UDB database. 
    
read.essentia
=============

With the environment setup, we can now use **read.essentia** to execute an essenia script that exports the data from the Essentia database in csv format and then read it into R. 

The **read.essentia** function takes one argument: ``file``, which can contain any arguments that you could typically pass to a bash script. 

The output can be saved into an R dataframe :: 

    **my_dataframe_name** <- read.essentia(file)
    
**read.essentia** requires you to store the essentia query in a bash script. Thus we save the following statement to readquery.sh::

    # This statement exports the time segment vector from its database. 
    ess exec "aq_udb -exp logsapache1:vector1"

and then simply have R run::

    library(RESS)           # load Essentia's R Integration package
    
    mydata <- read.essentia('readquery.sh')          # call read.essentia to execute the essentia statement written in readquery.sh and save their output into R as a dataframe called mydata
    
We are now free to analyze this data using the massive variety of R functions and methods. To get a few quick plots of this data, we run::

    barplot(t(as.matrix(mydata[,2])), names.arg=mydata[,1], col=c("black"), beside=TRUE, main="# of Pages",xlab="Time",axes=TRUE,las=2,ylim=c(0,max(mydata[,2])))
    legend("topright",legend=c("Pages"),fill=c("black"),bty="n")
    barplot(t(as.matrix(mydata[,3])), names.arg=mydata[,1], col=c("blue"), beside=TRUE, main="# of Hits",xlab="Time",axes=TRUE,las=2,ylim=c(0,max(mydata[,3])))
    legend("topright",legend=c("Hits"),fill=c("blue"),bty="n")
    barplot(t(as.matrix(mydata[,4])), names.arg=mydata[,1], col=c("red"), beside=TRUE, main="Bandwidth",xlab="Time",axes=TRUE,las=2,ylim=c(0,max(mydata[,4])),cex.axis=.7,cex.names=.8)
    legend("topright",legend=c("Bandwidth"),fill=c("red"),bty="n")
    
This created plots of the number of pages, hits, and bandwidth versus the day of the week. 

essQuery
========
    
.. With the environment setup, we can now use **essQuery** to export the data from the UDB database and into an R dataframes. 
We could also have used **essQuery** to export the data from the UDB database and into an R dataframes. 

The **essQuery** function takes three arguments: ``essentia``, ``aq``, and ``flags``. 

The output can be saved into an R dataframe :: 

    **my_dataframe_name** <- essQuery(essentia, aq = "", flags = "")

or directly analyzed in R. For demonstration purposes, we'll save the output of the **essQuery** call to a dataframe.

First we must open an R script or the R interactive prompt and type ::

   library(RESS)
   
to tell R to use the installed RESS package. Then we run ::
    
   mydata <- essQuery("ess exec", "aq_udb -exp logsapache1:vector1")

to import the apache files into R and save them as a dataframe called mydata. 

Here ``essentia`` is an ``ess exec`` 
command pulling all of the aggregated and grouped apache access log data from the UDB database.

We can now run::

    barplot(t(as.matrix(mydata[,2])), names.arg=mydata[,1], col=c("black"), beside=TRUE, main="# of Pages",xlab="Time",axes=TRUE,las=2,ylim=c(0,max(mydata[,2])))
    legend("topright",legend=c("Pages"),fill=c("black"),bty="n")
    barplot(t(as.matrix(mydata[,3])), names.arg=mydata[,1], col=c("blue"), beside=TRUE, main="# of Hits",xlab="Time",axes=TRUE,las=2,ylim=c(0,max(mydata[,3])))
    legend("topright",legend=c("Hits"),fill=c("blue"),bty="n")
    barplot(t(as.matrix(mydata[,4])), names.arg=mydata[,1], col=c("red"), beside=TRUE, main="Bandwidth",xlab="Time",axes=TRUE,las=2,ylim=c(0,max(mydata[,4])),cex.axis=.7,cex.names=.8)
    legend("topright",legend=c("Bandwidth"),fill=c("red"),bty="n")
    
in R to create the same plots as before. 

capture.essentia
================

An alternative way to send the data to R is to use **capture.essentia**.

**capture.essentia** requires you to store the essentia queries in a bash script and then store that script's filename as ``file`` in R. Thus we save the following statements to capture_essentia_query.sh::

    ess exec "aq_udb -exp logsapache1:vector1" #Rinclude #R#mydata#R#

and then simply have R run::

    library(RESS)           # load Essentia's R Integration package
    
    capture.essentia("capture_essentia_query.sh")          # call capture.essentia to execute the essentia statement written in capture_essentia_query.sh and save them to the R dataframe mydata
    
    barplot(t(as.matrix(mydata[,2])), names.arg=mydata[,1], col=c("black"), beside=TRUE, main="# of Pages",xlab="Time",axes=TRUE,las=2,ylim=c(0,max(mydata[,2])))
    legend("topright",legend=c("Pages"),fill=c("black"),bty="n")
    barplot(t(as.matrix(mydata[,3])), names.arg=mydata[,1], col=c("blue"), beside=TRUE, main="# of Hits",xlab="Time",axes=TRUE,las=2,ylim=c(0,max(mydata[,3])))
    legend("topright",legend=c("Hits"),fill=c("blue"),bty="n")
    barplot(t(as.matrix(mydata[,4])), names.arg=mydata[,1], col=c("red"), beside=TRUE, main="Bandwidth",xlab="Time",axes=TRUE,las=2,ylim=c(0,max(mydata[,4])),cex.axis=.7,cex.names=.8)
    legend("topright",legend=c("Bandwidth"),fill=c("red"),bty="n")

and we get the same three plots as before.
            
Next Steps
==========

This tutorial was meant to continue to familiarize the user with Essentia's R Integration and demonstrated how to use the
functions inside the RESS package to send data through Essentia's preprocessor and into R.
To see more advanced analysis of much more complex datasets, please read through our :doc:`../usecases/rapache` use case.
