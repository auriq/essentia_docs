Installation
============

Essentia is being distributed in three formats.

1. Feature limited, desktop download.
2. Full featured, free 30 day trial on the AWS cloud.
3. Full featured, pay by the hour, AWS cloud version.

Desktop version
---------------

The benefit of the desktop version is that users do not need an AWS account.  Therefore the scaling features,
such as the ability to launch a cluster of worker nodes, is not available.  Otherwise the features are the same
between it and the cloud based versions.

Installation instructions for the desktop version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Fetch the installer (for both Mac and Linux) `here <http://www.auriq.net/local-install/>`_.
2. Unpack the zip file.
3. ``cd`` into the directory it creates
4. type ``./install`` to start the installation.  Essentia will be installed by default to ``~/.local/essentia``
5. Add the executable directories to your ``$PATH`` environment variable.

Full example::

unzip essentia-standalone-2.1.5.zip
cd essentia-standalone-2.1.5
./install
export PATH=$PATH:$HOME/.local/essentia/bin
export PATH=$PATH:$HOME/.local/essentia/bin/aq_tools/bin
export PATH=$PATH:$HOME/.local/essentia/bin/aq_tools/udb

The final three ```export`` commands assume you are using a Bourne shell (i.e. bash, zsh).  C-Shell users would use::

setenv PATH $PATH:$HOME/.local/essentia/bin
setenv PATH $PATH:$HOME/.local/essentia/bin/aq_tools/bin
setenv PATH $PATH:$HOME/.local/essentia/bin/aq_tools/udb

Essentia is self contained, and to uninstall, one only needs to execute ``rm -rf ~/.local/essentia``.

Full Featured, 30 day trial on AWS cloud
----------------------------------------

