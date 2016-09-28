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

Existing Clusters, Removing Worker Nodes
-------------------------------------------------

Again, you must first stop importing any data into your existing worker node instances so that Essentia's UDB Database can be redistributed. Then, to remove worker nodes from your existing cluster:

1. Remove computers from your existing cluster by referencing their Reservation ID using ``ess cluster remove RESERVATION_ID``.

   **Ex:** ``ess cluster remove r-6b1f57d5``

Finding Existing Clusters
-------------------------

To find information about the cluster you are currently running from the directory you started it from, run ``ess cluster status``. 
This will show you connection and resource information about each of the computers currently connected to in that cluster as well as 
show you those computers' Reservation ID(s) so that you can reuse them in the future.

You can find information about all of the clusters you have connected to and kept the information of by looking in the ESS_AWS_DIR. 
If you are not familiar with this directory please see `Advanced Options <../../reference/manuals/essentia-ref.html#advanced-options>`_. 
This directory contains all of the pem files that you've used to connect to your clusters as well as the Reservation ID's for the computers in those clusters.

.. Not sure about the Reservation ID info for all clusters or just in ess cluster status

Cleaning up Existing Clusters
-----------------------------

You can **Stop** or **Terminate** the cluster you are connected to in your current directory using ``ess cluster stop`` or ``ess cluster terminate``. 
By default, Essentia will remember your connection information for the computers you used for this cluster so you can reuse those computers easily in the future.

You can choose to have Essentia both **terminate** and **forget** you cluster's computers by running either of the following::

 ess cluster terminate --all       # Terminate and forget your cluster
 ess cluster terminate --all -y    # Terminate and forget your cluster without requiring the user's confirmation

.. .. caution::
..    Stop or Terminate your cluster(s) with Essentia before running ``ess cluster remove`` or you will have to stop or terminate them from the Amazon Console.
