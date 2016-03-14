************
Local Install
************

The local version of Essentia will run on Linux systems. It's tested on 6 Linux 
based operating systems including Amazon Linux 2015.09.1, CentOS 7.1, Debian "Jessie",Ubuntu 15.04, 
Red Hat Enterprise Linux 7.2, and Fedora 23. Installing the local version of Essentia on these systems is simple. 

Essentia's local version is limited to only scale to at most five worker instances and will work without additional licensing for up to one year. This license can be extended by contacting `essentia@auriq.com <mailto:essentia@auriq.com>`_.

How to Install Essentia on your Local Machine
=============================================

.. note::
  
   You must have root privileges to run the installer. If you do not, please contact your system administrator.

#. Go to the directory where the installer is located.

#. Run::

    unzip essentia-linux-x64-310_3.zip
    
#. Read the README and LICENSE.txt files.

#. Run:: 

    sudo ./essentia-linux-x64-310_3.sh

#. Type ``y`` to install Essentia.

#. Add ``/opt/aq_tool/bin`` in your PATH variable.
   To do so, add the following two lines in your ~/.bash_profile::

    PATH=$PATH:/opt/aq_tool/bin
    export PATH

#. Then run:: 
    
    source ~/.bash_profile

You can then go through our :doc:`../../tutorial/essentiatutorials/index`, :doc:`../../tutorial/dataprocessingtutorials/index`, and :doc:`../../usecases/index` to get familiar with Essentia.

.. note:: 

   This software is subject to the End-User License Agreement located in :doc:`license`.

.. Essentia requires Python 2.7.5 or greater. If you encounter the error: "ess requires Python 2.7.5 and up." during installation then you need to install a newer version of Python.

This software requires python2.7.5 or higher, pip2.7 and wget.

If your system does not have python2.7.5 or higher, please read the python download page:

https://www.python.org/downloads/

If your system does not have pip, please read the following instruction:

https://pip.pypa.io/en/stable/installing/

Alternatively, the installation script provides an option to automatically install pip and wget 
for the above listed operating systems.
    
To **Uninstall Essentia**: 

#. Run::

    sudo ./essentia-linux-x64-310_3.sh

#. Type ``n`` when asked to install Essentia.

#. Type ``y`` to uninstall Essentia.

#. Type ``y`` to confirm that you want to uninstall Essentia.

Additional Notes
================

.. toctree::

   license

.. install locations
.. uninstall
.. python2.7
..   "ess requires Python 2.7.5 and up."
.. select "y" to install the Data Processing Tools (aq_tool).
