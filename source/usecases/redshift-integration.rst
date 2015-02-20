****************************
Essentia Redshift Integrator
****************************

Categorize, Explore, and Preprocess Your Data for Easy Loading and Analysis in Redshift

Features:
---------------------------------------

**Data Flexibility**

* Essentia can handle any text-based, delimited data.  It doesn't matter if your data is clean or dirty, compressed or uncompressed, zip or gzip.  

**Data Scanner**

* Scan and understand your files, create simple rules to categorize your files, and select exactly the data you want.

**Extract, Transform, and Load**

* Pipe your data into our powerful and easy-to-use ETL tool to cleanse, transform, and merge as you see fit.

A Typical Process
--------------------

**Scan S3**

Using our scanner you can easily select the data you want from your S3 repository. Essentia will then automatically create a manifest file to tell redshift how to connect to essentia and store that manifest file on your S3 bucket. Then you can simply run the code below to preprocess the data as you see fit and stream the modified data directly into redshift.

::

    ess redshift register redshift_cluster_name
    ess redshift stream Standard 2014-12-01 2014-12-10 "aq_pp ...." -U auriq -d redshift_table_name -p secret

**Run ETL**

For example you can ETL your data to cut out any unwanted columns and eliminate any erroneous records and then load the output directly into your resdhift table. If your redshift cluster is called "my_cluster" and your redshift table is called "my_table" then you can easily preprocess the data and load it into your redshift table by running the code below.

::

    ess redshift register my_cluster
    ess redshift stream Standard 2014-12-01 2014-12-10 "aq_pp -f,eok - -d X s:userid X X X X i:siteid X X X X X X X X X X X X X X X X X X X X X" -U auriq -d my_table -p secret

This allows you not only to perform whatever ETL is necessary for your analysis, but ensures you can load both zip and gzip files and that you can select only the necessary subset of your data's columns that are directly needed for your analysis, saving you a great deal of time and money.

Fast and Easy Zip to GZip Conversion
------------------------------------

In addition to directly streaming your zip files into a Redshift table, you can also convert your zip files into gzip files using Essentia by running the following script.

::
      
    ess datastore select s3://*YourBucket* --aws_access_key=*AccessKey* --aws_secret_access_key=*SecretAccessKey*
    ess datastore scan
    ess datastore rule add "*.zip" "zipfiles" "YYMMDD.zip" ## rule to change, select the patterns that match your files.
    ess datastore probe zipfiles --apply
    ess datastore summary
    
    ess task stream zipfiles "*" "*" "gzip -3 -c -" --s3out=s3://*YourBucket*/gz/%path/%file.gz --debug

Then you can load all of the converted gzip files into your redshift table using the following copy command::
    
    Copy tablename
    From 's3://*YourBucket*/gz/'
    credentials 'aws_access_key_id=<access-key-id>;aws_secret_access_key=<secret-access-key>';