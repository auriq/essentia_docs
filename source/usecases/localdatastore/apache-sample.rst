***************************
Analyze Apache Web Log Data
***************************

One common type of log file are those that are collected from Apache web servers.  However in many cases the raw log
needs some preprocessing before it can be properly used.  Here we will demonstrate the use of ``aq_pp``, a powerful
application in the Essentia toolkit that allows us to perform processing and analysis of Apache data in a fluid manner.

The script and the data used in this brief demo can be found on the git repository under ``casestudies/apache``.  The script
is called ``apache.sh`` and is designed to find out the most popular 'referrers'.
It uses ``aq_pp`` to parse each line from the log and turn it into a CSV record.  Then ``aq_pp`` performs
additional Data Processing operations and finally feeds the modified data into the UDB database. We use the UDB to sort and count the number of
records for each referrer.

Primary Lines in this Script
============================

**Line 8** 

* Store a vector in the database apache that aggregates the values in the pagecount column for each unique referrer. 
* The pagecount column only contains the number '1' so this serves to count the number of times any one referrer was seen in the web logs.

**Line 12**

* Create a new rule to take any files in your home directory with 'accesslog' and '125-access_log' in their name and put them in the 125accesslogs category.

**Line 14** 

* Pipe the files in the category 125accesslogs that were created between November 30th and December 7th, 2014 to the aq_pp command. 
* In the aq_pp command, tell the preprocessor to take data from stdin, ignoring errors and not outputting any error messages. 
* Then define the incoming data's columns, skipping all of the columns except referrer, and create a column called pagecount that always contains the value 1. 
* Then import the data to the vector in the apache database so the attributes listed there can be applied.

**Line 21** 

* Export the aggregated data from the database, sorting by pagecount and limiting to the 25 most common referrers. Also export the total number of unique referrers.

.. literalinclude:: ../../EssentiaPublic/casestudies/apache/apache.sh
   :language: bash
   :linenos:
   :emphasize-lines: 8,12,14-19,21-22

..    ess server reset
    ess create database apache --ports=1
    ess create vector vector1 s,pkey:referrer i,+add:pagecount
    ess udbd restart

    ess select local
    ess category add 125accesslogs "$HOME/*accesslog*125-access_log*" 

    ess stream 125accesslogs "2014-11-30" "2014-12-07" \
    "logcnv -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' \
    i,tim:time sep:'] \"' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 sep:'\" ' i:res_status sep:' ' \
    i:res_size sep:' \"' s,clf:referrer \
    sep:'\" \"' s,clf:user_agent sep:'\"' X | \
    aq_pp -f,qui,eok - -d X X X X X X X X X s:referrer X \
    -eval i:pagecount \"1\" -ddef -udb -imp apache:vector1"

    ess exec "aq_udb -exp apache:vector1 -sort pagecount -dec -top 25; \
    aq_udb -cnt apache:vector1"


