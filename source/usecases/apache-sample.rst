***************************
Analyze Apache Web Log Data
***************************

This script pipes the apache log data through a log converter to get the logs into a csv format, into the Essentia preprocessor, and then into the udbd database.

The preprocessor allows more efficient loading of data by ignoring the irrelevant columns in the web logs and creates a column to keep track of the number of records.

Attributes are applied in the database and the number of records corresponding to each unique referrer is counted.

Then the 25 referrers that corresponded to the most records in the web log data are output and the total number of unique referrers is displayed.

A Brief Description of What This Script Does
============================================

**Line 5** 

* Store a vector in the database apache that aggregates the values in the pagecount column for each unique referrer. 
* The pagecount column only contains the number '1' so this serves to count the number of times any one referrer was seen in the web logs.

**Line 13** 

* Create a new rule to take any files with '125-access_log' in their name and put them in the 125accesslogs category.

**Line 19** 

* Pipe the files in the category 125accesslogs that were created between November 30th and December 7th, 2014 to the aq_pp command. 
* In the aq_pp command, tell the preprocessor to take data from stdin, ignoring errors and not outputting any error messages. 
* Then define the incoming data's columns, skipping all of the columns except referrer, and create a column called pagecount that always contains the value 1. 
* Then import the data to the vector in the apache database so the attributes listed there can be applied.

**Line 21** 

* Export the aggregated data from the database, sorting by pagecount and limiting to the 25 most common referrers. Also export the total number of unique referrers.

..  code-block:: sh
    :linenos:
    :emphasize-lines: 5,13,19,21

    ess instance local
    ess spec drop database apache
    ess spec create database apache --ports=1
    
    ess spec create vector vector1 s,pkey:referrer i,+add:pagecount
    
    ess udbd start
    
    ess datastore select ../../data
    
    ess datastore scan
    
    ess datastore rule add "*125-access_log*" "125accesslogs" "YYYYMMDD"
    
    ess datastore probe 125accesslogs --apply
    ess datastore category change 125accesslogs compression none
    ess datastore summary
    
    ess task stream 125accesslogs "2014-11-30" "2014-12-07" "logcnv -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] \"' s,clf,hl1:req_line1 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X | aq_pp -f,qui,eok - -d X X X X X X X X X s:referrer X -evlc i:pagecount \"1\" -ddef -udb_imp apache:vector1" --debug
    
    ess task exec "aq_udb -exp apache:vector1 -sort pagecount -dec -top 25; aq_udb -cnt apache:vector1" --debug
    
    ess udbd stop
    
This script provided a very simple analysis of Apache Log Data using Essentia. To run the complete version of our
Apache Log Demo, including more advanced analysis using Essentia and R, please follow the steps in
`Getting Started with the R Integrator <http://www.auriq.net/documentation/source/usecases/r-format-requirements.html>`_.
