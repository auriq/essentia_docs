Installation
============

Essentia is being distributed in three formats:

1. Feature limited, desktop download.
2. Full featured, 30 day free trial on the AWS cloud.
3. Full featured, pay by the hour, AWS cloud version.

Two are based on the AWS cloud, and the other can be run on your desktop.
If you don't have an AWS account but are interested in using Essentia on the
cloud, we recommend reading :doc:`aws/aws`.

Desktop version
---------------

The benefit of the desktop version is that users do not need an AWS account.
We've removed the ability to launch worker nodes in the cloud as a consequence,
but otherwise the features are the same between it and the cloud based versions.

Installation instructions for the desktop version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The desktop version assumes you are using OSX or Linux as your operating system, and that you have Python 2.7 installed.

1. Fetch the installer (for both Mac and Linux) `here <http://auriq.net/wp-content/uploads/installer/essentia-standalone-2.1.5.zip>`_.
2. Unpack the zip file.
3. ``cd`` into the directory it creates
4. type ``./install`` to start the installation.  Essentia will be installed by default to ``~/.local/essentia``
5. Add the executable directories to your ``$PATH`` environment variable.

Full example:

.. code-block:: sh

  unzip essentia-standalone-2.1.5.zip
  cd essentia-standalone-2.1.5
  ./install
  export PATH=$PATH:$HOME/.local/essentia/bin
  export PATH=$PATH:$HOME/.local/essentia/bin/aq_tools/bin
  export PATH=$PATH:$HOME/.local/essentia/bin/aq_tools/udb

The final three ``export`` commands assume you are using a Bourne shell (i.e. bash, zsh).  C-Shell users would use:

.. code-block:: sh

  setenv PATH $PATH:$HOME/.local/essentia/bin
  setenv PATH $PATH:$HOME/.local/essentia/bin/aq_tools/bin
  setenv PATH $PATH:$HOME/.local/essentia/bin/aq_tools/udb

Essentia is self contained, and to uninstall, one only needs to execute ``rm -rf ~/.local/essentia``.

Full Featured, 30 day trial on AWS cloud
----------------------------------------

We have created a free public AMI which any AWS user can launch to form a
private, AWS account specific master node.
Once active, you can log into the instance and start Essentia.  This version
of will look for a license key which is needed to run.

This license is also free, and can be obtained `here <../pricing>`_.  It grants
the user 30 days of unlimited use.  Note however that standard EC2 rates
still apply, but during the trial the cost of using Essentia is free.

#. Go to your AWS console, where all services are listed.
#. Click on EC2.
#. Create on the 'Launch Instance' button.  This will take you to a site where
   you can select what OS and software you would like to access.
#. Select the 'community AMI' tab, and search for 'Essentia'
#. There may be more than one version listed, but new users should choose the
   most recently created version.
#. You will be asked to select a node type.  For almost all applications,
   an ``m3.medium`` is the safest choice, but the ``t2`` line is OK for
   testing or other work that does not require high performance.

At this point the decisions available will depend on your account and zone.
You may have the ability to launch Essentia into 'EC2-Classic' mode, or from
within a VPC.  The latter is preferred for security.  Whatever you choose,
you will eventually be asked to configure a security group.  This is important
enough that we created a separate walkthrough for it here.

Once your instance is configured and launched, you should copy your
license key to it using the following command from a terminal::

  scp -i myinstance.pem essentia_license ec2-user@public.ip.add:.

The public IP will be listed on your AWS console.

Full Featured, pay by the hour AWS Cloud version
------------------------------------------------

To use this unlimited version, follow the instructions for the trial based version with two exceptions:

1. Instead of 'Community AMIs', select 'AWS Marketplace' when you go to launch an EC2 instance.
2. No license key needs to be acquired.

The cost per hour ranges on the node type you use, but typically ~ $0.10/hour.


.. toctree::
   :hidden:

   aws/aws
   aws/security-group

