***************************
Analyze Apache Web Log Data
***************************

One common type of log file are those that are collected from Apache web servers.  However in many cases the raw log
needs some preprocessing before it can be properly used.  Here we will demonstrate the use of ``logcnv``, another
application in the Essentia toolkit which allows us to perform ETL and analysis of Apache data in a fluid manner.

The script and the data used in this brief demo can be found on the git repository under ``usecases/``.  The script
is designed to find out the most popular 'referrers'.
It uses ``logcnv`` to parse a line from the log and turn it into a CSV record.  This record is then fed into ``aq_pp``
for ETL operations, and then finally fed into the UDB database. We use the UDB to sort and count the number of
records for each referrer.


..  code-block:: sh
    :linenos:
    :emphasize-lines: 3,7,9-15,17-18

    ess spec reset
    ess spec create database apache --ports=1
    ess spec create vector vector1 s,pkey:referrer i,+add:pagecount
    ess udbd restart

    ess datastore select local
    ess datastore category add 125accesslogs "$HOME/*accesslog*125-access_log*" 

    ess task stream 125accesslogs "2014-11-30" "2014-12-07" \
    "logcnv -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' \
    i,tim:time sep:'] \"' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 sep:'\" ' i:res_status sep:' ' \
    i:res_size sep:' \"' s,clf:referrer \
    sep:'\" \"' s,clf:user_agent sep:'\"' X | \
    aq_pp -f,qui,eok - -d X X X X X X X X X s:referrer X \
    -eval i:pagecount \"1\" -ddef -udb_imp apache:vector1"

    ess task exec "aq_udb -exp apache:vector1 -sort pagecount -dec -top 25; \
    aq_udb -cnt apache:vector1"

Line by line description
========================

**Line 3** 

* Store a vector in the database apache that aggregates the values in the pagecount column for each unique referrer. 
* The pagecount column only contains the number '1' so this serves to count the number of times any one referrer was seen in the web logs.

**Line 7**

* Create a new rule to take any files in your home directory with 'accesslog' and '125-access_log' in their name and put them in the 125accesslogs category.

**Line 9** 

* Pipe the files in the category 125accesslogs that were created between November 30th and December 7th, 2014 to the aq_pp command. 
* In the aq_pp command, tell the preprocessor to take data from stdin, ignoring errors and not outputting any error messages. 
* Then define the incoming data's columns, skipping all of the columns except referrer, and create a column called pagecount that always contains the value 1. 
* Then import the data to the vector in the apache database so the attributes listed there can be applied.

**Line 17** 

* Export the aggregated data from the database, sorting by pagecount and limiting to the 25 most common referrers. Also export the total number of unique referrers.


    


