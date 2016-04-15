*************************
Example Essentia Syntax 
*************************
.. Example Essentia Commands  .. Essentia Option Usage


Setup UDB databases and schemas
===============================

::

    ess server reset

    ess create database largecount 

    ess create table mytable "s,pkey:country s,+key:user s,+first:start_time s,+last:end_time i,+add:payment"

    ess create vector countrytotals "s,pkey:country i,+add:usercount i,+add:payment"

    ess create variable "i:totalusers"

    ess drop database largecount

    ess drop table mytable

    ess drop vector countrytotals

    ess drop variable

    ess use largecount

    ess server summary

    ess server commit


--------------------------------------------------------------------------------
	
Control the UDB servers
=======================

::

    ess udbd start
    
    ess udbd stop

    ess udbd status

    ess server restart 


--------------------------------------------------------------------------------

Manage data stored locally, on an S3 bucket, or on an Azure container
=====================================================================

::

    ess select local
    ess select s3://asi-public --credentials=/home/ec2-user/asi-public.csv
    ess select blob://my_azure_container --account_name=my_account_name --account_key=my_account_key
    
    ess summary

    ess category add myfavoritedata "*exampledata*gz" --dateregex ".*[:%m:]-[:%y:]-[:%d:].*"

    ess category delete myfavoritedata
    
    ess category change comment myfavoritedata "This category deserves a comment"

    ess ls "*"
    ess ls -r --cat myfavoritedata
    ess ls -r --cat myfavoritedata "*MY_PATTERN*"

--------------------------------------------------------------------------------

Execute commands on master or worker nodes
==========================================

**On the MASTER Node:**

::

    ess stream myfavoritedata "2013-10-01" "2014-09-30" "aq_pp -f,+1,eok - -d %cols -eval i:usercount '0' -udb largecount -imp mytable -imp countrytotals" --debug --master --thread=4
    
    ess exec "aq_udb -exp largecount:mytable" --debug --master

**On the WORKER Nodes:**

::

    ess stream myfavoritedata "2013-10-01" "2014-09-30" "aq_pp -f,+1,eok - -d %cols -eval i:usercount '0' -udb largecount -imp mytable -imp countrytotals" --debug --thread=4
    
    ess exec "aq_udb -exp largecount:mytable" --debug

--------------------------------------------------------------------------------

Manage the Essentia cluster
===========================

::
    
    ess cluster create --number=4 --type=t2.micro

    ess cluster terminate

    ess cluster stop
    
    ess cluster start
    
    ess cluster status
     	 	 	 	 	 	 	 	

--------------------------------------------------------------------------------

SQL style query on raw logs
===========================

::

    ess query 'select * from myfavoritedata:*:* where payment >= 50'
    ess query "select * from purchase:2014-09-01:2014-09-15 where articleID>=46 limit 10"
    
--------------------------------------------------------------------------------

Link Essentia and Redshift clusters
===================================

::

    ess redshift register MyRed MyRed_database essentia DEMOpassword999

    ess redshift stream myfavoritedata '*' '*' "aq_pp -f,+1,eok - -d %cols -eval i:usercount '0'" --debug --master --threads=2 MyRed_table --options TRUNCATECOLUMNS

    ess redshift status

--------------------------------------------------------------------------------

Display version information
===========================
::

    ess -v 
    ess --version
    
--------------------------------------------------------------------------------
	
Send the contents of a file from your datastore to standout output on your screen
=================================================================================

::

    ess cat /path_to_data/exampledata.csv
    
--------------------------------------------------------------------------------
	
Output the filenames contained within an archive file
=====================================================

::

    ess lsa my_archive_file.zip
    
--------------------------------------------------------------------------------
	
Send and receive files from your worker nodes
=============================================

::

    ess file get path_to_file/exampledata.csv
    
    ess file put exampledata.csv --dest path_to_put_file/
    
    ess file mkdir path_to_put_file/