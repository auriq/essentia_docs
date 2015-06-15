AWS Account Creation
====================

If you don't have an AWS account, it is free to sign up.  New accounts get several services for free,
but with some restrictions.  See `the free tier page <http://aws.amazon.com/free>`_ for more information.  Since most
of the tutorials in this documentation are not computationally expensive, it would be safe to use the 'free tier' of
instances that AWS provides for new users.

Creating an AWS account
-----------------------

#. Go to `<http://aws.amazon.com>`_
#. Click on "Create an AWS Account" in the upper right hand corner.
#. Enter your email address and select "I am a new user" then "Sign in using our Secure Server".
#. Enter your name, email address, and password and then click "Create Account".
#. Fill Out Your Contact Information.
#. Enter Your Credit Card Information.
#. Enter your phone number and hit "Call Me Now" then enter the pin they provide into your phone.
#. Select a Support Plan. The free option is called "Basic".
#. Wait for your account to be created and then click "Launch the AWS Management Console".
#. Enter your email address and password to login.
#. Click on "Identity and Access Management", "Users", and then "Create New Users".
#. Enter a username and then click "Create" in the lower right corner.
#. Click "Show User Security Credentials" to see your credentials and then be sure to make a copy/record of them.
   You can also download a credential file to save your keys for future use.

Now What?
---------

The main AWS resource that Essentia uses are the EC2 instances.  These virtual
machines act as master and worker nodes in an Essentia cluster, and supply
the computing and memory required for processing data.  First time users are
strongly encouraged to read the excellent
`documentation <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html>`_ provided by Amazon.

Just as vital is the
`S3 data storage <http://docs.aws.amazon.com/AmazonS3/latest/gsg/GetStartedWithS3.html>`_
resource.  By providing highly redundant data storage in the cloud, Essentia
is able to effectively process large volumes of data without being I/O bound.

Although AWS related operations can be performed with the Web-based GUI the
AWS Console provides, we encourage our users to download and use the
`AWS Command Line Interface <http://aws.amazon.com/cli/>`_.
