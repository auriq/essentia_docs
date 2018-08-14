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
    
+++++++++++++++++++++++++++++++++
``ess cluster create``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster create [-h] [--number NumberOfWorkers] [--type TYPE]
                              [--add]
                              [--credentials CREDENTIALS | --aws_access_key AWS_ACCESS_KEY]
                              [--aws_secret_access_key AWS_SECRET_ACCESS_KEY]
                              [--error_return_code]
    
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
      --error_return_code   return error code when some of worker nodes failed
    
+++++++++++++++++++++++++++++++++
``ess cluster terminate``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster terminate [-h] [--all] [-y]
                                 [--credentials CREDENTIALS | --aws_access_key AWS_ACCESS_KEY]
                                 [--aws_secret_access_key AWS_SECRET_ACCESS_KEY]
    
    optional arguments:
      -h, --help            show this help message and exit
      --all                 delete all worker nodes, security group, keys
      -y                    confirm to terminate all
      --credentials CREDENTIALS
                            Credentials file
      --aws_access_key AWS_ACCESS_KEY
                            EC2 access key
      --aws_secret_access_key AWS_SECRET_ACCESS_KEY
                            EC2 secret access key
    
+++++++++++++++++++++++++++++++++
``ess cluster stop``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster stop [-h]
                            [--credentials CREDENTIALS | --aws_access_key AWS_ACCESS_KEY]
                            [--aws_secret_access_key AWS_SECRET_ACCESS_KEY]
    
    optional arguments:
      -h, --help            show this help message and exit
      --credentials CREDENTIALS
                            Credentials file
      --aws_access_key AWS_ACCESS_KEY
                            EC2 access key
      --aws_secret_access_key AWS_SECRET_ACCESS_KEY
                            EC2 secret access key
    
+++++++++++++++++++++++++++++++++
``ess cluster start``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster start [-h]
                             [--credentials CREDENTIALS | --aws_access_key AWS_ACCESS_KEY]
                             [--aws_secret_access_key AWS_SECRET_ACCESS_KEY]
    
    optional arguments:
      -h, --help            show this help message and exit
      --credentials CREDENTIALS
                            Credentials file
      --aws_access_key AWS_ACCESS_KEY
                            EC2 access key
      --aws_secret_access_key AWS_SECRET_ACCESS_KEY
                            EC2 secret access key
    
+++++++++++++++++++++++++++++++++
``ess cluster status``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster status [-h]
    
    optional arguments:
      -h, --help  show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess cluster remove``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster remove [-h] reservation [reservation ...]
    
    positional arguments:
      reservation  reservation ids to remove
    
    optional arguments:
      -h, --help   show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess cluster add``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster add [-h] reservation [reservation ...]
    
    positional arguments:
      reservation  reservation ids to add
    
    optional arguments:
      -h, --help   show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess cluster reset``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster reset [-h]
    
    optional arguments:
      -h, --help  show this help message and exit
    
+++++++++++++++++++++++++++++++++
``ess cluster iplist``
+++++++++++++++++++++++++++++++++

::

    usage: ess cluster iplist [-h] [--private | --public]
    
    optional arguments:
      -h, --help  show this help message and exit
      --private   Private IPs only
      --public    Public IPs only
    
