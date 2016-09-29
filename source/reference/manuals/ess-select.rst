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
    