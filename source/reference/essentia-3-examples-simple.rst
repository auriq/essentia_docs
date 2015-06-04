*************************
Example Essentia Commands
*************************
.. Essentia Syntax / Essentia Option Usage


ess spec
========

Setup UDB databases and schemas::

    ess spec reset

    ess spec create database largecount --ports=3

    ess spec create table mytable "s,pkey:country s,+key:user s,+first:time s,+last:time i,+add:payment"

    ess spec create vector countrytotals "s,pkey:country i,+add:usercount i,+add:payment"

    ess spec create variable "i:totalusers"

    ess spec drop database largecount

    ess spec drop table mytable

    ess spec drop vector countrytotals

    ess spec drop variable

    ess spec use largecount

    ess spec summary

    ess spec commit


--------------------------------------------------------------------------------
	
ess udbd
========

Control the UDB servers::

    ess udbd start
    
    ess udbd stop

    ess udbd status

    ess udbd restart 


--------------------------------------------------------------------------------

ess datastore
=============

Manage data stored locally, on an S3 bucket, or on an Azure container::

    ess datastore select s3://asi-public --credentials=/home/ec2-user/asi-public.csv
    ess datastore select /home/ec2-user/mydatafolder
    
    ess datastore summary

    ess datastore scan

..    ess datastore purge
..
..    ess datastore push
..
    ess datastore category add myfavoritedata "*exampledata*gz" --dateformat "*MM-YY-DD*"

    ess datastore category delete myfavoritedata

    ess datastore category change 3 pattern "*newerisbetter*zip"

    ess datastore probe myfavoritedata --apply
    
    ess datastore category change comment myfavoritedata "This category deserves a comment"

    ess datastore ls "*"
  
    ess datastore ls -r --cat myfavoritedata "*"

--------------------------------------------------------------------------------

ess task
========

Execute commands on master or worker nodes::

    ess task stream myfavoritedata "2013-10-01" "2014-09-30" "aq_pp -f,+1,eok - -d %cols -eval i:usercount '0' -udb largecount -imp mytable -imp countrytotals" --debug --master --thread=4
    
    ess task exec "aq_udb -exp largecount:mytable" --debug --master

--------------------------------------------------------------------------------

ess instance
============

Manage the Essentia cluster::
    
    ess cluster create --number=4 --type=t2.micro

    ess cluster terminate

    ess cluster status
     	 	 	 	 	 	 	 	

--------------------------------------------------------------------------------

ess query
=========

SQL style query on raw logs::

    ess query 'select * from myfavoritedata:*:* where payment >= 50'
    ess query "select * from purchase:2014-09-01:2014-09-15 where articleID>=46 limit 10"
    
--------------------------------------------------------------------------------

ess redshift
============

Link Essentia and Redshift clusters::

    ess redshift register MyRed

    ess redshift stream myfavoritedata '*' '*' "aq_pp -f,+1,eok - -d %cols -eval i:usercount '0'" --debug --master --threads=2 -U bwaxer -d redcount -p mysecret

    ess redshift status

--------------------------------------------------------------------------------

ess -v| --version
=================
Display version information::

    ess -v 
    ess --version