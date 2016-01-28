************
Local Install
************

The local version of Essentia will run on Linux systems such as Centos 6. Installing the local version of Essentia on these systems is simple. 

How to Install Essentia on your Local Machine
=============================================

#. Go to the directory where the installer is located.

#. Run::

    unzip essentia-linux-x64-310_1.zip
    
#. Read the README and LICENSE.txt files.

#. Run:: 

    sudo ./essentia-linux-x64-310_1.sh

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

Essentia requires Python 2.7.5 or greater. If you encounter the error: "ess requires Python 2.7.5 and up." during installation then you need to install a newer version of Python.
    
To **Uninstall Essentia**: 

#. Run::

    sudo ./essentia-linux-x64-310_1.sh

#. Type ``y`` to uninstall Essentia.

#. Type ``y`` to confirm that you want to uninstall Essentia.

.. install locations
.. uninstall
.. python2.7
..   "ess requires Python 2.7.5 and up."
.. select "y" to install the Data Processing Tools (aq_tool).
