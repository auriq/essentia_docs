***********
AWS Install
***********


The Amazon cloud version requires that the user has an Amazon Web Services account.
New users can get more information from our :doc:`aws-account` guide.

Essentia is available as an Amazon Machine Image (AMI) which contains a Linux based OS with Essentia
installed. Any AWS user can launch this AMI to create a private, AWS account specific master node.
Prices range from $0.07-$2.00 per hour depending on instance type used, although the t2.micro instance type
is free for AWS users interested in simply evaluating the software.


How to Launch Essentia in the Amazon Cloud
==========================================

#. Go to your AWS console, where all services are listed.
#. Click on EC2.
#. Click on the **'Launch Instance'** button.  This will take you to a site where
   you can select what OS and software you would like to access.
#. Select the **'Marketplace'** tab, and search for **'AuriQ'**
#. The list of results should include the latest release of Essentia.  Click on it to start.
#. You will be asked to select a node type.  For most users,
   an ``m3.medium`` is the safest choice, but the ``t2`` line is OK for
   testing or other work that does not require high performance. 
   The t2.micro is free if you qualify for the AWS Free Tier.
#. Amazon will now ask you to **'Configure Instance Details'**.  Use the list below as a guide:

   * Number of instances = **1**
   * Network: Select VPC and choose one of your available VPCs.
   * Subnet: Select a subnet to launch in.

   | There is no strict requirement on what VPC to launch Essentia in, with one exception:
   Users wanting to use the **REDSHIFT** integrator should launch Essentia into the **same VPC**
   as their Redshift cluster.

   * Auto-assign Public IP: **ENABLE**
   * IAM Role: **None** is OK, though it would be ideal to attach an IAM role that authorizes the
     instance to spin up more ec2 instances (worker nodes) to aid in processing.  For more
     information, refer to our section on :doc:`iam-role`.

   | If you plan to use our RStudio Integration, you need to click **Advanced Details**. 
   Then, in the *User Data* section, enter **"rstudio"**.
   
   Remaining options are OK. Click **NEXT** at the bottom of the screen.
   
#. Add Storage section: defaults are fine. (click **NEXT**)
#. Tag Instance.  Not required but useful to name your instance. Do this and click **NEXT**.
#. Configure Security Group. We need to create a new group to handle the firewall between the internet
   and an Essentia Master node.  Please refer to our walk through: :doc:`security-group`
#. Once your security group is setup, click **REVIEW AND LAUNCH**, and then **LAUNCH**.  You will be asked
   to generate a new access key pair, or use an existing one.  The file created in this process is
   critical because it is the only way to gain access via SSH to your worker node.



AWS additional notes
====================

.. toctree::

   aws-account
   iam-role
   security-group

