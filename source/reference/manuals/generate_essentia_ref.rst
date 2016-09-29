--------------------------------
**ess**
--------------------------------

::

    usage: ess [-h] [-v]
               {select,summary,probe,purge,ls,category,file,cat,lsa,cluster,query,server,create,drop,use,stream,exec,udbd,redshift}
               ...
    
    The Essentia ETL Engine
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
    
    Subcommands:
      {select,summary,probe,purge,ls,category,file,cat,lsa,cluster,query,server,create,drop,use,stream,exec,udbd,redshift}
        select              Choose a datastore
        summary             Summarize datastore
        probe               Probe category
        purge               Delete database
        ls                  File commands
        category            Category commands
        file                File transfer with workers
        cat                 dump file contents to stdout
        lsa                 list contents of an archive
        cluster             manage a cluster of worker nodes
        query               SQL-like query command
        server              Modify server files for udbd
        create              Adds fields to config file
        drop                Removes fields from config file
        use                 Change active database
        stream              Import data
        exec                Execute command
        udbd                udbd commands
        redshift            Link essentia to redshift
    
--------------------------------
**ess select**
--------------------------------

::

    usage: ess select [-h] [--region REGION]
                      [--credentials CREDENTIALS | --aws_access_key AWS_ACCESS_KEY | --account_name ACCOUNT_NAME]
                      [--aws_secret_access_key AWS_SECRET_ACCESS_KEY | --account_key ACCOUNT_KEY]
                      [--label LABEL] [--overwrite]
                      source
    
    Choose a datastore
    
    positional arguments:
      source                Source location
    
    optional arguments:
      -h, --help            show this help message and exit
      --region REGION       Region of datastore
      --credentials CREDENTIALS
                            Credentials file
      --aws_access_key AWS_ACCESS_KEY
                            S3 access key
      --account_name ACCOUNT_NAME
                            Azure account name
      --aws_secret_access_key AWS_SECRET_ACCESS_KEY
                            S3 secret access key
      --account_key ACCOUNT_KEY
                            Azure account key
      --label LABEL         Assign a label to the datastore
      --overwrite           Overwrite credential information
    
--------------------------------
**ess summary**
--------------------------------

::

    usage: ess summary [-h] [--label [LABEL]] [--scan] [--short] [category]
    
    Summarize datastore
    
    positional arguments:
      category         category
    
    optional arguments:
      -h, --help       show this help message and exit
      --label [LABEL]  select a datastore
      --scan           scan and update stats on datastore
      --short          return total file count and size only. used with --scan
    
--------------------------------
**ess probe**
--------------------------------

::

    usage: ess probe [-h] [--file FILE] [--label [LABEL]] [--pcmd [PCMD]]
                     [--size [SIZE]]
                     category
    
    Probe a file within the category
    
    positional arguments:
      category         category
    
    optional arguments:
      -h, --help       show this help message and exit
      --file FILE      probe a specific file
      --label [LABEL]  select a datastore
      --pcmd [PCMD]    command to replace loginf
      --size [SIZE]    number of Bytes of file to fetch
    
--------------------------------
**ess purge**
--------------------------------

::

    usage: ess purge [-h] label
    
    Delete datastore
    
    positional arguments:
      label       datastore to delete
    
    optional arguments:
      -h, --help  show this help message and exit
    
--------------------------------
**ess ls**
--------------------------------

::

    usage: ess ls [-h] [--exclude [EXCLUDE]] [--cat CAT] [--label LABEL] [-r]
                  [--dateregex DATEREGEX] [--limit [LIMIT]] [--short]
                  [pattern]
    
    list files based on an expression
    
    positional arguments:
      pattern               Glob patterns to match for
    
    optional arguments:
      -h, --help            show this help message and exit
      --exclude [EXCLUDE]   Glob patterns to exclude files within pattern
      --cat CAT             Name of category to show files for
      --label LABEL         select a datastore
      -r, --recursive       Ascend through sub paths
      --dateregex DATEREGEX
                            regex style pattern used to get date from filename.
                            Option: [auto|none|custom]
      --limit [LIMIT]       number of file to fetch
      --short               return file names only
    
--------------------------------
**ess category**
--------------------------------

+++++++++++++++++++++++++++++++++
``ess category add``
+++++++++++++++++++++++++++++++++

::

    usage: ess category add [-h] [--exclude [EXCLUDE]] [--dateregex DATEREGEX]
                            [--dateformat DATEFORMAT] [--archive ARCHIVE]
                            [--compression COMPRESSION] [--delimiter DELIMITER]
                            [--columnspec COLUMNSPEC] [--preprocess PREPROCESS]
                            [--alls | --allx] [--overwrite] [--label LABEL]
                            [--comment COMMENT] [--noprobe] [--usecache]
                            name pattern
    
    positional arguments:
      name                  Name of Category to call these files
      pattern               GLOB patterns to match files
    
    optional arguments:
      -h, --help            show this help message and exit
      --exclude [EXCLUDE]   GLOB patterns to exclude files within pattern
      --dateregex DATEREGEX
                            regex style pattern used to get date from filename.
                            Option: [auto|none|custom]
      --dateformat DATEFORMAT
                            Format of the date encoded in the filename. Will be
                            deprecated soon, please use dateregex
      --archive ARCHIVE     GLOB patterns to match members within an archive (e.g.
                            zip,tar,tgz,tar.bz2)
      --compression COMPRESSION
                            Force file to be treated as compressed in given format
      --delimiter DELIMITER
                            Overwrite delimiter
      --columnspec COLUMNSPEC
                            Overwrite columnspec
      --preprocess PREPROCESS
                            preprocess command
      --alls                Force column server to be all strings
      --allx                Force column server to ignore all columns
      --overwrite           Overwrite if category exists
      --label LABEL         select a datastore
      --comment COMMENT     Comment for the category
      --noprobe             Skip file probe. Just index.
      --usecache            Use cached file list if possible.
    
+++++++++++++++++++++++++++++++++
``ess category change``
+++++++++++++++++++++++++++++++++

::

    usage: ess category change [-h]
                               {columnspec,dateformat,dateregex,usecache,comment}
                               ...
    
    Modify parameters of a category
    
    optional arguments:
      -h, --help            show this help message and exit
    
    Category change commands:
      {columnspec,dateformat,dateregex,usecache,comment}
        columnspec          Modify the columnspec
        dateformat          Modify the dateformat. Will be deprecated soon, please
                            use dateregex
        dateregex           Modify the dateregex
        usecache            Modify the usecache
        comment             Modify the comment
    
+++++++++++++++++++++++++++++++++
``ess category delete``
+++++++++++++++++++++++++++++++++

::

    usage: ess category delete [-h] [--label LABEL] category
    
    positional arguments:
      category       category name
    
    optional arguments:
      -h, --help     show this help message and exit
      --label LABEL  select a datastore
    
+++++++++++++++++++++++++++++++++
``ess category copy``
+++++++++++++++++++++++++++++++++

::

    usage: ess category copy [-h] [--label LABEL] src dest
    
    positional arguments:
      src            source name
      dest           copy name
    
    optional arguments:
      -h, --help     show this help message and exit
      --label LABEL  select a datastore
    
--------------------------------
**ess file**
--------------------------------

+++++++++++++++++++++++++++++++++
``ess file push``
+++++++++++++++++++++++++++++++++

::

    usage: ess file push [-h] [--dest DEST] [files [files ...]]
    
    positional arguments:
      files        Files to push
    
    optional arguments:
      -h, --help   show this help message and exit
      --dest DEST  destination directory on worker
    
+++++++++++++++++++++++++++++++++
``ess file get``
+++++++++++++++++++++++++++++++++

::

    usage: ess file get [-h] [name [name ...]]
    
    positional arguments:
      name        name of files/folders to get
    
    optional arguments:
      -h, --help  show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess file mkdir``
+++++++++++++++++++++++++++++++++

::

    usage: ess file mkdir [-h] name
    
    positional arguments:
      name        Directory to create
    
    optional arguments:
      -h, --help  show this help message and exit
    
--------------------------------
**ess cat**
--------------------------------

::

    usage: ess cat [-h] [--label LABEL] [--decompress] filename
    
    positional arguments:
      filename       Filename to dump contents of
    
    optional arguments:
      -h, --help     show this help message and exit
      --label LABEL  Select a datastore
      --decompress   decompress file if supported
    
--------------------------------
**ess lsa**
--------------------------------

::

    usage: ess lsa [-h] [--pattern PATTERN] [--label LABEL] filename
    
    positional arguments:
      filename           Name of the archive file
    
    optional arguments:
      -h, --help         show this help message and exit
      --pattern PATTERN  GLOB patterns to match files
      --label LABEL      Select a datastore
    
--------------------------------
**ess cluster**
--------------------------------

+++++++++++++++++++++++++++++++++
``ess cluster set``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster set [-h] {local,cloud,custom}
    
    positional arguments:
      {local,cloud,custom}
    
    optional arguments:
      -h, --help            show this help message and exit
    
**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_
    
+++++++++++++++++++++++++++++++++
``ess cluster create``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster create [-h] [--number NumberOfWorkers] [--type TYPE]
                              [--add]
                              [--credentials CREDENTIALS | --aws_access_key AWS_ACCESS_KEY]
                              [--aws_secret_access_key AWS_SECRET_ACCESS_KEY]
    
    optional arguments:
      -h, --help            show this help message and exit
      --number NumberOfWorkers
                            Number of worker nodes
      --type TYPE           Type of worker nodes
      --add                 create additional worker nodes
      --credentials CREDENTIALS
                            Credentials file
      --aws_access_key AWS_ACCESS_KEY
                            EC2 access key
      --aws_secret_access_key AWS_SECRET_ACCESS_KEY
                            EC2 secret access key
    
**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_
    
+++++++++++++++++++++++++++++++++
``ess cluster terminate``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster terminate [-h] [--all] [-y]
    
    optional arguments:
      -h, --help  show this help message and exit
      --all       delete all worker nodes, security group, keys
      -y          confirm to terminate all
    
**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_
    
+++++++++++++++++++++++++++++++++
``ess cluster stop``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster stop [-h]
    
    optional arguments:
      -h, --help  show this help message and exit
    
**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_
    
+++++++++++++++++++++++++++++++++
``ess cluster start``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster start [-h]
    
    optional arguments:
      -h, --help  show this help message and exit
    
**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_
    
+++++++++++++++++++++++++++++++++
``ess cluster status``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster status [-h]
    
    optional arguments:
      -h, --help  show this help message and exit
    
**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_
    
+++++++++++++++++++++++++++++++++
``ess cluster remove``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster remove [-h] reservation [reservation ...]
    
    positional arguments:
      reservation  reservation ids to remove
    
    optional arguments:
      -h, --help   show this help message and exit
    
**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_
    
+++++++++++++++++++++++++++++++++
``ess cluster add``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster add [-h] reservation [reservation ...]
    
    positional arguments:
      reservation  reservation ids to add
    
    optional arguments:
      -h, --help   show this help message and exit
    
**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_
    
+++++++++++++++++++++++++++++++++
``ess cluster reset``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster reset [-h]
    
    optional arguments:
      -h, --help  show this help message and exit
    
**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_
    
--------------------------------
**ess query**
--------------------------------

::

    usage: ess query [-h] [--label LABEL] [--check] command [command ...]
    
    SQL-like command.
    
    positional arguments:
      command        SQL command
    
    optional arguments:
      -h, --help     show this help message and exit
      --label LABEL  Specify the datastore to use
      --check        check SQL syntax only
    
--------------------------------
**ess server**
--------------------------------

+++++++++++++++++++++++++++++++++
``ess server reset``
+++++++++++++++++++++++++++++++++

::

    usage: ess server reset [-h]
    
    Terminate all daemons and delete server files
    
    optional arguments:
      -h, --help  show this help message and exit
    
**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_
    
+++++++++++++++++++++++++++++++++
``ess server restart``
+++++++++++++++++++++++++++++++++

::

    usage: ess server restart [-h]
    
    Flush all memory by stopping and starting daemons
    
    optional arguments:
      -h, --help  show this help message and exit
    
**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_
    
+++++++++++++++++++++++++++++++++
``ess server commit``
+++++++++++++++++++++++++++++++++

::

    usage: ess server commit [-h]
    
    Upload server files to workers
    
    optional arguments:
      -h, --help  show this help message and exit
    
**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_
    
+++++++++++++++++++++++++++++++++
``ess server summary``
+++++++++++++++++++++++++++++++++

::

    usage: ess server summary [-h] [--name [NAME]]
    
    optional arguments:
      -h, --help     show this help message and exit
      --name [NAME]  Select database to show
    
**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_
    
--------------------------------
**ess create**
--------------------------------

+++++++++++++++++++++++++++++++++
``ess create database``
+++++++++++++++++++++++++++++++++

::

    usage: ess create database [-h] [--ports PORTS [PORTS ...]] dbname
    
    positional arguments:
      dbname                Specify database name
    
    optional arguments:
      -h, --help            show this help message and exit
      --ports PORTS [PORTS ...]
                            Number of ports
    
+++++++++++++++++++++++++++++++++
``ess create table``
+++++++++++++++++++++++++++++++++

::

    usage: ess create table [-h] name ...
    
    positional arguments:
      name        Specify table name
      columns     Specify column server
    
    optional arguments:
      -h, --help  show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess create vector``
+++++++++++++++++++++++++++++++++

::

    usage: ess create vector [-h] name ...
    
    positional arguments:
      name        Specify vector name
      columns     Specify column server
    
    optional arguments:
      -h, --help  show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess create variable``
+++++++++++++++++++++++++++++++++

::

    usage: ess create variable [-h] ...
    
    positional arguments:
      columns     Specify column server
    
    optional arguments:
      -h, --help  show this help message and exit
    
--------------------------------
**ess drop**
--------------------------------

+++++++++++++++++++++++++++++++++
``ess drop database``
+++++++++++++++++++++++++++++++++

::

    usage: ess drop database [-h] dbname
    
    positional arguments:
      dbname      Specify database name
    
    optional arguments:
      -h, --help  show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess drop table``
+++++++++++++++++++++++++++++++++

::

    usage: ess drop table [-h] name
    
    positional arguments:
      name        Specify table name
    
    optional arguments:
      -h, --help  show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess drop vector``
+++++++++++++++++++++++++++++++++

::

    usage: ess drop vector [-h] name
    
    positional arguments:
      name        Specify vector name
    
    optional arguments:
      -h, --help  show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess drop variable``
+++++++++++++++++++++++++++++++++

::

    usage: ess drop variable [-h]
    
    optional arguments:
      -h, --help  show this help message and exit
    
--------------------------------
**ess use**
--------------------------------

::

    usage: ess use [-h] dbname
    
    Change active database
    
    positional arguments:
      dbname      Name of database to switch to
    
    optional arguments:
      -h, --help  show this help message and exit
    
--------------------------------
**ess stream**
--------------------------------

::

    usage: ess stream [-h] [--exclude EXCLUDE] [--master] [--debug] [--bulk]
                      [--threads THREADS] [--archive ARCHIVE] [--s3out S3OUT]
                      [--label LABEL] [--progress] [--limit LIMIT] [--quitonerror]
                      category lower upper [command]
    
    Import data
    
    positional arguments:
      category           Which category to use
      lower              start
      upper              stop
      command            Command to stream data to
    
    optional arguments:
      -h, --help         show this help message and exit
      --exclude EXCLUDE  exclude files that match pattern
      --master           where to run
      --debug            debug mode
      --bulk             bulk mode
      --threads THREADS  Number of threads
      --archive ARCHIVE  glob pattern to id file within archive
      --s3out S3OUT      send output to an s3 bucket
      --label LABEL      Assign a label to the datastore
      --progress         Show a progress bar
      --limit LIMIT      Limit # of files streamed
      --quitonerror      Stop stream when error occurs
    
**See Also:** :doc:`../tables/index`
    
--------------------------------
**ess exec**
--------------------------------

::

    usage: ess exec [-h] [--master] [--debug] [--s3out S3OUT] command
    
    Execute arbitrary command
    
    positional arguments:
      command        Filter to use
    
    optional arguments:
      -h, --help     show this help message and exit
      --master       where to run
      --debug        debug mode
      --s3out S3OUT  send output to an s3 bucket
    
**See Also:** :doc:`../tables/index`
    
--------------------------------
**ess udbd**
--------------------------------

+++++++++++++++++++++++++++++++++
``ess udbd start``
+++++++++++++++++++++++++++++++++

    
+++++++++++++++++++++++++++++++++
``ess udbd stop``
+++++++++++++++++++++++++++++++++

    
+++++++++++++++++++++++++++++++++
``ess udbd status``
+++++++++++++++++++++++++++++++++

    
+++++++++++++++++++++++++++++++++
``ess udbd restart``
+++++++++++++++++++++++++++++++++

    
+++++++++++++++++++++++++++++++++
``ess udbd ckmem``
+++++++++++++++++++++++++++++++++

    
+++++++++++++++++++++++++++++++++
``ess udbd cklog``
+++++++++++++++++++++++++++++++++

    
--------------------------------
**ess redshift**
--------------------------------

+++++++++++++++++++++++++++++++++
``ess redshift list``
+++++++++++++++++++++++++++++++++

::

    usage: ess redshift list [-h]
    
    optional arguments:
      -h, --help  show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess redshift register``
+++++++++++++++++++++++++++++++++

::

    usage: ess redshift register [-h] clusterid dbname user password
    
    positional arguments:
      clusterid   Cluster-id
      dbname      Name of database on redshift
      user        Username on redshift
      password    user password on redshift
    
    optional arguments:
      -h, --help  show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess redshift deregister``
+++++++++++++++++++++++++++++++++

::

    usage: ess redshift deregister [-h]
    
    optional arguments:
      -h, --help  show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess redshift sql``
+++++++++++++++++++++++++++++++++

::

    usage: ess redshift sql [-h] [command]
    
    Run a command on the redshift cluster
    
    positional arguments:
      command     Command to stream data to
    
    optional arguments:
      -h, --help  show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess redshift gentable``
+++++++++++++++++++++++++++++++++

::

    usage: ess redshift gentable [-h] [--key KEY] [--label LABEL] table category
    
    Create SQL table based off essentia colspec
    
    positional arguments:
      table          Name of table on redshift to create.
      category       Which category to use
    
    optional arguments:
      -h, --help     show this help message and exit
      --key KEY      Set addtional options on a single column
      --label LABEL  Choose category from labelled datastore
    
+++++++++++++++++++++++++++++++++
``ess redshift stream``
+++++++++++++++++++++++++++++++++

::

    usage: ess redshift stream [-h] [--label LABEL] [--threads THREADS]
                               [--options [OPTIONS [OPTIONS ...]]]
                               category lower upper [command] table
    
    Import data
    
    positional arguments:
      category              Which category to use
      lower                 start
      upper                 stop
      command               Command to stream data to
      table                 Name of table on redshift to dump data.
    
    optional arguments:
      -h, --help            show this help message and exit
      --label LABEL         Choose category from labelled datastore
      --threads THREADS     Number of threads
      --options [OPTIONS [OPTIONS ...]]
                            Reshift specific arguments
    
