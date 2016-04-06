===========================================
Loading and Querying Tutorial Purchase Logs
===========================================

To demonstrate Essentia's efficient ability to load many compressed files directly into a redshift cluster, we'll use the example of the tutorial data's purchase logs.

Setup Essentia
***************

To load our purchase log data into Redshift via Essentia we need to create a cloud Essentia cluster::

    ess cluster set cloud
    ess cluster create --number 2 --type m3.medium
    
and then select which AWS S3 Bucket our data is located in::

    ess select s3://asi-public --credentials=PATH/TO/CREDENTIAL_FILE.csv
    
and create a category to tell Essentia which data in our datastore corresponds to the purchase logs we want to load into Redshift::
    
    ess category add purchase "diy_woodworking/*purchase*"

Setup Redshift
***************    
            
Now we need to register and connect to our running Redshift cluster::
 
    ess redshift register redshiftdemo redshiftdemo essentia DEMOpassword999
      
and then use the purchase category to generate a Redshift SQL Table called ``purchase``::

    echo "---------- Replicating Category purhase as a Redshift Table ----------"
    ess redshift gentable purchase purchase --key "userID = distkey"
        
.. note:: 

   Instead of using the purchase category to generate an SQL Table we could have simply coded an SQL Table into a PostgreSQL editor connected to our Redshift Cluster

Load Redshift
***************

So far we've created our cloud Essentia cluster, connected to the data we want to load, created an SQL Table to store the data in, and connected to our running Redshift cluster. Now we can load the purchase log data into that SQL Table using the ``ess redshift stream`` command::

    ess redshift stream purchase "2014-09-01" "2014-09-03" "aq_pp -f+1,eok - -d S:purchaseDate I:userID I:articleID F:price I:referrerID -notitle" purchase --options TRUNCATECOLUMNS

Query Redshift
***************

The data has now been loaded into table ``purchase`` on our Redshift cluster. We can now query that data using an sql statement via Essentia::

    echo "---------- Running an SQL Query on the data in the Redshift Table purchase ----------"    
    ess redshift sql 'select * from purchase'
