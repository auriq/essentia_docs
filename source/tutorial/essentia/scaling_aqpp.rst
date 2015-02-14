****************
Scaling AQ Tools
****************

An incredibly important feature of Essentia is the ability to spool up as many worker nodes as you want to increase your data processing speed. This speed increases almost linearly with the number of nodes used, allowing your company to analyze more data in less time.

This tutorial is meant to build off of `<http://www.auriq.net/documentation/source/tutorial/essentia/scaling_udb.html>`_ and demonstrate how to adapt that tutorial's script to use multiple ec2 worker instances. To understand the processing occurring in this script you should go through that tutorial first. This tutorial will focus on the changes required to run on worker instances instead of one master instance and what this means for essentia.

Step 1 : 
--------
    Follow the `<http://www.auriq.net/documentation/source/tutorial/essentia/ess_on_aws.html>`_ tutorial to connect your access keys and repository to the essentia platform and connect to a master instance.

Step 2 : 
--------
    Follow `<http://www.auriq.net/documentation/source/tutorial/essentia/scaling_udb.html>`_ to understand the processing in this script.

Step 3 :
--------
    Change **``ess instance local``** to **``ess instance ec2 create 10 t2.micro``** in the beginning of the script to tell essentia to start 10 t2.micro worker instances and tell essentia to communicate with these instances so your essentia commands can parallelize.

Step 4 : 
--------
    Add the command  **``ess spec commit``** to send your databases to your worker nodes so they know what to do with the imported data.

Step 5 :
--------
    Add the option  **``--master``** to the end of the last line of the script to tell essentia to run that command on the master node so that you it can aggregate all of the data from the worker nodes and save it to one csv file on the master instance.

The Full Script:
----------------

::

    ess instance ec2 create --number=10 --type=t2.micro       
    # Starts 10 t2.micro worker instances so your essentia commands can parallelize.Tells essentia to run on and communicate with your worker instances.
    ## ess instance ec2 existing
    ## use the above command instead of ess instance ec2 create if you already have your worker node(s) running and you just want to reuse them.
    ess udbd stop                             
    # Checks that the nothing in stored in memory from previous essentia runs.
    
    ess datastore select s3://asi-public --aws_access_key=*AccessKey* --aws_secret_access_key=*SecretAccessKey*
    #ess datastore purge
    ess datastore scan
    
    ess datastore rule add "*MOCK_DATA*" "mockdata"
    ess datastore probe mockdata --apply
    ess datastore summary
    
    ess spec drop database etl-ess2working
    ess spec create database etl-ess2working --ports=1
    ess spec create vector vector1 s,pkey:my_string_column_to_group_by f,+add:float_column_to_import f,+last:rowcount f,+last:rowcount2
    
    ess spec commit           
    # Send your databases to the worker nodes so they know what to do with the imported data.
    ess udbd start            
    # Starts communication with worker nodes. Starts the database so you can import data into it.
    
    ess task stream mockdata "*" "*" "aq_pp -f,+1,eok - -d s:column_to_import -evlc f:float_column_to_import '(ToF(column_to_import))' -filt '(float_column_to_import >= 1 && float_column_to_import <= 8)' -evlc s:my_string_column_to_group_by 'ToS(1)' -evlc f:rowcount '\$RowNum' -ddef -udb_imp etl-ess2working:vector1" --debug
    # This command is now replicated on each of the 10 worker nodes and each node processes a portion of the files. Each of the 10 nodes also stores a portion of the unique values of the hash column that was specified in the vector in the database etl-ess2working and the corresponding data. Thus the query is parallelized efficiently across the memory of the 10 nodes.
    
    ess task exec "aq_udb -exp etl-ess2working:vector1 -pp vector1 -pp_evlc rowcount2 'rowcount' -pp_evlc rowcount 'float_column_to_import / rowcount' > /home/ec2-user/corescripts/results/ess2testresults/etltutorial.csv; aq_udb -cnt etl-ess2working:vector1" --debug --master
    # The --master tag is now needed to tell Essentia to run this command on your master instance. This is required to ensure that essentia can draw all of the data from the memory of each of the worker nodes and combine them into the one csv file on the master instance.