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
    | ``[--cat pattern]`` 
    | ``[--label name]`` 
    | ``[-r]``","list the contents of the source datastore"
    ess probe,"| category
    | ``[--file filename]``
    | ``[--label name]``
    | ``[--pcmd ProbeCommand]``
    | ``[--size Bytes]``","scans a file to determine its compression, file format, etc."
    ess category add,"| name pattern 
    | ``[--dateformat auto|none|custom]`` 
    | ``[--archive pattern]``
    | ``[--compression type|none]``
    | ``[--delimiter delimiter]``
    | ``[--columnspec NewColumnSpec]``
    | ``[--allx]``
    | ``[--alls]``
    | ``[--overwrite]``
    | ``[--label name]``
    | ``[--comment comment]``
    | ``[--noprobe]``","Add a category to the datastore"
    ess category delete,"| ExistingCategory
    ``[--label name]``","Remove the reference to this category"
    ess category copy,"ExistingCategory NewCategory","Create a copy of an existing category reference"
    ess category change,"| columnspec|dateformat|comment
    | NewSpec|NewFormat|NewComment","Modify or override details about a category"
    ess cluster create,"| ``[--type]`` 
    | ``[--number]``","Create worker nodes"
    ess cluster terminate,,"Shutdown all worker nodes"
    ess cluster status,,"Summarizes the state of all workers"
    ess cluster stop,,"Suspend worker nodes (i.e. stop the EC2 instances)"
    ess cluster start,,"Restart suspended worker nodes"
    ess cluster set,"local|cloud","Force essentia into master node only (local) or not."
    ess query,,"SQL style query on raw logs"
    ess stream,"| category start stop command 
    | ``[--exclude pattern]`` 
    | ``[--master]`` 
    | ``[--debug]`` 
    | ``[--bulk]`` 
    | ``[--threads number]`` 
    | ``[--archive pattern]`` 
    | ``[--s3out label:path]`` 
    | ``[--progress]`` 
    | ``[--limit number]``","stream data in given range to given command (cat being default)"
    ess exec,"| command 
    | ``[--master]`` 
    | ``[--debug]`` 
    | ``[--s3out label:path]``","execute given command on all worker nodes"
    ess server reset,,"Delete all database definitions"
    ess server restart,,"Clear database contents, but maintain schemas"
    ess server commit,,"Upload database spec files to workers"
    ess server summary,,"Summarize the databases and objects available for processing"
    ess create,"database|table|vector|variable name spec", "create an object. Name not required for variable"
    ess drop,"database|table|vector|variable name", "delete the object"
    ess use,database, "select the given database for queries"
    ess cat,"| filename 
    | ``[--label name]``", "read file and print to stdout"
    ess lsa,"| filename 
    | ``[--label name]`` 
    | ``[--pattern]``", "List the files within an archive file with optional filtering."
    ess file push,,"Send a local file to worker nodes"
    ess file get,,"Fetch a file from workers to the master"
    ess file mkdir,,"create a directory on worker nodes"
    ess redshift register,clusterName,"Look up your redshift cluster and find its connection information"
    ess redshift stream,"| category startdate stopdate command 
    | ``[--debug]`` 
    | ``[--master]`` 
    | ``[--threads]`` 
    | ``[--bulk]`` 
    | ``[-U userName]`` 
    | ``[-d redshiftTableName]`` 
    | ``[-p password]``","Import data from specified category between (and including) specified dates using the specified filter. Default is to execute on worker nodes. Data is streamed, one file at a time, to the given command and then into your redshift table"
    ess redshift status,,"Get information about the host and port"
    ess udbd,"start|stop|restart|status", "direct manipulation of UDB"
    ess udbd,"ckmem|cklog", "check memory or logs of UDB daemons on workers"
