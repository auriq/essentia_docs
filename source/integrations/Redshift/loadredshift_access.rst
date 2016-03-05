=======================================
Loading and Querying Apache Access Logs
=======================================

We'll use apache access logs to demonstrate how Essentia loads many complex files directly into a redshift cluster and can then be used to easily query that data using simple sql statements.

Setup Essentia
***************

To load access log data into Redshift via Essentia we need to create a cloud Essentia cluster::

    ess cluster set cloud
    ess cluster create --number 2 --type m3.medium
    
and then select which AWS S3 Bucket our data is located in::

    ess select s3://asi-public --credentials=PATH/TO/CREDENTIAL_FILE.csv
    
Now we need to create a category to tell Essentia which data in our datastore corresponds to the access logs we want to load into Redshift::

    ess category create April2014 "accesslogs/125-access_log-201404*"

Setup Redshift
***************

Now we register and connect to our running Redshift cluster::
 
    ess redshift register redshiftdemo redshiftdemo essentia DEMOpassword999
           
Now we need to create a category with the correct column specification to generate our Redshift SQL Table::

    ess category add redtable "accesslogs/125-access_log-20140406" \
     --preprocess 'aq_pp -f,eok,qui - -d ip:ip sep:" " s:rlog sep:" " s:rusr sep:" [" s:time_s sep:"] \"" s,clf:req_line1 sep:" " s,clf:req_line2 sep:" " \
    s,clf:req_line3 sep:"\" " i:res_status sep:" " i:res_size sep:" \"" s,clf:referrer sep:"\" \"" s,clf:user_agent sep:"\"" -eval i:time "DateToTime(time_s, \"d.b.Y.H.M.S.z\")"' \
    --columnspec "s:day s:hour i:hitcount i:pagecount i:pagebytes ip:ip X X X X X X" --overwrite
      
and then use that category to generate a Redshift SQL Table called ``april2014``::

    echo "---------- Replicating Category redtable as a Redshift Table ----------"
    ess redshift gentable april2014 redtable --key "day = distkey"
    
.. note:: 

   Instead of creating this category and using it to generate an SQL Table we could have simply coded an SQL Table into a PostgreSQL editor connected to our Redshift Cluster

Load Redshift
***************

So far we've created our cloud Essentia cluster, connected to the data we want to load, created an SQL Table to store the data in, and connected to our running Redshift cluster. Now we can load the access log data into that SQL Table using the ``ess redshift stream`` command::

    ess redshift stream April2014 "2014-04-01" "2014-04-30" "aq_pp -f,qui,eok - -d ip:ip sep:' ' X sep:' ' X sep:' [' \
    s:time_s sep:'] \"' X sep:' ' s,clf:accessedfile sep:' ' X sep:'\" ' i:httpstatus sep:' ' i:pagebytes sep:' \"' X \
    sep:'\" \"' X sep:'\"' X -eval i:time 'DateToTime(time_s, \"d.b.Y.H.M.S.z\")' -filt 'httpstatus == 200 || httpstatus == 304' -eval i:hitcount '1' \
    -if -filt '(PatCmp(accessedfile, \"*.html[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*.htm[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*.php[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*.asp[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*/\", \"ncas\") || PatCmp(accessedfile, \"*.php\", \"ncas\"))' -eval i:pagecount '1' -eval s:pageurl 'accessedfile' -else -eval pagecount '0' -endif \
    -eval s:month 'TimeToDate(time,\"%B\")' -eval s:day 'TimeToDate(time,\"%d\")' -eval s:dayoftheweek 'TimeToDate(time,\"%a\")' -eval s:hour 'TimeToDate(time,\"%H\")' \
    -c day hour hitcount pagecount pagebytes ip -notitle" april2014 --options TRUNCATECOLUMNS

Query Redshift
***************

The data has now been loaded into table ``april2014`` on our Redshift cluster. We can now query that data using an sql statement via Essentia::

    echo "---------- Running an SQL Query on the data in the Redshift Table april2014 ----------"    
    ess redshift sql 'select distinct day, hour, sum(hitcount) Hits, sum(pagecount) Pages, sum(pagebytes) Bandwidth, count(distinct ip) IPs from April2014 group by day, hour order by day, hour'


