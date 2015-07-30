**********************
Selecting your Data
**********************

Essentia defines a resource that contains data as a 'datastore'.  Current datastore types that are supported by Essentia
include: 

* a **local** disk drive
* an AWS **s3** store (cloud based storage)
* and an Azure **blob** store  

To register the local datastore with Essentia you would enter the command::

  $ ess select local

.. For the version of the files on our public S3 bucket, you would enter::

For an AWS S3 bucket you would enter::

  $ ess select s3://bucket_name --credentials=~/your_credential_file.csv

..  $ ess select s3://asi-public --credentials=~/mycredentials.csv

The ``credentials`` flag can be replaced with ``aws_access_key`` and ``aws_secret_access_key`` to directly enter
credentials, though we recommend the use of credential files if possible.

For an Azure Blob datastore you would enter::

  $ ess select blob://private_container --account_name=associated_account --account_key=associated_key
  
for a private container or ::

  $ ess select blob://public_container --account_name=associated_account
  
for a public container.

Public Data
================

The rest of the tutorials work on your local datastore and on data pulled from a public Github Repository that we provide.  

We also provide a public bucket on AWS S3 and container on Azure Blob that contain data you can play with after you finish our tutorials. 
To select these public datastores, the commands are::

  $ ess select s3://asi-public --credentials=~/mycredentials.csv

for AWS, and ::

  $ ess select blob://asi-public --account_name=asipublic
  
for Azure.