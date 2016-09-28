************
Docker Install
************

The docker version of Essentia will run on most systems. Due to the portable, containerized nature of docker, the docker version of Essentia is easy to install. 

Essentia's docker version cannot launch worker instances and thus does not have the full scalability of Essentia. If you need to parallelize your analyis, you can use the cloud version of Essentia or contact `essentia@auriq.com <mailto:essentia@auriq.com>`_.

.. Essentia's local version is limited to only scale to at most five worker instances and will work without additional licensing for up to one year. This license can be extended by contacting `essentia@auriq.com <mailto:essentia@auriq.com>`_.

How to Install Essentia using Docker
=============================================

.. note::
  
   You must have root privileges to run some of the following steps. If you do not, please contact your system administrator.

#. Install Docker. For a CentOs system, follow the steps under "Install with yum" and then "Create a docker group" here: https://docs.docker.com/engine/installation/linux/centos/. For other systems, follow the steps to install docker for your system by going to that link and navigating to your system's installation instructions using the left navigation bar.

#. Run::

    sudo apachectl stop

#. Open your firewall to port 80. The Commands for a CentOS 7 Firewall are::

    firewall-cmd --list-all-zones
    firewall-cmd --permanent --add-port=80/tcp --zone=public
    firewall-cmd --permanent --add-port=80/tcp --zone=internal
    firewall-cmd --reload

#. Fetch and run the container from docker:: 

    docker run --privileged -itd -e "container=docker"  -v /sys/fs/cgroup:/sys/fs/cgroup --name essentia -p 80:80 auriqsystems/essentia /usr/sbin/init

#. Check that the docker conatiner is running. Run:: 

    docker ps -a

    # CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS              PORTS             NAMES
    # 3c2cc851df58        auriqsystems/essentia   "/home/start_server.s"   17 hours ago        Up 17 hours         3306/tcp, 0.0.0.0:80->80/tcp, 10010-10079/tcp   essentia

#. Login to the Essentia Data Lake Manage UI by accessing the url of the instance and entering the following login information::

    Username: essentia
    Password: essentia

#. Change your username and password using the UI.

You can then go through :doc:`../../dlv/dlv`, :doc:`../../tutorial/essentiatutorials/index`, :doc:`../../tutorial/dataprocessingtutorials/index`, and :doc:`../../usecases/index` to get familiar with Essentia.

.. note:: 

   This software is subject to the End-User License Agreement located in :doc:`license`.

**Command Line Access**

To access your essenta docker container via the command line, secure shell into your instance and then run::

    docker exec -it essentia bash

This starts an interactive shell for the docker container so that you can enter and use the Essentia commands. 

**Note:** Always check your version of Essentia by running ``ess -v``.
If this version does not match the version of this documentation listed in the top-left of this page,
click the **Versions** link next to our documentation version and navigate to the documentation version that matches your version of Essentia.

Additional Notes
================

.. toctree::

   license

