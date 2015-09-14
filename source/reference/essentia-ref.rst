*****************
Essentia Commands
*****************



.. csv-table::
    :header: "Command", "Arguments", "Description"
    :widths: 15, 10 ,30

    ess version,,"print out the current version of Essentia and the AQ tools."
    ess select,source,"source,Select a data source"
    ess summary,[--category],"Provide a summary of the categories in the current datastore, or a deep summary of a single category"
    ess purge,,"Delete the reference to the datastore (not the datastore itself)"
    ess ls,,"list the contents of the source datastore"
    ess probe,,"scans a file to determine its compression, file format, etc."
    ess category add,,"Add a category to the datastore"
    ess category delete,,"Remove the reference to this category"
    ess category copy,,"Create a copy of an existing category reference"
    ess category change,"columnspec|dateformat|comment","Modify or override details about a category"
    ess cluster create,"[--type][--number]","Create worker nodes"
    ess cluster terminate,,"Shutdown all worker nodes"
    ess cluster status,,"Summarizes the state of all workers"
    ess cluster stop,,"Suspend worker nodes (i.e. stop the EC2 instances)"
    ess cluster start,,"Restart suspended worker nodes"
    ess cluster set,"local|cloud","Force essentia into master node only (local) or not."
    ess query,,"SQL style query on raw logs"
    ess task stream,"category start stop [command]","stream data in given range to given command (cat being default)"
    ess task exec,command,"execute given command on all worker nodes"
    ess server reset,,"Delete all database definitions"
    ess server restart,,"Clear database contents, but maintain schemas"
    ess server commit,,"Upload database spec files to workers"
    ess server summary,,"Summarize the databases and objects available for processing"
    ess create,"database|table|vector|variable name spec", "create an object. Name not required for variable"
    ess drop,"database|table|vector|variable name", "delete the object"
    ess use,database, "select the given database for queries"
    ess cat,"filename [--label]", "read file and print to stdout"
    ess lsa,"filename [--label] [--pattern]", "List the files within an archive file with optional filtering."
    ess file push,,"Send a local file to worker nodes"
    ess file get,,"Fetch a file from workers to the master"
    ess file mkdir,,"create a directory on worker nodes"
    ess redshift register,clusterName,"Look up your redshift cluster and find its connection information"
    ess redshift stream,"category startdate stopdate command --debug --master --threads --bulk -U userName -d redshiftTableName -p password","Import data from specified category between (and including) specified dates using the specified filter. Default is to execute on worker nodes. Data is streamed, one file at a time, to the given command and then into your redshift table"
    ess redshift status,,"Get information about the host and port"
    ess udbd,"start|stop|restart|status", "direct manipulation of UDB"
    ess udbd,"ckmem|cklog", "check memory or logs of UDB daemons on workers"
