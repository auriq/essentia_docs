Essentia Reference
===================

----------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------
Essentia Guidelines
--------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------

How To Approach An Essentia File:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1.         Tell essentia to whether to run on your local machine or on ec2 worker instances.
2.         Pick the bucket containing the data you want to analyze and scan it for files.
3.         **Organize these files into categories of your choosing and have essentia examine them to determine their columns specifications or input them manually**. *This step is only required first time you access your bucket*.
4.         Define a database and what you want to store in it.
5.         Start udbd so data can be stored in the database you just created.
6.         Import data from one of your categories into your database using ``ess task stream``.
7.         Export your modified data from the database and save it to a file.
 
The categorization step ONLY HAS TO BE RUN ONCE.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To start using essentia you need to scan your bucket and categorize your S3 files. This involves steps 2 and 3.

Typically, categories dont change much once you have completed the initial setup so all you have to repeat each time you want to access your data is step 2::

    ess datastore select s3://*YourBucket* --aws_access_key=*YourAccessKey* --aws_secret_access_key=*YourSecretAccessKey*

    ess datastore scan

Thus you can skip step 3 after your first run.

Learn more about how to `Manage Your S3 Bucket <http://vm146.auriq.net/documentation/source/tutorial/essentia/manage-your-s3-bucket.html>`_.

----------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------
Essentia Commands 
----------------------------------------------------------------------------------------

.. .. csv-table:: Essentia Commands
   :file: ..\..\..\_static\essentiacommands.csv
   :encoding: Excel

--------------------------------------------------------------------------------

**ess spec:**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table:: *Define your database schema.*
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

..      ess spec:
        ^^^^^^^^^
        Define your database schema.
        
        ======================= =================== =======================================================================================================================================================================================	
            Command               Arguments           Description
        ----------------------- ------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        spec reset	 	                        Wipes schema definitions
        spec create database	    dbname --ports    	Adds a database entry. Specifies the number of ports to use, or if the number is between 10010 and 10079, the specific ports to use. Comma separated lists of port numbers is accepted
        spec create table	    name colspec    	Adds a table entry to the active database
        spec create vector	    name colspec    	Adds a vector entry to the active database
        spec create variable	    colspec	            Adds a variable entry to the active database (only 1 allowed per spec)
        spec drop database	    name	            Delete a database schema
        spec drop table	            name	            Delete table from schema
        spec drop vector	    name    	    Delete vector from schema
        spec drop variable	             	    Delete variable from schema
        spec use        	    dbname    	    Sets the active database. Subsequent table/vector/variable commands reference it
        spec summary    	     	            Simply provide a summary of all known spec files
        spec commit	 	                        Upload the schemas to the worker nodes.
        ======================= =================== =======================================================================================================================================================================================

--------------------------------------------------------------------------------
	
**ess udbd:**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table:: *Control the udbd across all nodes.*
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30

    udbd start,[--ports],Start daemons (ports optional..default is all ports specified in the schemas)
    udbd stop,[--ports],Stop daemons
    udbd status,[--ports],Get status
    udbd restart,[--ports],Stop and Start
    udbd ckmem,[--ports],Query the memory usage
    udbd cklog,[--ports],Query the log file for activity
 	
..      **ess udbd:**
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        Control the udbd across all nodes.
        
        =============== =============== =============================================================================
        udbd start	[--ports]	Start daemons (ports optional..default is all ports specified in the schemas)
        udbd stop	[--ports]	Stop daemons
        udbd status	[--ports]	Get status
        udbd restart	[--ports]	Stop and Start
        udbd ckmem	[--ports]	Query the memory usage
        udbd cklog	[--ports]	Query the log file for activity
        =============== =============== =============================================================================

--------------------------------------------------------------------------------

**ess datastore:**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table:: *Select the source of the data and maintain the database which stores an index of the files and their categories. These are the commands that make up the Essentia Scanner, allowing you to understand your S3 bucket.*
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
  
..      **ess datastore:**
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        Select the source of the data and maintain the database which stores an index of the files and their categories. These are the commands that make up the Essentia Scanner, allowing you to understand your S3 bucket.
        
        =============================   ==================================================================  ===================================================================================================================================================================================
        datastore select	        source --credentials | [--aws_access_key --aws_secret_access_key]	    Select the datastore to use. Must be of the form : S3://bucket/path/to/data. The index file is created if none exists. If one exists, the index file is pulled to the master node.
        datastore summary	                                 	                                    Summarize the datastore by outputing all known categories of data, their column spec, and other useful information.
        datastore scan	 	                                                                            Scan the datastore, updating the index file.
        datastore purge	 	                                                                            Delete the local copy of the index file.
        datastore push	 	                                                                            Pushed the index file to the S3 bucket
        datastore rule add	        pattern category dateFormat	                                    Add a new rule to the database and apply it.
        datastore rule delete        	ruleNumber	                                                    Deletes the specified rule number
        datastore rule change    	ruleNumber field newValue	                                    Changes a rule
        datastore probe	                filename|categoryName --apply	                                    Scans a file for type, compression, etc. optionally updates the category table with the information.
        datastore category change	categoryName field newValue	                                    Modified information about a category
        datastore sql	                command	                                                            Applies an arbitrary sql command on the file database
        datastore ls	                pattern	                                                            Returns all files in the bucket that match the unix style glob pattern
        =============================   ==================================================================  ===================================================================================================================================================================================

--------------------------------------------------------------------------------

**ess task:**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table:: *Pipe the data to and run the commands, and launch jobs on worker nodes.*
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30

    task stream,category startdate stopdate command --debug --master --threads --bulk,"Import data from specified category between (and including) specified dates using the specified filter. Default is to execute on worker nodes. Data is streamed, one file at a time, to the given command"
    task exec,command --debug --threads --master,"Execute a command or set of commands on the workers (or master if specified)"

..      ess task:
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        Pipe the data to and run the commands, and launch jobs on worker nodes.
        
        =============== ======================================================================  ==========================================================================================================================================================================================================
        task stream	category startdate stopdate command --debug --master --threads --bulk	Import data from specified category between (and including) specified dates using the specified filter. Default is to execute on worker nodes. Data is streamed, one file at a time, to the given command
        task exec	command --debug --threads --master	                                Execute a command or set of commands on the workers (or master if specified)
        =============== ======================================================================  ==========================================================================================================================================================================================================
         	 	
        ess file:
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File transfer between worker and master.
        
        ==============  =============  ===============================
        file push	         	Upload a file to all workers
        file fetch	log|dir|file	Get file from workers
        ==============  =============  ===============================

--------------------------------------------------------------------------------

**ess instance:**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table:: *Core commands to setup the computing environment.*
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30
    
    instance local,--ips,Start a local environment using the listed ip addresses as workers
    instance ec2 create,--num --type,create ec2 instances
    instance ec2 reuse,--reservation,reuse existing reservations
    instance ec2 remove,--reservation,remove listed reservations from setup
    instance ec2 add,--reservation,add additional reservations to the setup
    instance ec2 terminate,all|reservation,terminate all instances or specific reservations
    instance status,--reservation,status of current reservation or optionally of the given list
    instance find,--instance,find reservations that hold a given instance
     	 	 	 	
..      ess instance:
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        Core commands to setup the computing environment.
       	
        ======================= =============== ===================================================================
        instance local	        --ips	        Start a local environment using the listed ip addresses as workers
        instance ec2 create	--num --type	create ec2 instances
        instance ec2 reuse	--reservation	reuse existing reservations
        instance ec2 remove	--reservation	remove listed reservations from setup
        instance ec2 add	--reservation	add additional reservations to the setup
        instance ec2 terminate	all|reservation	terminate all instances or specific reservations
        instance status	        --reservation	status of current reservation or optionally of the given list
        instance find	        --instance	find reservations that hold a given instance
        ======================= =============== ===================================================================

--------------------------------------------------------------------------------

**ess monitor:**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table:: *Essentia monitoring commands.*
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30

    monitor tmon,,Task monitor
    monitor smon,start|stop|status|restart| cksize|cktime|purge|now,System monitor    
     	 	 	 	 	 	 	 	
..      ess monitor:
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        Essentia monitoring commands.
       	
        =============== =================================================== ==================
        monitor tmon	 	                                            Task monitor
        monitor smon	start|stop|status|restart| cksize|cktime|purge|now  System monitor
        =============== =================================================== ==================

--------------------------------------------------------------------------------

**ess query:**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table:: *Directly query files.*
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30

    query 'select ...',,"SQL style query. 'table' is defined as category:date1:date2, where category matches a classified category with the datastore command, and date1/2 is the date range you want to query"  
     	 	
..      ess query:
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Directly query files.
   	
    ==================== ======= =====================================================================================================================================================================================
    query 'select ...'	 	SQL style query. 'table' is defined as category:date1:date2, where category matches a classified category with the datastore command, and date1/2 is the date range you want to query
    ==================== ======= =====================================================================================================================================================================================

--------------------------------------------------------------------------------

**ess redshift:**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table:: *Essentia redshift integration commands.*
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30

    redshift register,clusterName,"Look up your redshift cluster and find its connection information"
    redshift stream,category startdate stopdate command --debug --master --threads --bulk -U userName -d redshiftTableName -p password,"Import data from specified category between (and including) specified dates using the specified filter. Default is to execute on worker nodes. Data is streamed, one file at a time, to the given command and then into your redshift table"
    redshift status,,"Get information about the host and port"        
                        
..      ess redshift:
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        Essentia redshift integration commands.
        
        ==================== ========================================================================================================================   ===========================================================================================================================================================================================================================================
        redshift register	clusterName	                                                                                                        Look up your redshift cluster and find its connection information
        redshift stream	        category startdate stopdate command --debug --master --threads --bulk -U userName -d redshiftTableName -p password	Import data from specified category between (and including) specified dates using the specified filter. Default is to execute on worker nodes. Data is streamed, one file at a time, to the given command and then into your redshift table
        redshift status	 	                                                                                                                        Get information about the host and port
        ==================== ========================================================================================================================   ===========================================================================================================================================================================================================================================

--------------------------------------------------------------------------------

**ess -v| --version**	 	
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table:: *Display Version number*
    :header: "", "", ""
    :widths: 15, 10 ,30
    
    ,,
 
--------------------------------------------------------------------------------
 
----------------------------------------------------------------------------------------
Starting Your Worker Instances
----------------------------------------------------------------------------------------
How To Start Your Worker Instances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. On your master node, run the command ``ess instance ec2 create --number=# --type=NodeType`` where # is the number of worker instances you want to use and NodeType is the ec2 node type you want the instance to be.
2. After you create any database(s) you need you must run ``ess spec commit`` to upload the databases to your worker nodes.
3. If you have already created worker instances that you want to reuse you need to run the command ``ess instance ec2 existing`` instead of the ``ess instance ec2 create --number=# --type=NodeType`` command.

How To Terminate Your Instances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. When you're done using your worker instances you should terminate them using the command ``ess instance ec2 terminate all`` from the Master Node CLI.
2. To Stop the Master Node, press the Stop button from the Instance tab in the Essentia UI.
3. To Terminate the Master Node, press the Power button on the Essentia UI. This will completely wipe the instance and any files you generated on it. If you plan to use your master node again we recommend you simply stop the node.