AWS Security Groups
-------------------

Security groups define a firewall used to restrict access to AWS resources.
Essentia typically requires 2 firewall settings:

1. SSH (port 22) access to the master node (so you can log into it)
2. HTTP (port 80) access to the master node (so you can access the web GUI)

Covering every organization or user's security preferences or requirements is
beyond the scope of this article.  We present here a simple setup sufficient
for many users.  For more complex configurations, please do contact us.


Configure via AWS Console
~~~~~~~~~~~~~~~~~~~~~~~~~

#. Log into Amazon AWS services on a web browser and navigate to EC2.￼
#. On the left menu, select “Security Groups”.
#. Click on “Create Security Group” button.
#. Enter a name for the Security group name (example: essentia-access).
#. Enter a description for the current security group (example: Essentia
   Access).
#. Select the VPC the instance belongs to.
#. Click on the “Add Rule” button.
#. Select 'SSH' from the Type dropdown menu, and 'My IP' from the Source dropdown.
#. Repeat the previous two steps, but this time selecting HTTP from the Type dropdown.
#. Click the “Save” button on the lower right corner.

.. caution::

    Security groups that are too open pose a potential security risk. Consult with your AWS experts or contact us
    for more advice on how to setup security groups.


Setup via the AWS Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Users with the AWS CLI installed may find :download:`this script <../../scripts/security-group.sh>` useful.
Simply save it in a file, and execute it using ``sh security-group.sh``
￼