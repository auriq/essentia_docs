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
    
