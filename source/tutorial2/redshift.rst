******************************************************
Empowering Data Integration with Redshift and Essentia
******************************************************

AWS provides a scalable SQL service called 'redshift'.  It is commonly used in data warehousing,
and can scale to store PB of data. But going from raw data into a properly formatted table suitable for Redshift (or
any other database for that matter) is often problematic.

We added a module to Essentia to address issues that include:

* File format: Redshift can read files that are compressed under gz, bz2, and lzo (or not compressed at all).  A lot
  of our clients had zip files which they wanted to load into Redshift.

* Data quality: Raw log data often requires filtering and transformation to produce the data that is actually desired.

Requirements
============
In order to link Essentia and Redshift, the following is needed:

* A running Redshift cluster
* The Essentia security group needs to allow SSH (port 22) access from your Redshift cluster.
* Essentia cluster needs to be in the same zone as the Redshift cluster
* Redshift database username and password required
* User needs to have write access to Redshift database.


Moving data
===========

Transferring data is very straightforward.  First register the Redshift cluster with Essentia,
and then provide the ETL operation which is in a format very similar to the 'stream' command as described in the
:doc:`ETL tutorial <../tutorial/etl>`::

  $ ess redshift register redshift_cluster_name
  $ ess redshift stream Standard 2014-12-01 2014-12-10 “command” -U username -d table -p password

Here, 'command' is typically ``aq_pp``, but it can also be any other program that accepts text data from the stdin
and outputs the results to stdout.

