:tocdepth: 1

***************
Desktop Install
***************

.. note::

    The desktop version uses Essentia 2.1.7 even though v3.0.0 now available for the Azure cloud.  An updated desktop
    installer will be made available soon.

The desktop version assumes you are using OSX or Linux as your operating system,
and that you have Python 2.7 installed.

1. Fetch the `installer <http://auriq.net/wp-content/uploads/installer/essentia-standalone-latest.zip>`_
   (for both Mac and Linux) .
2. Unpack the zip file.
3. ``cd`` into the directory it creates
4. type ``./install`` to start the installation.  Essentia will be installed by default to ``~/.local/essentia``
5. Add the executable directories to your ``$PATH`` environment variable.

Full example:

.. code-block:: sh

  unzip essentia-standalone-latest.zip
  cd essentia-standalone-latest
  ./install
  export PATH=$PATH:$HOME/.local/essentia/bin
  export PATH=$PATH:$HOME/.local/essentia/bin/aq_tool.osx/bin

The final line assumes you are using a mac.  If on a linux system, use 'aq_tool.x86' instead.
Also, the final two ``export`` commands assume you are using a Bourne shell (i.e. bash, zsh).  C-Shell users would use:

.. code-block:: sh

  setenv PATH $PATH:$HOME/.local/essentia/bin
  setenv PATH $PATH:$HOME/.local/essentia/bin/aq_tools/bin

Once installed and the paths set, Essentia can be invoked from the command line using ``ess``.

Essentia is self contained, and to uninstall, one only needs to execute ``rm -rf ~/.local/essentia``.