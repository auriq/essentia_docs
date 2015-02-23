***********************
Scaling R with Essentia
***********************

It is a good idea to have port 8787 open when using the R integrator and this is necessary when
using rstudio-server on an AWS instance.

Installing R and Rstudio-server
--------------------------------
First you need to install R and, optionally, Rstudio-server on your machine.

The commands to do this are, for a linux-based Redhat/CentOS 5.4+ system::

    sudo yum update
    sudo yum install R

and, to install Rstudio-server::

    sudo yum install openssl098e # Required only for RedHat/CentOS 6 and 7
    wget http://download2.rstudio.org/rstudio-server-0.98.1091-x86_64.rpm
    sudo yum install --nogpgcheck rstudio-server-0.98.1091-x86_64.rpm

For other types of systems, see

<http://www.jason-french.com/blog/2013/03/11/installing-r-in-linux/> and

<http://www.rstudio.com/products/rstudio/download-server/>

Connecting via Rstudio-server (Optional)
----------------------------------------

Make sure you have a user with a username and password so you can login to Rstudio-server.
If you dont, create one with::

    adduser **user_name**
    passwd **password**

You can then connect to rstudio by typing in your URL followed by :8787 in your browser::

    **URL**:8787

Login with the user and password you created in the previous step.