**************************************
Obtain Last, First, and Minimum Values
**************************************

This script imports one dataset with five columns. It then takes the last imported string value of the third column
and first value of the fourth column, sums the integer values of the second column, and takes the minimum value
of the floating-point-type first column for each unique value of the string-type fifth column. This demonstrates
the ease with which Essentia can apply attributes to your data and return the results you want in the time-frame
you need.

A Brief Description of What This Script Does
============================================

``ess spec create vector vector1 s,pkey:country s,+last:first_name s,+first:last_name i,+add:integer_col f,+min:float_col``

* Store a vector in the database fivecoltutorial that stores the last imported first_name value and first last_name value, aggregates the values in the integer column and keeps track of the minimum value of the float column for each unique value in the country column.

``ess datastore select s3://asi-public --aws_access_key=*AccessKey* --aws_secret_access_key=*SecretAccessKey*``

* Tells Essentia to look for data in the publicly available bucket asi-public, which you must enter still enter your AWS credentials to access.

``ess datastore rule add "*fivecoltutorial*" "tutorialdata" "YYMMDD"``

* Create a new rule to take any files with 'fivecoltutorial' in their name and put them in the tutorialdata category.

``ess task stream tutorialdata "*" "*" "aq_pp -f,+1,eok - -d f:float_col i:integer_col s:last_name s:first_name s:country -ddef -udb_imp fivecoltutorial:vector1" --debug``

* Pipe all files in the category tutorialdata to the aq_pp command. 
* In the aq_pp command, tell the preprocessor to take data from stdin, ignoring errors and skipping the first line (the header). 
* Then define the incoming data's columns, and import the data to the vector in the fivecoltutorial database so the attributes listed there can be applied.

``ess task exec "aq_udb -exp fivecoltutorial:vector1 -o /home/ec2-user/corescripts/results/ess2testresults/``
``simplescripts/countrytutorialresults.csv" --debug``

* Export the modified and aggregated data from the database and save the results to a csv file.

::
    
    ess instance local
    ess spec drop database fivecoltutorial
    ess spec create database fivecoltutorial --ports=1 
    
    ess spec create vector vector1 s,pkey:country s,+last:first_name s,+first:last_name i,+add:integer_col f,+min:float_col
    
    ess udbd start
    
    ess datastore select s3://asi-public --aws_access_key=*AccessKey* --aws_secret_access_key=*SecretAccessKey*
    
    ess datastore scan
    
    ess datastore rule add "*fivecoltutorial*" "tutorialdata" "YYMMDD"
    
    ess datastore probe tutorialdata --apply
    ess datastore summary
    
    ess task stream tutorialdata "*" "*" "aq_pp -f,+1,eok - -d f:float_col i:integer_col s:last_name s:first_name s:country -ddef -udb_imp fivecoltutorial:vector1" --debug 
    
    ess task exec "aq_udb -exp fivecoltutorial:vector1 -o /home/ec2-user/corescripts/results/ess2testresults/simplescripts/countrytutorialresults.csv" --debug 
    
    ess udbd stop