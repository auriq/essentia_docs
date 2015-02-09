Calculate Sum and Maximum
====================================

This script imports the first three columns of a five column dataset. It then adds the floating point value in the first column and takes the maximum integer value in the second column for each unique value of the string-type third column. Selecting only the necessary subset of columns is good practice for larger datasets, as it allows you to fit more of the relevant data into memory and thus increases the efficiency of your analysis.

Primary Lines in this Script:
---------------------------------------------

``ess spec create vector vector1 s,pkey:string_col i,+max:integer_col f,+add:float_col``

* Store a vector in the database fivecoltutorial that keeps track of the maximum value of the integer column and aggregates the values in the float column for each unique value of the string column.

``ess datastore select s3://asi-public --aws_access_key=*AccessKey* --aws_secret_access_key=*SecretAccessKey*``

* Tells Essentia to look for data in the publicly available bucket asi-public, which you must enter still enter your AWS credentials to access.

``ess datastore rule add "*fivecoltutorial*" "tutorialdata" "YYMMDD"``

* Create a new rule to take any files with 'fivecoltutorial' in their name and put them in the tutorialdata category.

``ess task stream tutorialdata "*" "*" "aq_pp -f,+1,eok - -d f:float_col i:integer_col s:string_col X X -ddef -udb_imp fivecoltutorial:vector1" --debug``

* Pipe all files in the category tutorialdata to the aq_pp command. 
* In the aq_pp command, tell the preprocessor to take data from stdin, ignoring errors and skipping the first line (the header). 
* Then define the incoming data's columns, skipping the fourth and fifth columns, and import the data to the vector in the fivecoltutorial database so the attributes listed there can be applied.

``ess task exec "aq_udb -exp fivecoltutorial:vector1 -o /home/ec2-user/corescripts/results/ess2testresults/``
``simplescripts/fivecoltutorialresults.csv" --debug``

* Export the modified and aggregated data from the database and save the results to a csv file.

::
    
    ess instance local
    ess spec drop database fivecoltutorial
    ess spec create database fivecoltutorial --ports=1 
    
    ess spec create vector vector1 s,pkey:string_col i,+max:integer_col f,+add:float_col
    
    ess udbd start
    
    ess datastore select s3://asi-public --aws_access_key=*AccessKey* --aws_secret_access_key=*SecretAccessKey*
    
    ess datastore scan
    
    ess datastore rule add "*fivecoltutorial*" "tutorialdata" "YYMMDD"
    
    ess datastore probe tutorialdata --apply
    ess datastore summary
    
    ess task stream tutorialdata "*" "*" "aq_pp -f,+1,eok - -d f:float_col i:integer_col s:string_col X X -ddef -udb_imp fivecoltutorial:vector1" --debug 
    
    ess task exec "aq_udb -exp fivecoltutorial:vector1 -o /home/ec2-user/corescripts/results/ess2testresults/simplescripts/fivecoltutorialresults.csv" --debug 
    
    ess udbd stop