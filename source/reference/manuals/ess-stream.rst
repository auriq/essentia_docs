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
    