*****************
Essentia Commands
*****************



.. csv-table::
    :header: "Command", "Arguments", "Description"
    :widths: 15, 25 ,30

    ess version,,"print out the current version of Essentia and the AQ tools."
    ess select,"| source
    | ``[--region REGION]``
    | ``[--credentials file]``
    | ``[--aws_access_key publickey]``
    | ``[--account_name AzureAccount]``
    | ``[--aws_secret_access_key secretkey]``
    | ``[--account_key AzureKey]``
    | ``[--label name]``","Select a data source"
    ess summary,"| ``[category]``
    | ``[--label name]``
    | ``[--scan]``","Provide a summary of the categories in the current datastore, or a deep summary of a single category"
    ess purge,label,"Delete the reference to the datastore (not the datastore itself)"
    ess ls,"| ``[pattern]`` 
    | ``[--exclude subpattern]``
    | ``[--cat category]`` 
    | ``[--label name]`` 
    | ``[-r]``
    | ``[--dateregex regex_pattern]``
    | ``[--limit number]``","list the contents of the source datastore"
    ess probe,"| category
    | ``[--file filename]``
    | ``[--label name]``
    | ``[--pcmd ProbeCommand]``
    | ``[--size Bytes]``","scans a file to determine its compression, file format, etc."
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
    | ``[--usecache]``","Add a category to the datastore"
    ess category delete,"| ExistingCategory
    | ``[--label name]``","Remove the reference to this category"
    ess category copy,"| ExistingCategory NewCategory
    | ``[--label name]``","Create a copy of an existing category reference"
    ess category change,"| columnspec|dateformat|dateregex|usecache|comment
    | NewSpec|NewFormat|NewRegex|NewCache|NewComment","Modify or override details about a category"
    ess cluster create,"| ``[--type NodeType]`` 
    | ``[--number Number]``","Create worker nodes"
    ess cluster terminate,,"Shutdown all worker nodes"
    ess cluster status,,"Summarizes the state of all workers"
    ess cluster stop,,"Suspend worker nodes (i.e. stop the EC2 instances)"
    ess cluster start,,"Restart suspended worker nodes"
    ess cluster set,"local|cloud","Force essentia into master node only (local) or not."
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
    | ``[--limit number]``","stream data in given range to given command (cat being default)"
    ess exec,"| command 
    | ``[--master]`` 
    | ``[--debug]`` 
    | ``[--s3out label:path]``","execute given command on all worker nodes"
    ess server reset,,"Delete all database definitions"
    ess server restart,,"Clear database contents, but maintain schemas"
    ess server commit,,"Upload database spec files to workers"
    ess server summary,``[--name database]``,"Summarize the databases and objects available for processing"
    ess create,"database|table|vector|variable name spec", "create an object. Name not required for variable"
    ess drop,"database|table|vector|variable name", "delete the object"
    ess use,database, "select the given database for queries"
    ess cat,"| filename 
    | ``[--label name]``", "read file and print to stdout"
    ess lsa,"| filename 
    | ``[--label name]`` 
    | ``[--pattern]``", "List the files within an archive file with optional filtering."
    ess file push,"| files
    | ``[--dest directory]``","Send a local file to worker nodes"
    ess file get,"file|folder","Fetch a file from workers to the master"
    ess file mkdir,"name","create a directory on worker nodes"
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
    ess udbd,"start|stop|restart|status", "direct manipulation of UDB"
    ess udbd,"ckmem|cklog", "check memory or logs of UDB daemons on workers"
