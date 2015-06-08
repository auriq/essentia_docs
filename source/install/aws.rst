:tocdepth: 1

***********
AWS Install
***********


The cloud version requires that the user has an Amazon Web Services account.  New users can get more information from
our :doc:`aws/aws` guide.

Essentia is available as an Amazon Machine Image (AMI) which contains a Linux based OS with Essentia installed.
Any AWS user can launch on of these AMIs to form a private, AWS account specific master node.
Once active, you can log into the instance and start Essentia.  There is a version that requires a
license key to run, and a paid version which doesn't need a key but instead charges by the hour.

Cloud version (Free AMI)
========================

A trial license key is free, and can be obtained via an `easy signup <../pricing>`_.  It grants
the user 30 days of unlimited use.  Note however that standard EC2 rates
still apply, but during the trial the cost of using Essentia is free.

#. Go to your AWS console, where all services are listed.
#. Click on EC2.
#. Create on the 'Launch Instance' button.  This will take you to a site where
   you can select what OS and software you would like to access.
#. Select the 'community AMI' tab, and search for 'AuriQ'
#. The list of results will include the free version, as well as a link
   to the paid 'marketplace' version.  Select one to continue.
#. You will be asked to select a node type.  For almost all applications,
   an ``m3.medium`` is the safest choice, but the ``t2`` line is OK for
   testing or other work that does not require high performance.

At this point the decisions available will depend on your account and zone.
You may have the ability to launch Essentia into 'EC2-Classic' mode, or from
within a VPC.  The latter is preferred for security.  Whatever you choose,
you will eventually be asked to configure a security group.  This is important
enough that we created a separate walk-though for it: :doc:`aws/security-group`

Once your instance is configured and launched, you should copy your
license key (if using the free version) to it using the following command from a terminal::

  scp -i myinstance.pem essentia_license ec2-user@public.ip.add:.

The public IP will be listed on your AWS console.

Cloud version (Paid AMI)
========================
We also offer an unlocked version of the software on the Amazon Marketplace.
This version has no restrictions or time limits, but does cost a nominal free for each hour
it is in use.  Prices range from $0.07-$2.00 per hour depending on instance type used.

To get up and running with this AMI, the instructions are similar to the free version:

#. Go to your AWS console, where all services are listed.
#. Click on EC2.
#. Create on the 'Launch Instance' button.  This will take you to a site where
   you can select what OS and software you would like to access.
#. Select the 'Marketplace' tab, and search for 'AuriQ'
#. The list of results should include the latest release of Essentia.  Click on it to start.
#. Follow the setup instructions.

AWS additional notes
====================

.. toctree::

   aws/aws
   aws/security-group

