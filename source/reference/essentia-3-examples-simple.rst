*************************
Example Essentia Syntax 
*************************
.. Example Essentia Commands  .. Essentia Option Usage


ess spec
========

Setup UDB databases and schemas::

    ess spec reset

    ess spec create database largecount 

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

    ess datastore select local
    ess datastore select s3://asi-public --credentials=/home/ec2-user/asi-public.csv
    ess datastore select blob://my_azure_container --account_name=my_account_name --account_key=my_account_key
    
    ess datastore summary

    ess datastore scan

    ess datastore category add myfavoritedata "*exampledata*gz" --dateformat "*MM-YY-DD*"

    ess datastore category delete myfavoritedata
    
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
    
--------------------------------------------------------------------------------
	
ess cat
========

Send the contents of a file from your datastore to standout output on your screen::

    ess cat path_to_data/exampledata.csv
    
--------------------------------------------------------------------------------
	
ess lsa
========

Output the filenames contained within an archive file::

    ess lsa my_archive_file.zip
    
--------------------------------------------------------------------------------
	
ess file
========

Send and receive files from your worker nodes::

    ess file get path_to_file/exampledata.csv
    
    ess file put exampledata.csv --dest path_to_put_file/
    
    ess file mkdir path_to_put_file/