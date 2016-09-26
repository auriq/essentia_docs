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

Existing Clusters, 

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
