*****************
Essentia Commands
*****************


ess spec
========

Setup UDB databases and schemas

.. csv-table::
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30

    spec reset,,Wipes schema definitions
    spec create database,dbname --ports,"Adds a database entry. Specifies the number of ports to use, or if the number is between 10010 and 10079, the specific ports to use. Comma separated lists of port numbers is accepted"
    spec create table,name colspec,"Adds a table entry to the active database"
    spec create vector,name colspec,"Adds a vector entry to the active database"
    spec create variable,colspec,"Adds a variable entry to the active database (only 1 allowed per spec)"
    spec drop database,name,"Delete a database schema"
    spec drop table,name,"Delete table from schema"
    spec drop vector,name,"Delete vector from schema"
    spec drop variable,,"Delete variable from schema"
    spec use,dbname,"Sets the active database. Subsequent table/vector/variable commands reference it"
    spec summary,,"Simply provide a summary of all known spec files"
    spec commit,,"Upload the schemas to the worker nodes."


--------------------------------------------------------------------------------
	
ess udbd
========

Control the UDB servers

.. csv-table::
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30

    udbd start,[--ports],Start daemons (ports optional..default is all ports specified in the schemas)
    udbd stop,[--ports],Stop daemons
    udbd status,[--ports],Get status
    udbd restart,[--ports],Stop and Start
    udbd ckmem,[--ports],Query the memory usage
    udbd cklog,[--ports],Query the log file for activity


--------------------------------------------------------------------------------

ess datastore
=============

Manage data stored locally or on an S3 bucket.

.. csv-table::
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30

    datastore select,source --credentials | [--aws_access_key --aws_secret_access_key],"Select the datastore to use. Must be of the form : S3://bucket/path/to/data. The index file is created if none exists. If one exists, the index file is pulled to the master node."
    datastore summary,,"Summarize the datastore by outputing all known categories of data, their column spec, and other useful information."
    datastore scan,,"Scan the datastore, updating the index file."
    datastore purge,,"Delete the local copy of the index file."
    datastore push,,"Pushed the index file to the S3 bucket"
    datastore rule add,pattern category dateFormat,"Add a new rule to the database and apply it."
    datastore rule delete,ruleNumber,"Deletes the specified rule number"
    datastore rule change,ruleNumber field newValue,"Changes a rule"
    datastore probe,filename|categoryName --apply,"Scans a file for type, compression, etc. optionally updates the category table with the information."
    datastore category change,categoryName field newValue,"Modified information about a category"
    datastore sql,command,"Applies an arbitrary sql command on the file database"
    datastore ls,pattern,"Returns all files in the bucket that match the unix style glob pattern"
  

--------------------------------------------------------------------------------

ess task
========

Execute commands on master or worker nodes.

.. csv-table::
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30

    task stream,category startdate stopdate command --debug --master --threads --bulk,"Import data from specified category between (and including) specified dates using the specified filter. Default is to execute on worker nodes. Data is streamed, one file at a time, to the given command"
    task exec,command --debug --threads --master,"Execute a command or set of commands on the workers (or master if specified)"

--------------------------------------------------------------------------------

ess instance
============

Manage the Essentia cluster

.. csv-table::
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30
    
    instance local,--ips,Start a local environment using the listed ip addresses as workers
    instance ec2 create,--number --type,create ec2 instances
    instance ec2 existing,reservation#,reuse existing reservations
    instance ec2 remove,--reservation,remove listed reservations from setup
    instance ec2 add,--reservation,add additional reservations to the setup
    instance ec2 terminate,all|reservation,terminate all instances or specific reservations
    instance status,--reservation,status of current reservation or optionally of the given list
    instance find,--instance,find reservations that hold a given instance

--------------------------------------------------------------------------------

ess monitor
===========

Monitor commands to track worker node stats.

.. csv-table::
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30

    monitor tmon,,Task monitor
    monitor smon,start|stop|status|restart| cksize|cktime|purge|now,System monitor    
     	 	 	 	 	 	 	 	

--------------------------------------------------------------------------------

ess query
=========

SQL style query on raw logs.

.. csv-table::
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30

    query 'select ...',,"SQL style query. 'table' is defined as category:date1:date2, where category matches a classified category with the datastore command, and date1/2 is the date range you want to query"  

--------------------------------------------------------------------------------

ess redshift
============

Link Essentia and Redshift clusters

.. csv-table::
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30

    redshift register,clusterName,"Look up your redshift cluster and find its connection information"
    redshift stream,category startdate stopdate command --debug --master --threads --bulk -U userName -d redshiftTableName -p password,"Import data from specified category between (and including) specified dates using the specified filter. Default is to execute on worker nodes. Data is streamed, one file at a time, to the given command and then into your redshift table"
    redshift status,,"Get information about the host and port"        

--------------------------------------------------------------------------------

ess -v| --version
=================
Display version information
