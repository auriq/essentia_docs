Zip To Gzip Conversion
======================
Redshift and other common analytics tools will only load data from compressed files if they have gzip compressed. Thus it requires an extra step in the process to convert existing S3 zip files to gzip files that Redshift can read.

This tutorial provides a script to convert all zip files on your S3 bucket into gzip files using essentia's versatile capabilities. It will also give you examples to help you adapt the script to select only a subset of your zip files.::

    ess datastore select s3://*YourBucket* --aws_access_key=*AccessKey* --aws_secret_access_key=*SecretAccessKey*
    ess datastore scan
    ess datastore rule add "*.zip" "zipfiles" "YYMMDD.zip"     ## rule to change, select the patterns that match your files.
    ess datastore probe zipfiles --apply
    ess datastore summary
    
    ess task stream zipfiles "*" "*" "gzip -3 -c -" --s3out=s3://*YourBucket*/gz/%path/%file.gz --debug
 
Line 1 :
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Select your bucket and place it after the ess datastore select statement, then input your access keys.

Line 3 : 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Input the pattern to find your zip files and a date pattern if your files have a date in their filename.

    If they dont have a date in their filename then you can leave the third set of quotations blank.

    For example, if you wanted to include all zip files with 112233 in their filename then you should run

        ``ess datastore rule add "*112233*.zip" "zipfiles"``

    If they also had a date in their filename, such as in *"this/is/a/path/filename_112233_20141023.zip"* then to match this file and others like it you would run

        ``ess datastore rule add "*112233*.zip" "zipfiles" "_YYYYMMDD.zip"``

    If necessary you can then select files that match another pattern, say 445566 by adding another line:

        ``ess datastore rule add "*445566*.zip" "zipfiles" "_YYYYMMDD.zip"``

    More examples are included later in this tutorial.

Line 7 :
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    You can then select all of the data in the category zipfiles by using the command in the script above or you can select a subset of those files by limiting the allowed date range.

    This is done by replacing the two "*"  arguments with a start and end time, respectively. If you wanted to select all files between 10-23-2013 and 10-31-2014 you would run the command

        ``ess task stream zipfiles "2014-10-23" "2014-10-31" "gzip -3 -c -" --s3out=s3://*OutputBucket*/gz/%path/%file.gz&nbsp;--debug``
 
Examples of category creation:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AWS Bucket Logs :
------------------------------
## not actually zip files, just as an example.

    *Example File*: 
        
        asi-wikistats/asipubliclogs/2014-10-28-23-20-37-3075C8DDF0A31597.zip
    
    *Format*: 
    
        path/year-month-day-hour-minute-second-code.zip
    
    *File-matching Pattern*: 
    
        "*.zip"
    
    *Date Pattern*: 
    
        "YYYY-MM-DD-"
    
    *Command to Run*: 
    
        ``ess datastore rule add "*.zip" "zipfiles" "YYYY-MM-DD-"``

Standard Logs : 
------------------------------
    *Example Files:*

        asi-mapreduce/data/Standard/201406/Auriq_Standard_Advertiser_213524_Daily_140901.zip

        asi-mapreduce/data/Standard/201406/Auriq_Standard_Advertiser_213524_Daily_141017.zip

        asi-mapreduce/data/Standard/201406/Auriq_Standard_Advertiser_543210_Daily_140901.zip

        asi-mapreduce/data/Standard/201406/Auriq_Standard_Advertiser_543210_Daily_140925.zip

    *Format:*
        
        path/Company_Standard_Advertiser_ID_Daily_YYMMDD.zip
        
    *File-matching Pattern:*
    
        "*.zip"
        
    *Date Pattern:*
        
        "YYMMDD.zip"
        
    *Command to Run:*
        
        ``ess datastore rule add "*.zip" "zipfiles" "YYMMDD.zip"``

    *To select just files with id* **213524**:  
    
        ``ess datastore rule add "*213524*.zip" "zipfiles" "YYMMDD.zip"``

    *To select just files with id* **543210**:  
    
        ``ess datastore rule add "*543210*.zip" "zipfiles" "YYMMDD.zip"``

    *To select all files with either id* **213524** *or* **543210**
    
        ``ess datastore rule add "*213524*.zip" "zipfiles" "YYMMDD.zip"``
        
        ``ess datastore rule add "*543210*.zip" "zipfiles" "YYMMDD.zip"``

General Script:
^^^^^^^^^^^^^^^^^^^^^^

::

    ess datastore select s3://*OutputBucket* --aws_access_key=*AccessKey* --aws_secret_access_key=*SecretAccessKey* 
    # Unnecessary if your output bucket is the bucket your zip files are stored in.
    
    ess datastore select s3://*YourBucket* --aws_access_key=*AccessKey* --aws_secret_access_key=*SecretAccessKey*
    #ess datastore purge
    ess datastore scan
    
    ess datastore rule add "*.zip" "zipfiles" "YYMMDD.zip"     ## rule to change, select the patterns that match your files.
    ess datastore probe zipfiles --apply
    ess datastore summary
    
    ess task stream zipfiles "*" "*" "gzip -3 -c -" --s3out=s3://*OutputBucket*/gz/%path/%file.gz --debug
    
The only change this script makes is the ability to have different input and output buckets. The difference is

Lines 1 and 4 :
------------------------------
    Select your input bucket (where your zip files are) and your output bucket (where you want your gzip files to be) and place them after two ess datastore select statements, then input your access keys.