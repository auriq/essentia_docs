*************************************************************
Necessary Files to Connect to S3 Buckets and Launch Worker Instances
*************************************************************

--------------------------------------------------------------------------------

Create a Credential File
------------------------
In order to connect to an S3 bucket, essentia requires your access keys.

The credential file is a simple 2-line csv file that tells essentia your username, access_key, and secret_access_key.

A good naming convention is ``**Bucket_Name**.csv``, where you replace ``**Bucket_Name**`` with the name of the S3 bucket the keys grant access to.

The credential file has the following form:

::

  User Name,Access Key Id,Secret Access Key
  **User_Name**,**Access_Key**,**Secret_Key**

All you need to do is replace the values in the second line with your username, aws access key, and aws secret access key.

--------------------------------------------------------------------------------

Customizing Your instance.conf File
------------------------------------