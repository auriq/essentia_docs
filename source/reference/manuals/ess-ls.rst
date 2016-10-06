--------------------------------
**ess ls**
--------------------------------

::

    usage: ess ls [-h] [--exclude [EXCLUDE]] [--cat CAT] [--label LABEL] [-r]
                  [--dateregex DATEREGEX] [--limit [LIMIT]]
                  [--nameonly | --nosize | --nodate]
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
      --nameonly            return file names only
      --nosize              return file names and dates
      --nodate              return file names and sizes
    