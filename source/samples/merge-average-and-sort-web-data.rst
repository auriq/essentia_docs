Merge, Average, and Sort Web Data
=================================

This script imports two datasets, uses the rankings dataset to lookup and replace the destination URL with the corresponding page rank, calculates the average page rank and total ad revenue by unique sourceIP, and outputs the results sorted by total ad revenue.

A Brief Description of What This Script Does:
---------------------------------------------

``ess spec create vector vector1 s,pkey:sourceIP f,+add:avgpageRank f,+add:adRevenue f,+add:row``

* Tell essentia that the amp1nodeess2 database will store a vector that adds the page ranks, adds the ad Revenue, and counts the number of rows for each unique value of the sourceIP.

``ess datastore rule add "*pavlo/text/1node/uservisits/part*" uservisits "YYYYMMDD-"``

* Create a new rule to take any files in the folder uservisits and put them in the uservisits category.

``ess datastore rule add "*pavlo/text/1node/rankings/part*" rankings "YYYYMMDD-"``

* Create a new rule to take any files in the folder rankings and put them in the rankings category.

``ess datastore category change uservisits compression none``

``ess datastore category change rankings compression none``

* Tell essentia that the files in these categories are not compressed.

``ess task stream rankings "*" "*" "aq_pp -f,eok - -d s:pageURL s:pageRank X -o,app /home/ec2-user/corescripts/results/ess2testresults/lookuppagerank.csv" --debug --thread=10`` 

* Pipe all files in the category rankings to the aq_pp command, and run this command 10 times (allowing you to stream 10 files simultaneously). 
* In the aq_pp command, tell the preprocessor to take data from stdin, ignoring errors. 
* Then define the incoming data's columns, skipping the third column, and write the data to a lookup csv file on your local machine.

``ess task stream uservisits "*" "*" "aq_pp -f,eok - -d s:sourceIP s:destURL s:visitDate f:adRevenue X X X X X -evlc i:dt 'DateToTime(visitDate,\"Y.m.d\")' -filt '((dt >= 315532860) && (dt <= 788918460))' -sub,req destURL /home/ec2-user/corescripts/results/ess2testresults/lookuppagerank.csv -evlc f:avgpageRank 'ToF(destURL)' -evlc f:row '1' -udb_imp amp1nodeess2:vector1" --debug --thread=5``

* Pipe all files in the uservisits category to the aq_pp command, cutting out the last five coumns of each file. 
* Create a column conatining the Posix time of each user's visit and limit the data to users who visited between two POSIX times. 
* Use the lookup file created in the previous step to replace each destination URL with the corresponding page Rank and create a column that contains the float version of these values. 
* Create a new column called 'row' to keep track of the number of rows per sourceIP and import the data into the vector in the database so the attributes listed there can be applied.

``ess task exec "aq_udb -exp amp1nodeess2:vector1 -pp vector1 -pp_evlc avgpageRank 'avgpageRank / (row)' -c sourceIP avgpageRank adRevenue -o - | rw_csv -f+1 - -d s:sourceIP f:avgpageRank f:adRevenue -sort adRevenue > sortedtable.csv" --debug`` 

* Export the modified and aggregated data from the database and convert the aggregated page rank to an average by dividing by the number of rows per sourceIP, then sort the data by adRevenue using rw_csv and save the results to a file.

::

    ess instance local
    ess udbd stop
    
    ess spec create database amp1nodeess2 --ports=1 
    
    ess spec create vector vector1 s,pkey:sourceIP f,+add:avgpageRank f,+add:adRevenue f,+add:row
    
    ess udbd start
    
    ess datastore select s3://big-data-benchmark --aws_access_key=*AccessKey* --aws_secret_access_key=*SecretAccessKey*
    
    #ess datastore purge
    ess datastore scan
    
    ess datastore rule add "*pavlo/text/1node/uservisits/part*" uservisits "YYYYMMDD-"
    ess datastore rule add "*pavlo/text/1node/rankings/part*" rankings "YYYYMMDD-"
    
    ess datastore category change uservisits compression none
    ess datastore category change rankings compression none
    
    ess datastore summary
    
    ess task stream rankings "*" "*" "aq_pp -f,eok - -d s:pageURL s:pageRank X -o,app /home/ec2-user/corescripts/results/ess2testresults/lookuppagerank.csv" --debug --thread=10
    
    ess task stream uservisits "*" "*" "aq_pp -f,eok - -d s:sourceIP s:destURL s:visitDate f:adRevenue X X X X X -evlc i:dt 'DateToTime(visitDate,\"Y.m.d\")' -filt '((dt >= 315532860) && (dt <= 788918460))' -sub,req destURL /home/ec2-user/corescripts/results/ess2testresults/lookuppagerank.csv -evlc f:avgpageRank 'ToF(destURL)' -evlc f:row '1' -udb_imp amp1nodeess2:vector1" --debug --thread=5
    
    ess task exec "aq_udb -exp amp1nodeess2:vector1 -pp vector1 -pp_evlc avgpageRank 'avgpageRank / (row)' -c sourceIP avgpageRank adRevenue -o - | rw_csv -f+1 - -d s:sourceIP f:avgpageRank f:adRevenue -sort adRevenue > sortedtable.csv" --debug
    
    ess udbd stop