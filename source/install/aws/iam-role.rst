IAM Roles
---------

In order for Essentia to launch worker nodes, it requires authentication credentials.  These can be provided in two
different ways.

First, users can log into their master node and run the command::

  aws configure

The user will then need to enter their credentials, which will then be stored in a file which Essentia will read when
it needs them.

A downside of this is that the user needs to worry about credentials, and updating them should they change.  A
simpler option is to grant the master the authorization to create other ec2 instances.  This is done via an
`IAM Role <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html>`_.

To create one, follow these steps:

#. Open your AWS console
#. Select the "Identity & Access Management" menu.
#. From the left panel, select 'Roles'.
#. Click on 'CREATE NEW ROLE'.
#. Set the Role name. 'EssentiaMaster' for example.
#. Under 'AWS Service Roles', select 'Amazon EC2' (the top menu item)
#. The next menu will let you attach 2 existing policies to your Role.  We won't select any, so be sure
   none of the checkboxes are ticked, then go to 'NEXT STEP'
#. The next menu we'll also skip. Just click 'CREATE ROLE'.
#. You should be back a menu that lists all the roles.  Select the one you just created and click on it.
#. Under INLINE POLICIES, click the menu to reveal a new link to create a new inline policy.  Click it.
#. Select a CUSTOM policy.
#. Name it something appropriate (optional)
#. Under the Policy Document section, cut and paste the following::

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
            }
        ]
    }

#. Finally click on 'APPLY POLICY'

.. caution::

   Improperly created roles pose a security risk.  The above role is very liberal in granting permissions to spin up
   new ec2 instances. Consult with your AWS experts, or contact us if there are any questions or concerns.
   
.. note::

   If you plan to utilize our Redshift Integration, you need to enable Redshift access in this IAM Role. The following policy will do that:
   
::

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
    