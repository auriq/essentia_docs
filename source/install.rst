:tocdepth: 1

************
Installation
************

Essentia is available as either a desktop download, or via a cloud based service.  The tutorials on this site will
work with either, though for evaluating performance on larger or more complex data sets,
users should consider the cloud version which allows the creation of an Essentia cluster.


Desktop version
===============

The desktop version assumes you are using OSX or Linux as your operating system,
and that you have Python 2.7 installed.

1. Fetch the `installer <http://auriq.net/wp-content/uploads/installer/essentia-standalone-2.1.5.zip>`_
   (for both Mac and Linux) .
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

Once installed and the paths set, Essentia can be invoked from the command line using ``ess``.

Essentia is self contained, and to uninstall, one only needs to execute ``rm -rf ~/.local/essentia``.

Cloud version
=============
The cloud version requires that the user has an Amazon Web Services account.  New users can get more information from
our :doc:`aws/aws` guide.

We have created AMIs which any AWS user can launch to form a
private, AWS account specific master node.
Once active, you can log into the instance and start Essentia.  There is a version that requires a
license key to run, and a paid version which doesn't need a key but instead charges by the hour.

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


AWS additional notes
====================

.. toctree::

   aws/aws
   aws/security-group

