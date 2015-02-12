*************************************************************
Necessary Files to Connect to S3 Buckets and Launch Worker Instances
*************************************************************

Create a Credential File
------------------------
In order to connect to an S3 bucket or launch worker instances, essentia requires your access keys.

The credential file is a simple 2-line csv file that tells essentia your username, access_key, and secret_access_key.

A good naming convention is ``**Bucket_Name**.csv``, where you replace ``**Bucket_Name**`` with the name of the S3 bucket the keys grant access to.

The credential file has the following form:

::

  User Name,Access Key Id,Secret Access Key
  **User_Name**,**Access_Key**,**Secret_Key**

All you need to do is replace the values in the second line with your username, aws access key, and aws secret access key.

If you're planning on running any of the samples scripts provided in the EssentiaPublic github repository, you need to include this credential file in the same directory as you put the github repo. It should be in the same directory as the folders **aws-ec2/**, **data-for-local-installation/**, and **scripts-for-local-installation/**.

Customizing Your instance.conf File
------------------------------------

Now that you have created your credential file, you need to modify the instance.conf file included with Essentia so that it contains your credential and pem files.

The format of the included instance.conf is::
 
    [EC2]
    aws_credential: credential_file
    use_private_ip: False
    instance_tag: Essentia Worker Node
    instance_type:  m3.medium
    instance_count: 2
    key_name: pem_file
    security_groups: essentia-access
    username: ec2-user

All you need to do to customize this instance.conf is give it the path to and name of your credential file after ``aws_credential:`` and the path and name of your pem file after ``key_name:``.

These paths can be absolute or relative. The pem file entry only needs to be the ``**pem_filename**`` part of ``**pem_filename**.pem``.