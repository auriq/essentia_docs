*****************************************
Setting up a Customized Cluster
*****************************************

Let's say we have a master node (M), and several worker nodes (W). To configure your system to utilize this full compute cluster, do the following steps:

1. Create 'ec2-user' user on all the nodes (M+W). Right now, only the user 'ec2-user' is supported.

2. Configure the nodes so M can ssh to W using a pem file just like AWS EC2:

* Generate the key with `ssh-keygen -t rsa -b 2048 -v` on M or use a pem file from AWS EC2. If you use a pem file from EC2, you can create the corresponding pub file from ~/.ssh/authorized_keys.
* Upload the public certificate to each W: `ssh-copy-id -i ~/my-certificate.pub ec2-user@W_IP` (Running once for each worker node you want to add and replacing 'W_IP' with your worer node's public IP).
* Make the .pem file on your M read-only `chmod 400 my-certificate.pem`.
* Confirm you can login to each W by running `ssh -i /path/to/my-certificate.pem ec2-user@W_IP` (no password should be needed). 
  
  *Note:* Don't change the default ssh port number (22).

3. Install Essentia on all the nodes (M+W) by following the instructions for your chosen method in :doc:`../../install/index`.
4. Try `ess -v` on each node to confirm the Essentia installation was successful.

5. Go to your working directory on your M:

* Run `ess cluster set custom`.
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

6. Run `ess cluster status` on your M, you should get something like::

    Summary for cluster my_id

    ID        state    publicIP    privateIP    cpu      mem disk
    --------  -------  ----------  -----------  -----  ----- ------
    master    running  127.0.0.1   127.0.0.1    [0.0]   20.1 10.7
    worker-1  running 10.1.0.10 10.1.0.10   [0.0]   27.8    10.1
    worker-2  running 10.1.0.11 10.1.0.11    [0.0]   27.8    10.1
    worker-3  running 10.1.0.12 10.1.0.12   [0.0]   27.8    10.1

7. Your customized cluster is ready to use now. You can just use Essentia as if a cluster existed

   **Note:** The "ess cluster [create|start|stop|terminate]" commands do not apply in the 'custom' setting.
