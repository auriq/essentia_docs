**************
Authentication
**************

In order for Essentia to launch worker nodes or access data on S3, it requires authentication.  This can be provided in three
different ways.

* Creating an `IAM Role <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html>`_ and attaching it to the instance during instance creation.
* Logging into the master node and running ``aws configure`` to save your AWS Access Credentials to a file. 
* Entering your AWS Access Credentials directly into the Essentia commands when they are needed.

A downside of the last two options is that the user needs to worry about the AWS Access Credentials, maintain their security, and 
update them should they change. Therefore, it is recommended to use IAM Roles instead.
If you do not have access to create an IAM Role, contact your AWS Administrator.

.. First, users can grant the master the authorization to create other ec2 instances and access S3.  

====================
Creating an IAM Role
====================

To create an IAM Role, follow these steps:

#. Open your AWS console
#. Select the "Identity & Access Management" menu.
#. From the left panel, select 'Roles'.
#. Click on 'CREATE NEW ROLE'.
#. Set the Role name. 'EssentiaMaster' for example.
#. Under 'AWS Service Roles', select 'Amazon EC2' (the top menu item)
#. The next menu will let you attach existing policies to your Role.  We won't select any, so be sure
   none of the checkboxes are ticked, then go to 'NEXT STEP'
#. The next menu we'll also skip. Just click 'CREATE ROLE'.
#. You should be back a menu that lists all the roles.  Select the one you just created and click on it.
#. Under INLINE POLICIES, click the menu to reveal a new link to create a new inline policy.  Click it.
#. Select a CUSTOM policy.
#. Name it something appropriate (optional)
#. Under the Policy Document section, cut and paste any of the following policies:

   * If you are using one of the other two methods for S3 access then you can use :doc:`worker-nodes-iam-role`.
   * If you are using one of the other two methods for creating worker nodes then you can use :doc:`s3-iam-role`.
   * If you are NOT using another method for authentication, use :doc:`worker-nodes-and-s3-iam-role`.

#. Finally click on 'APPLY POLICY'

.. caution::

   Improperly created roles pose a security risk.  The above roles are very liberal in granting permissions to spin up
   new ec2 instances and access s3 files. Consult with your AWS experts, or contact us if there are any questions or concerns.
   
.. note::

   If you plan to utilize our Redshift Integration, you need to enable Redshift access in your IAM Role. The following policies both do that:
   
* If you are using one of the other two methods for creating worker nodes and S3 access then you can use :doc:`redshift-iam-role`.
* If you are NOT using another method for authentication, use :doc:`worker-nodes-and-s3-and-redshift-iam-role`.

=============
AWS Configure
=============
    
Users can also grant the master the authorization to create other ec2 instances / access S3 by logging 
into their master node and running the command::

  aws configure

The user will then need to enter their AWS Access Credentials, which will then be stored in a file which Essentia will read when
it needs them.

================================
Command-Level Access Credentials
================================

Essentia also offers the ability to specify AWS Access Credentials in the various commands that use them. 

This can be a major benefit since it allows users or their administrators to change the level of access to 
suit the needs of the current analysis, by simply changing the access level of the credentials that were entered or 
entering new credentials with the desired access level.

**Appropriate Commands to Enter Access Credentials:**

Creating Worker Nodes for Scalability::

 ess cluster create ... --aws_access_key=**ENTER_AWS_ACCESS_KEY** --aws_secret_access_key=**ENTER_AWS_SECRET_KEY**

Accessing or Writing S3 Data::

 ess select ... --aws_access_key=**ENTER_AWS_ACCESS_KEY** --aws_secret_access_key=**ENTER_AWS_SECRET_KEY**

