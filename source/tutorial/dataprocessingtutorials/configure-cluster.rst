*****************************************
Setting up a Customized Cluster
*****************************************

Introduction
============

This tutorial assumes you already have computers accessible to you so you can connect to them and configure them for use with Essentia. If this is not the case:

* For a **Local** or **Docker** installation, ask your system administrator if you could have access to more computers and then follow this tutorial.
* On the **Azure Cloud**, follow the instructions in :doc:`../../install/azure/index` for each additional computer you want to add to your cluster and use for scaling your analyses.

Instructions
============

Let's say we have a master node (**M**), and several worker nodes (**W**). To configure your system to utilize this full compute cluster, do the following steps:

1. Create 'ec2-user' user on all the nodes (**M** + **W**). Right now, only the user 'ec2-user' is supported.

2. Configure the nodes so **M** can ssh to **W** using a pem file just like AWS EC2:

* Generate the key with ``ssh-keygen -t rsa -b 2048 -v`` on **M** or use a pem file from AWS EC2. Type **ENTER** to accept the default key file setting '~/.ssh/id_rsa' and then type **ENTER** two more times to make an empty passphrase. If you use a pem file from EC2, you can create the corresponding pub file from ~/.ssh/authorized_keys.

  *Note:* Make sure your key file ends with '.pem'. If it does not, run ``mv YOUR_PATH/my-certificate YOUR_PATH/my-certificate.pem``.

* Upload the public certificate to each **W**: ``ssh-copy-id -i YOUR_PATH/my-certificate.pub ec2-user@W_IP`` (Running once for each worker node you want to add and replacing '**W_IP**' with your worer node's public IP). If you used the default key file above then you would run ``ssh-copy-id -i ~/.ssh/id_rsa.pub ec2-user@Worker_IP`` for each **W**.
* Make the .pem file on your **M** read-only ``chmod 400 YOUR_PATH/my-certificate.pem``.
* Confirm you can login to each **W** by running ``ssh -i YOUR_PATH/my-certificate.pem ec2-user@W_IP`` (no password should be needed).
  
  *Note:* Don't change the default ssh port number (22).

3. Install Essentia on all the nodes (**M** + **W**) by following the instructions for your chosen method in :doc:`../../install/index`. Azure Install users can skip this step.
4. Run ``ess -v`` on each node to confirm the Essentia installation was successful. You should receive output in the form of::

    Essentia : Your_Version
    AQ Tools : Your_Version --- Date

5. Go to your working directory on your **M**:

* Run ``ess cluster set custom``.
* Copy your pem file to the .conf subdirectory.
* Inside the .conf subdirectory, create a file named "reservation.json" with the following content::

   {
      "id": "my_id",
      "pem": "pem_file_name",
      "ip_list": ["W1_IP","W2_IP", ...]
   }

  For example, in your .conf folder, you should have at least three files::

   dev.pem
   reservation.json
   .platform

  and reservation.json can look something like below::

   {
      "id": "my_id",
      "pem": "dev",
      "ip_list": ["10.1.0.10","10.1.0.11","10.1.0.12"]
   }

6. Run ``ess cluster status`` on your **M**, you should get something like::

    Summary for cluster my_id

    ID        state    publicIP    privateIP    cpu      mem disk
    --------  -------  ----------  -----------  -----  ----- ------
    master    running  127.0.0.1   127.0.0.1    [0.0]   20.1 10.7
    worker-1  running 10.1.0.10 10.1.0.10   [0.0]   27.8    10.1
    worker-2  running 10.1.0.11 10.1.0.11    [0.0]   27.8    10.1
    worker-3  running 10.1.0.12 10.1.0.12   [0.0]   27.8    10.1

7. Your customized cluster is ready to use now. You can just use Essentia as if a cluster existed

   **Note:** The ``ess cluster [create|start|stop|terminate]`` commands do not apply in the 'custom' setting.
