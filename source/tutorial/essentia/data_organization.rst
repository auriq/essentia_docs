*******************
Data Classification
*******************

While the AQ tools provide efficient processing of files, they alone are insufficient for dealing with *many* files.
In large part this is due simply to data accounting. i.e. what files contain what data and where?

Essentia provides a framework for data classification that when configured, can automatically add new files as they
are placed in your data store.  It is particularly handy for log data, where new files are created daily or even hourly.

Description of Tutorial Data
============================

In this and the remaining Essentia tutorials, we will be using a synthetic set of log files collected from a
fictional DIY woodworking web site.  This web site offers detailed construction plans for many items.  Users can
browse part of the article for free, but must pay to obtain the full plan. It is a new service,
and in order to determine how best to price the items, the site randomized the prices for each
set of plans over a 1 month period (prices range from 1 to 6 dollars).

There are two sets of log files.  The first have a filename in the form of ``browse_YYYYMMDD.csv.gz`` and contain the
browsing records of all users who visited the site on a given day.  The files have three columns of data:
:eventDate: is a timestamp of when the user visited a page.
:userID: is a numerical ID matched to a unique user.
:articleID: is a unique identifier for each of the articles offered





**Pick the bucket containing the data you want to analyze and scan it for files:**

Its extremely easy to tell essentia which bucket you want to select data from and to scan that bucket.

* Simply run ``ess datastore select s3://*YourBucket* --aws_access_key=*YourAccessKey* --aws_secret_access_key=*YourSecretAccessKey*`` where the only changes you need to make are to enter your S3 **bucket name** and **access keys**.
* Then scan your bucket by running ``ess datastore scan``
 
**Organize these files into categories of your choosing and have essentia examine them to determine their columns specifications or input them manually.**

We then need to put our data into one or more categories. This is accomplished using

``ess datastore rule add pattern CategoryName DateFormat``

* Pattern is the **linux style glob pattern** that matches the filenames you want to select. Thus you need to enter a linux command line pattern to **match part or all of each filename** you want to be included in your rule. This tends to be accomplished by using **wildcards ( "*" )** at the start and end of whatever phrase or pattern your files share in common. For example if you wanted to select all files with 'FindMe' in them then the pattern you would use is "*FindMe*".

* CategoryName is simply whatever you want your category to be called; however, each category name must be different from those of the other categories or there will be a conflict.

* For DateFormat you need to enter **the pattern of the date in your filenames**, if they have one. Including surrounding characters common to your filenames such as "_" or an extension like ".zip" is recommended to avoid matching other runs of numbers in your filenames. **Year is "Y", Month is "M", and Day is "D"**. You must enter one of these characters for each number in the Date. Thus 2014-11-05 is "YYYY-MM-DD" and 13-10-29 is "YY-MM-DD".    

A few examples of creating rules:

:Filename: 

    "s3://bucket/path/I_am-not_significant-20140322-I-am_significant.csv"

    ``ess datastore rule add "*I-am_significant*" significantfiles "YYYYMMDD"``

    where I called my category 'significantfiles' and told essentia that the files have a date in them in the format 'YYYYMMDD'.

:Filename: 

    "s3://bucket/I_am_significant/I_am-not_significant-131030-I-am-also-significant.zip"

    ``ess datastore rule add "*I_am_significant*I-am-also-significant*" splitsignificance "YYMMDD"``

    where I called my category 'splitsignificance' and told essentia that the files have a date in them in the format 'YYMMDD'.

The next step is to probe the datastore to find information about the categories we've created such as their columns specs, compression, and delimiter. Then we save these values so essentia doesn't have to repeat this step next time it uses this datastore.

``ess datastore probe CategoryName --apply``

Finally we output a summary of the existing categories in our bucket

``ess datastore summary``

---------------------------------------------------------
 
**A Script Showing the General Format of a First Time Scan:**

::

    ess datastore select s3://*YourBucket* --aws_access_key=*YourAccessKey* --aws_secret_access_key=*YourSecretAccessKey*
    # enter your bucket and keys
    ess datatstore scan
    ess datastore rule add pattern1 CategoryName1 DateFormat1
    # enter the pattern and dateformat for the files you want in your category and give your category a name.
    ess datastore rule add pattern2 CategoryName2 DateFormat2
    ... # for as many categories as you need to make
    ess datastore probe CategoryName1 --apply
    ess datastore probe CategoryName2 --apply
    ... # for as many categories as you made
    ess datastore summary
        # this lets you see information about each of your categories including total number of files and total size.
 
---------------------------------------------------------

**How To List Files in Your Datastore or Category:**

This can be accomplished by running

``ess datastore ls pattern``

* where pattern is again the linux style glob pattern. 

* Thus to list all the files in your datastore you just need to enter a **wildcard** character ( **"*"** ) for your pattern. That is, you would run

  ``ess datastore ls "*"``

* If you wanted to list all files that had the words "please", "find", and "me" in them (in that order) then you would enter the command

  ``ess datastore ls "*please*find*me*"``
 
**How To Modify Your Category:**

You can modify your category by running

``ess datastore rule change priority field newValue``

* where field can be any one of **filePattern, categoryName, dateFormat, or priority**. FilePattern is the linux style glob pattern and priority is the order in which your category was made and can be found at the bottom of the printout from ``ess datastore summary``.

* For example, if you wanted to change the priority of rule 1 to 2 then you would run

  ``ess datastore rule change 1 priority 2``

You can also run

``ess datastore category change CategoryName field newValue``
    
* to change any one of the following fields: **compression, delimiter, columnSpec, dateColumn, dateFormat, TZ**. ColumnSpec is the type specification of your columns; i.e. whether they are strings, integers, or another data type; and the column names. DateColumn is the column in your dataset that contains the date you want to order the data by, if it has one. TZ is the timezone that dates and times in your dataset are specified in.

* For example, if you wanted to change the delimiter from csv to tsv for a category called 'changeme' then you would run

  ``ess datastore category change changeme delimiter tsv``

---------------------------------------------------------
 
**How To Completely Start Over:**

Its simple! Just run ``ess datastore purge``  and you will delete the .auriq.db file that stores your file information and you can start anew.
 
**How To Save Your Categories Onto S3:**

This is also simple. After you have created or modified your categories, simply run ``ess datastore push``  and you will upload a copy of your .auriq.db file onto your S3 bucket. You must have write access to your S3 bucket to upload the database file.

This is beneficial since it streamlines essentia's workflow the next time you want to work with your bucket. The next time you use your bucket in a script, essentia will only have to scan your bucket for new or modified files and apply your rules to them to update your categories. Thus you can skip the rule creation step in future runs.