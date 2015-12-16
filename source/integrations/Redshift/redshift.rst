*******************************************
Data Integration: AWS Redshift and Essentia
*******************************************

AWS provides a scalable SQL service called 'redshift'.  It is commonly used in data warehousing,
and can scale to store PB of data. But going from raw data into a properly formatted table suitable for Redshift (or
any other database for that matter) is often problematic.

We added a module to Essentia to address issues that include:

* File format: Redshift can read files that are compressed under gz, bz2, and lzo (or not compressed at all).  A lot
  of our clients had zip files which they wanted to load into Redshift.

* Data quality: Raw log data often requires filtering and transformation to produce the data that is actually desired.

Requirements
============
In order to link Essentia and Redshift, the following is needed:

* A running Redshift cluster.
* A running Essentia cluster.
* The Essentia security group needs to allow SSH (port 22) access from your Redshift cluster.
* The Redshift security group needs to allow port 5439 access from your Essentia cluster.
* Essentia cluster needs to be in the same zone as the Redshift cluster.
* Essentia cluster needs to be in the same VPC as the Redshift cluster, and cannot be in EC2-Classic.
* Redshift database username and password required.
* User needs to have write access to Redshift database.
* Essentia cluster needs an IAM role that allows it to spin up additional EC2 instances and that allows it access to Redshift (see IAM Role below).

IAM Role
========

Here is an example of a policy that allows access to EC2 Instances as well as Redshift::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:*"
                ],
                "Resource": [
                    "*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "redshift:*"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }

To learn how to create an IAM role, follow the instructions in :doc:`../install/aws/iam-role`.

Moving data
===========

Transferring data is very straightforward.  First register the Redshift cluster with Essentia, then optionally generate a table using Essentia, 
and then provide the ETL operation which is in a format very similar to the 'stream' command as described in the
:doc:`ETL tutorial <../tutorial/etl>` to load the data into the table::

  $ ess redshift register redshift_cluster_name redshift_database_name username password
  $ ess redshift gentable table_name category_name --key "column_name = distkey"
  $ ess redshift stream category_name start_date end_date "command" table_name --options TRUNCATECOLUMNS
  
Here, 'command' is typically ``aq_pp``, but it can also be any other program that accepts text data from the stdin
and outputs the results to stdout.

Querying Data
=========================

Once you have data loaded into Redshift you can query that data with Essentia using sql statements. You simply run::

   $ ess redshift sql 'SQL_COMMAND'

Example: Access Logs
====================

::

    echo "---------- Creating Essentia Cluster ----------"
    ess cluster set cloud
    ess cluster create --number 2 --type m3.medium
    
    echo "---------- Selecting AWS Bucket ----------"
    ess select s3://asi-public --credentials=PATH/TO/CREDENTIAL_FILE.csv
    
    echo "---------- Creating Category redtable ----------"
    ess category add redtable "accesslogs/125-access_log-20140406" \
    --preprocess 'logcnv -f,eok,qui - -d ip:ip sep:" " s:rlog sep:" " s:rusr sep:" [" i,tim:time sep:"] \"" s,clf:req_line1 sep:" " s,clf:req_line2 sep:" " s,clf:req_line3 sep:"\" " i:res_status sep:" " i:res_size sep:" \"" s,clf:referrer sep:"\" \"" s,clf:user_agent sep:"\""' \
    --columnspec "s:day s:hour i:hitcount i:pagecount i:pagebytes ip:ip X X X X X" --overwrite
    
    echo "---------- Registering Redshift Cluster ----------"
    ess redshift register redshiftdemo redshiftdemo essentia DEMOpassword999
    
    echo "---------- Ensuring Table is Empty ----------"
    ess redshift sql 'drop table april2014 cascade'
    
    echo "---------- Replicating Category redtable as a Redshift Table ----------"
    ess redshift gentable april2014 redtable --key "day = distkey"
    
    echo "---------- Loading AWS S3 Data into Redshift ----------"
    ess redshift stream April2014 "2014-04-01" "2014-04-30" "logcnv -f,eok,qui - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] \"' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' -notitle | aq_pp -emod rt -f,eok - -d ip:ip X X i:time X s:accessedfile X i:httpstatus i:pagebytes X X -filt 'httpstatus == 200 || httpstatus == 304' -eval i:hitcount '1' -if -filt '(PatCmp(accessedfile, \"*.html[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*.htm[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*.php[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*.asp[?,#]?*\", \"ncas\") || PatCmp(accessedfile, \"*/\", \"ncas\") || PatCmp(accessedfile, \"*.php\", \"ncas\"))' -eval i:pagecount '1' -eval s:pageurl 'accessedfile' -else -eval pagecount '0' -endif -eval s:month 'TimeToDate(time,\"%B\")' -eval s:day 'TimeToDate(time,\"%d\")' -eval s:dayoftheweek 'TimeToDate(time,\"%a\")' -eval s:hour 'TimeToDate(time,\"%H\")' \
    -c day hour hitcount pagecount pagebytes ip -notitle" april2014 --options TRUNCATECOLUMNS

    echo "---------- Running an SQL Query on the data in the Redshift Table april2014 ----------"    
    ess redshift sql 'select distinct day, hour, sum(hitcount) Hits, sum(pagecount) Pages, sum(pagebytes) Bandwidth, count(distinct ip) IPs from April2014 group by day, hour order by day, hour'


