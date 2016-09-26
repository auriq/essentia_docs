****************************
Managing Essentia Clusters
****************************

This tutorial applies to the AWS Installation only.

Essentia's true power is most recognizable in a scalable environment. However, the size of the computer cluster that is needed is highly dependent on the analysis your need performed and the size of the data that you're processing. Thus, Essentia contains a few commands to make it easy to use and reuse, size and resize, and delete your Essentia compute clusters. 

The following sections describe various scenarios and which commands to run in those scenarios. 

No Existing Clusters, Creating First Cluster
--------------------------------------------

1. Create entirely new computers to use as your worker nodes using ``ess cluster create --number=YOUR_NUMBER --type=YOUR_TYPE``. 

   **Ex:** ``ess cluster create --number=5 --type=m3.medium``

2. Connect to computers that already exist on Amazon EC2 and use them as your worker nodes using ``ess cluster add YOUR_RESERVATION_ID``. 
   You can view a computer's Reservation ID by clicking on the instance on the Amazon Console and viewing the number next to "Reservation".

   **Ex:** ``ess cluster add r-6b1f57d5``

Existing Clusters, Adding Additional Worker Nodes
-------------------------------------------------

First you must stop importing any data into your existing worker node instances so that Essentia's UDB Database can be redistributed. Then, to add additional worker nodes onto your existing cluster:

1. Create additional worker nodes on Amazon EC2 to add to your existing cluster by running ``ess cluster create --add --number=YOUR_NUMBER --type=YOUR_TYPE``. 
   This command will create and add **YOUR_NUMBER** of **YOUR_TYPE** instances on Amazon EC2 to your cluster.

   **Ex:** ``ess cluster create --add --number=2 --type=m3.medium``

2. Add existing computers to your existing cluster by referencing their Reservation ID using ``ess cluster add RESERVATION_ID``.

   **Ex:** ``ess cluster add r-6b1f57d5``

Finding Existing Clusters
-------------------------

To find information about the cluster you are currently running from the directory you started it from, run ``ess cluster status``. This will show you connection and resource information about each of the computers currently connected to in that cluster as well as show you those computers' Reservation ID(s) so that you can reuse them in the future.

To find information about all of the clusters you have connected to and kept the information of, look in the ESS_AWS_DIR. If you are not familiar with this directory please see `Advanced Options <../../reference/manuals/essentia-ref.html#advanced-options>`_. This directory contains all of the pem files that you've used to connect to your clusters as well as the Reservation ID's for the computers in those clusters.

Cleaning up Existing Clusters
-----------------------------



.. caution::
   Stop or Terminate your cluster(s) with Essentia before running ``ess cluster remove`` or you will have to stop or terminate them from the Amazon Console.




Allow  to reuse worker nodes.

Options for creating new instances and reuse existing ones

Allow adding or removing instances from a cluster

Enable synchronizing the Essentia version of a cluster with the master


ess cluster
  - in .conf/reservation.json (for 'custom')
    i. add 'user' parameter (default: 'ec2-user')
    ii. support for no 'pem' file (access worker nodes without log in)
  - ess cluster create --add: create additional worker nodes
  - ess cluster add: add worker nodes to cluster by reservation id
  - ess cluster remove: remove worker nodes from cluster by reservation id
  - ess cluster terminate: won't delete pem file, and security groups
  - ess cluter terminate --all: delete worker nodes, pem file, and security groups
  - ESS_AWS_DIR for storing pem files (default: ~/.aws)
* ess cluster status
  - add reservation id information

ess cluster		
	ess cluster create -add	create additional worker nodes
	ess cluster add	add worker nodes to cluster by reservation id
	ess cluster remove	remove worker nodes from cluster by reservation id
	ess cluster terminate	won't delete pem file, and security groups
	ess cluter terminate --all	delete all worker nodes, pem file, and security groups
	ess cluter terminate --all -y	terminate without user's confirmation
	ess cluster status	add reservation id information
	ess cluster reset	remove reservation.json file
	ESS_AWS_DIR	for storing pem files (default: ~/.aws)
	.conf/reservation.json	add 'user' parameter (default: 'ec2-user')
	.conf/reservation.json	support for no 'pem' file (access worker nodes without log in)
