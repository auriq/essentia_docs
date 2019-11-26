*****************
Essentia Commands
*****************

-------------------
*Reference Manuals*
-------------------

.. toctree::
   :maxdepth: 1

   generate_essentia_ref
   
------------------------------------
*Working With Categories*
------------------------------------

To learn more about creating and using categories, see :doc:`category-rules`.

-------------------
*Overview*
-------------------

.. csv-table::
    :header: "Command", "Arguments", "Description"
    :widths: 15, 25 ,30

    ess --version,,"Print out the current version of Essentia and the AQ tools."
    ess select,"| source
    | ``[--region REGION]``
    | ``[--credentials=file]``
    | ``[--aws_access_key publickey]``
    | ``[--account_name AzureAccount]``
    | ``[--aws_secret_access_key secretkey]``
    | ``[--account_key AzureKey]``
    | ``[--label name]``
    | ``[--overwrite]``","Select a data source / repository"
    ess repository,,"Summarize currently defined data sources / repositories"
    ess summary,"| ``[category]``
    | ``[pkey|columnspec|schema|delimiter|compression|preprocess]``
    | ``[--label name]``
    | ``[--scan]``
    | ``[--short]``","Provide a summary of the categories in the current datastore, a deep summary of a single category, or a single parameter of a single category"
    ess purge,label,"Delete the reference to the datastore (not the datastore itself)"
    ess ls,"| ``[pattern]`` 
    | ``[--exclude subpattern]``
    | ``[--cat category]`` 
    | ``[--label name]`` 
    | ``[-r]``
    | ``[--dateregex regex_pattern]``
    | ``[--limit number]``
    | ``[--nameonly]``
    | ``[--nosize]``
    | ``[--nodate]``","List the contents of the source datastore"
    ess probe,"| category
    | ``[--file filename]``
    | ``[--label name]``
    | ``[--pcmd ProbeCommand]``
    | ``[--size Bytes]``","Scans a file to determine its compression, file format, etc."
    ess category add,"| name pattern 
    | ``[--exclude subpattern]``
    | ``[--dateregex regex_pattern|none]``
    | ``[--dateformat auto|none|custom]`` 
    | ``[--archive pattern]``
    | ``[--compression type|none]``
    | ``[--delimiter delimiter]``
    | ``[--columnspec NewColumnSpec]``
    | ``[--preprocess command]``
    | ``[--allx]``
    | ``[--alls]``
    | ``[--overwrite]``
    | ``[--label name]``
    | ``[--comment comment]``
    | ``[--noprobe]``
    | ``[--usecache]``
    | ``[--pkey PKEY]``","Add a category to the datastore"
    ess category delete,"| ExistingCategory
    | ``[--label name]``","Remove the reference to this category"
    ess category copy,"| ExistingCategory NewCategory
    | ``[--label name]``
    | ``[--credentials file]``
    | ``[--aws_access_key publickey]``
    | ``[--aws_secret_access_key secretkey]``","Create a copy of an existing category reference"
    ess category change,"| columnspec|dateformat|dateregex|usecache|comment
    | NewSpec|NewFormat|NewRegex|NewCache|NewComment","Modify or override details about a category"
    ess cluster create,"| ``[--type NodeType]`` 
    | ``[--number Number]``
    | ``[--add]``
    | ``[--credentials CREDENTIALS]``
    | ``[--aws_access_key AWS_ACCESS_KEY]``
    | ``[--aws_secret_access_key AWS_SECRET_ACCESS_KEY]``
    | ``[--error_return_code]``","Create worker nodes"
    ess cluster add,"| ReservationIDs","Add worker nodes to cluster by Reservation ID"
    ess cluster remove,"| ReservationIDs","Remove worker nodes from cluster by Reservation ID"
    ess cluster terminate,"| ``[--all]``
    | ``[-y]``
    | ``[--credentials CREDENTIALS]``
    | ``[--aws_access_key AWS_ACCESS_KEY]``
    | ``[--aws_secret_access_key AWS_SECRET_ACCESS_KEY]``","Shutdown all worker nodes, optionally deleting all pem files and security groups with or without confirmation"
    ess cluster status,,"Summarizes the state of all workers and shows their Reservations IDs"
    ess cluster stop,"| ``[--credentials CREDENTIALS]``
    | ``[--aws_access_key AWS_ACCESS_KEY]``
    | ``[--aws_secret_access_key AWS_SECRET_ACCESS_KEY]``","Suspend worker nodes (i.e. stop the EC2 instances)"
    ess cluster start,"| ``[--credentials CREDENTIALS]``
    | ``[--aws_access_key AWS_ACCESS_KEY]``
    | ``[--aws_secret_access_key AWS_SECRET_ACCESS_KEY]``","Restart suspended worker nodes"
    ess cluster set,"local|cloud|custom","Force essentia into master node only (local) or not."
    ess cluster reset,,"Clear and reset cluster configuration"
    ess cluster iplist,"| ``[--private]``
    | ``[--public]``","List the public and private IP's of cluster"
    ess query,"| command
    | ``[--label name]``
    | ``[--check]``","SQL style query on raw logs"
    ess stream,"| category start stop command 
    | ``[--exclude pattern]`` 
    | ``[--master]`` 
    | ``[--debug]`` 
    | ``[--bulk]`` 
    | ``[--threads number]`` 
    | ``[--archive pattern]`` 
    | ``[--s3out label:path]``
    | ``[--label name]`` 
    | ``[--progress]`` 
    | ``[--limit number]``
    | ``[--quitonerror]``","Stream data in given range to given command (cat being default). * can be used as start/stop to indicate any timestamp."
    ess exec,"| command 
    | ``[--master]`` 
    | ``[--debug]`` 
    | ``[--s3out label:path]``","Execute given command on all worker nodes"
    ess server reset,,"Delete all database definitions"
    ess server restart,,"Clear database contents, but maintain schemas"
    ess server commit,,"Upload database spec files to workers"
    ess server summary,``[--name database]``,"Summarize the databases and objects available for processing"
    ess create,"database|table|vector|variable name spec", "Create an object. Name not required for variable"
    ess drop,"database|table|vector|variable name", "Delete the object"
    ess use,database, "Select the given database for queries"
    ess cat,"| filename 
    | ``[--label name]``
    | ``[--decompress]``", "Read file and print to stdout"
    ess lsa,"| filename 
    | ``[--label name]`` 
    | ``[--pattern]``", "List the files within an archive file with optional filtering."
    ess file push,"| files
    | ``[--dest directory]``","Send a local file to worker nodes"
    ess file get,"file|folder","Fetch a file from workers to the master"
    ess file mkdir,"name","Create a directory on worker nodes"
    ess redshift register,"| redshift_cluster_name 
    | redshift_database_name 
    | username password","Look up your redshift cluster and find its connection information"
    ess redshift stream,"| category startdate stopdate command redshift_table_name
    | ``[--options RedshiftOptions]`` 
    | ``[--threads number]``
    | ``[--label name]``","Import data from specified category between (and including) specified dates using the specified filter. Default is to execute on worker nodes. Data is streamed, one file at a time, to the given command and then into your redshift table"
    ess redshift sql,"command","Query data in a redshift database using an SQL command"
    ess redshift gentable,"| category 
    | redshift_table_name 
    | ``--key 'column = distkey'``","Create a table in redshift using the column specification derived from an Essentia category"
    ess redshift list,,"Get information about all Redshift clusters accessible by Essentia"
    ess redshift deregister,,"Unlink redshift cluster from Essentia"
    ess udbd,"start|stop|restart|status", "Direct manipulation of UDB"
    ess udbd,"ckmem|cklog", "Check memory or logs of UDB daemons on workers"

-------------------
*Advanced Options*
-------------------

.. csv-table::
    :header: "Environment Variable", "Default", "Description"
    :widths: 15, 35, 30

    "ESS_CACHE_DIR","| ``GUI and RStudio:`` /var/www/html/mydmp/aws/1/.ess
    | ``Command Line:`` ~/.ess","Directory path where repository settings files will be stored. This is used to manage the local and cloud repositories associated with the instance you are on. The first default is for files created by the Graphical User Interface or RStudio and the second default is for files created via the command line."
    "ESS_WORK_DIR","| ``All Access Methods:`` ./.conf","Directory path where udb settings files will be stored. This is used to manage the UDB databases and ports associated with the instance you are on. The default is always a **.conf** folder in your current directory."
    "ESS_AWS_DIR","| ``GUI and RStudio:`` /var/www/html/mydmp/aws/1/.aws
    | ``Command Line:`` ~/.aws","Directory path where pem files will be stored. This is used to manage the computer clusters associated with the instance you are on. The first default is for files created by the Graphical User Interface or RStudio and the second default is for files created via the command line."
