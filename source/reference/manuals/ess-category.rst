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
                            [--pkey PKEY]
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
      --pkey PKEY           pkey column name
    
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
    
