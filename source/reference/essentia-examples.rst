*************************
Example Essentia Commands
*************************


ess spec
========

Setup UDB databases and schemas::

    ess spec reset

    ess spec create database largecount --ports=10010-10012
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
    ess udbd start --ports=10011
    
    ess udbd stop
    ess udbd stop --ports=10010

    ess udbd status
    ess udbd status --ports=10010-10012

    ess udbd restart 
    ess udbd restart --ports=10015
    
    ess udbd ckmem
    ess udbd ckmem --ports=10012

    ess udbd cklog 
    ess udbd cklog --ports=10010


--------------------------------------------------------------------------------

ess datastore
=============

Manage data stored locally or on an S3 bucket::

    ess datastore select s3://asi-public --credentials=/home/ec2-user/asi-public.csv
    ess datastore select /home/ec2-user/mydatafolder
    
    ess datastore summary

    ess datastore scan

    ess datastore purge

    ess datastore push

    ess datastore rule add "*exampledata*gz" myfavoritedata "MM-YY-DD"

    ess datastore rule delete 3

    ess datastore rule change 3 pattern "*newerisbetter*zip"

    ess datastore probe myfavoritedata --apply
    
    ess datastore category change myfavoritedata compression gzip

    ess datastore sql "select * from fileindex where categoryName=='myfavoritedata'"

    ess datastore ls "*"
  

--------------------------------------------------------------------------------

ess task
========

Execute commands on master or worker nodes::

    ess task stream myfavoritedata "2013-10-01" "2014-09-30" "aq_pp -f,+1,eok - -d %cols -evlc i:usercount '0' -udb largecount -imp mytable -imp countrytotals" --debug --master --thread=4
    
    ess task exec "aq_udb -exp largecount:mytable" --debug --master

--------------------------------------------------------------------------------

ess instance
============

Manage the Essentia cluster::
    
    ess instance local
    ess instance local ip1 ip2

    ess instance ec2 create --number=4 --type=t2.micro

    ess instance ec2 existing r-27e30bc8

    ess instance ec2 remove r-27e30bc8

    ess instance ec2 add r-27e30bc8

    ess instance ec2 terminate all
    ess instance ec2 terminate r-27e30bc8 

    ess instance status --reservation=r-27e30bc8

    ess instance find --instance="Ben 2.1.7"
    ess instance find --instance="Ben*"


--------------------------------------------------------------------------------

ess monitor
===========

Monitor commands to track worker node stats::

    ess monitor tmon

    ess monitor smon start
    ess monitor smon status    
     	 	 	 	 	 	 	 	

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

    ess redshift stream myfavoritedata '*' '*' "aq_pp -f,+1,eok - -d %cols -evlc i:usercount '0'" --debug --master --threads=2 -U bwaxer -d redcount -p mysecret

    ess redshift status

--------------------------------------------------------------------------------

ess -v| --version
=================
Display version information::

    ess -v 
    ess --version