--------------------------------
**ess**
--------------------------------

Synopsis
========

::

    usage: ess [-h] [-v]
               {select,summary,repository,probe,purge,ls,category,file,cat,lsa,cluster,query,server,create,drop,use,stream,exec,udbd,redshift}
               ...
    
Description
===========

    The Essentia ETL Engine
    
Command Summary
==============

::

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
    
    Subcommands:
      {select,summary,repository,probe,purge,ls,category,file,cat,lsa,cluster,query,server,create,drop,use,stream,exec,udbd,redshift}
        select              Choose a datastore
        summary             Summarize datastore
        repository          Summarize repository
        probe               Probe category
        purge               Delete datastore
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
    
See Also
=========

* :manpage:`ess-select(1)`
* :manpage:`ess-summary(1)`
* :manpage:`ess-repository(1)`
* :manpage:`ess-probe(1)`
* :manpage:`ess-purge(1)`
* :manpage:`ess-ls(1)`
* :manpage:`ess-category(1)`
* :manpage:`ess-file(1)`
* :manpage:`ess-cat(1)`
* :manpage:`ess-lsa(1)`
* :manpage:`ess-cluster(1)`
* :manpage:`ess-query(1)`
* :manpage:`ess-server(1)`
* :manpage:`ess-create(1)`
* :manpage:`ess-drop(1)`
* :manpage:`ess-use(1)`
* :manpage:`ess-stream(1)`
* :manpage:`ess-exec(1)`
* :manpage:`ess-udbd(1)`
* :manpage:`ess-redshift(1)`
