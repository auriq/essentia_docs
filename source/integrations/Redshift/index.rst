*******************
Redshift Integration
*******************

This section demonstrates how to use Essentia to load data from various sources into Redshift quickly and efficiently. 

================================================
Data Integration: AWS Redshift and Essentia
================================================

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

* A running Redshift cluster.
* A running Essentia cluster.
* The Essentia security group needs to allow SSH (port 22) access from your Redshift cluster.
* The Redshift security group needs to allow port 5439 access from your Essentia cluster.
* Essentia cluster needs to be in the same zone as the Redshift cluster.
* Essentia cluster needs to be in the same VPC as the Redshift cluster, and cannot be in EC2-Classic.
* Redshift database username and password required.
* User needs to have write access to Redshift database.
* Essentia cluster needs an IAM role that allows it to spin up additional EC2 instances and that allows it access to Redshift (see IAM Role below).

IAM Role
========

Here is an example of a policy that allows access to EC2 Instances as well as Redshift::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:*"
                ],
                "Resource": [
                    "*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "redshift:*"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }

..  note::

    To learn how to create an IAM role, follow the instructions in :doc:`../../install/aws/iam-role`.

Moving data
===========

Transferring data is very straightforward.  First register the Redshift cluster with Essentia and then optionally generate a table using Essentia. 
Then provide the necesary Data Processing operation, which is in a format very similar to the 'stream' command described in
:doc:`../../tutorial/essentiatutorials/etl`, to load the data into the table::

  $ ess redshift register redshift_cluster_name redshift_database_name username password
  $ ess redshift gentable table_name category_name --key "column_name = distkey"
  $ ess redshift stream category_name start_date end_date "command" table_name --options TRUNCATECOLUMNS
  
Here, 'command' is typically ``aq_pp`` (see :doc:`../../tutorial/dataprocessingtutorials/etl`), but it can also be any other program that accepts text data from the stdin
and outputs the results to stdout.

Querying Data
=========================

Once you have data loaded into Redshift you can query that data with Essentia using sql statements. You simply run::

   $ ess redshift sql 'SQL_COMMAND'

Examples
=========

Users are encouraged to go through these examples in order.

.. toctree::
   :maxdepth: 2

   loadredshift_purchase
   loadredshift_access

