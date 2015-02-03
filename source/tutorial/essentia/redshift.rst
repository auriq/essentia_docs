Using our scanner you can easily select the data you want from your S3 repository. Essentia will then automatically
create a manifest file to tell redshift how to connect to essentia and store that manifest file on your S3 bucket.
Then you can simply run the code below to preprocess the data as you see fit and stream the modified data directly
into redshift::
ess redshift register redshift_cluster_name
ess redshift stream Standard 2014-12-01 2014-12-10 “aq_pp ….” -U auriq -d redshift_table_name -p secret



For example you can ETL your data to cut out any unwanted columns and eliminate any erroneous records and then load the
output directly into your resdhift table. If your redshift cluster is called “my_cluster” and your redshift table is
called “my_table” then you can easily preprocess the data and load it into your redshift table by running the code
below::

ess redshift register my_cluster
ess redshift stream Standard 2014-12-01 2014-12-10 \
“aq_pp -f,eok - -d X s:userid X X X X i:siteid X X X X X X X X X X X X X X X X X X X X X" -U auriq -d my_table -p secret

This allows you not only to perform whatever ETL is necessary for your analysis, but ensures you can load both zip and
gzip files and that you can select only the necessary subset of your data’s columns that are directly needed for your
analysis, saving you a great deal of time and money.</p>