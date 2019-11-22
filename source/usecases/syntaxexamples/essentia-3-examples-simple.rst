*************************
Example Essentia Syntax 
*************************
.. Example Essentia Commands  .. Essentia Option Usage


Setup UDB databases and schemas
===============================

::

    # stop udb server, delete existing schema and empty the data.
    ess server reset

    # create a database called largecount
    ess create database largecount 

    # next three lines create table, vector and variable with given name and column spec within largecount database
    ess create table mytable "s,pkey:country s,+key:user s,+first:start_time s,+last:end_time i,+add:payment"

    ess create vector countrytotals "s,pkey:country i,+add:usercount i,+add:payment"

    ess create variable "i:totalusers"

    # ess drop command delete the given object 
    ess drop database largecount
    ess drop table mytable
    ess drop vector countrytotals
    ess drop variable

    # select largecount database for queries
    ess use largecount

    # summarize the database and objects available
    ess server summary

    # upload database spec files to worker nodes
    ess server commit


--------------------------------------------------------------------------------
	
Control the UDB servers
=======================

::

    # commands below controls udb server in cluster environment
    ess udbd start
    
    ess udbd stop

    ess udbd status

    ess server restart 


--------------------------------------------------------------------------------

Manage data stored locally, on an S3 bucket, or on an Azure container
=====================================================================

::
    
    # from the top, select local machine, s3 bucket, or azure blob container as datastore
    ess select local
    ess select s3://asi-public --credentials=/home/ec2-user/asi-public.csv
    ess select blob://my_azure_container --account_name=my_account_name --account_key=my_account_key
    
    # print out summary of current datastore
    ess summary

    # add category called myfarotiedata
    ess category add myfavoritedata "*exampledata*gz" --dateregex ".*[:%m:]-[:%y:]-[:%d:].*"

    # delete category
    ess category delete myfavoritedata
    
    # changes the comment of the category. 
    ess category change comment myfavoritedata "This category deserves a comment"

    ess ls "*" 

    # displays the files included in the category
    ess ls -r --cat myfavoritedata 

    # display the file in the catgegorythat matches the given pattern
    ess ls -r --cat myfavoritedata "*MY_PATTERN*" 

--------------------------------------------------------------------------------

Execute commands on master or worker nodes
==========================================

**On the MASTER Node:**

::

    # stream myfarotiedata, do some processing with aq_pp, then import to udb, on master node
    ess stream myfavoritedata "2013-10-01" "2014-09-30" "aq_pp -f,+1,eok - -d %cols -eval i:usercount '0' -udb largecount -imp mytable -imp countrytotals" --debug --master --thread=4
    
    ess exec "aq_udb -exp largecount:mytable" --debug --master

**On the WORKER Nodes:**

::

    # same as above, but notice the commands are without "--master" option.
    ess stream myfavoritedata "2013-10-01" "2014-09-30" "aq_pp -f,+1,eok - -d %cols -eval i:usercount '0' -udb largecount -imp mytable -imp countrytotals" --debug --thread=4
    
    ess exec "aq_udb -exp largecount:mytable" --debug

--------------------------------------------------------------------------------

Manage the Essentia cluster
===========================

::
    
    # create cluster wtih 4 worker nodes of type t2.micro instance
    ess cluster create --number=4 --type=t2.micro

    ess cluster terminate # shut down all worker nodes
    ess cluster stop # suspend worker nodes (stop ec2 instance)
    
    # restart suspended worker nodes
    ess cluster start
    
    # summarize the state of all workers and shows thier reservation IDs
    ess cluster status
     	 	 	 	 	 	 	 	

--------------------------------------------------------------------------------

SQL style query on raw logs
===========================

::

    # ess query runs given SQL style query
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
        
    # display Essentia and aq_tools' version
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
