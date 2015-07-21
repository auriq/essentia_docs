:tocdepth: 1

*************
Azure Install
*************

The Azure version is hosted on the Azure Marketplace, and users can use
`this direct link <http://azure.microsoft.com/en-us/marketplace/partners/auriq-systems/essentia-data-viewer/>`_ to access it.

.. note::

   Users are required to have an Azure account to launch this or any other Virtual Machine on the Azure cloud.  Details on
   Azure and the sign up process are available fro Microsoft's `Azure Web Page <https://azure.microsoft.com/en-us/>`_.

The Essentia Data Lake Viewer is run on a standalone virtual machine which you can provision and control.  Access is available
via a web based UI and via an SSH connection.  At the Azure store, click on the *Create Virtual Machine* button to start the
provisioning process.  This will redirect you to an Azure portal signin, or directly to the VM creation blade if already signed in.

In the creation blade, the Essentia Data Lake Viewer product will be listed.  Clicking on that leads to a series of new blades
requiring configuration information from the user.

Configuring the VM
******************
The instructions below are meant to get Azure subscribers up and running with Essentia quickly. Users are encouraged to review
the Azure documentation for a more full explanation of some of the settings.  The five sections below represent the 5 creation steps
listed in the Azure blade during provisioning.  After each step, clicking OK will move to the next step in the chain.

1.  **BASICS**:

* name:   Name of the VM.
* User name:  Pick the name of the admin user for the VM
* Authentication type: Can be Password or key based.  Password is easier, key-based is more secure (see `this note <https://azure.microsoft.com/en-us/documentation/articles/virtual-machines-linux-use-ssh-key/>`_.
* Resource Group: Can be an existing group, but preferably a new one should be created.

2. **SIZE**:
   The Data Lake Viewer requires only modest computing, which is why the A1 and D1 series of VMs are recommended.  Larger
   instance types can be provisioned, but do not add much to performance.  **A1 Standard** should be selected if possible.  Users
   who want to make extensive use of the file migration tool may prefer the D1 series.
3. **SETTINGS**:
   All of these can be left to their default settings unless specific networking and storage setups are required.
4. **SUMMARY**:
   Simply provides a summary of the VM settings.
5. **BUY**:
   Provides a final note and the 'buy' button.  Until 'Buy' is pressed, no charges to your Azure account have been made.


Once the 'BUY" option is worked through, the 'CREATE' button in the remaining blade will be opened.  Press this to provision the
instance and launch Essentia.


Configuring the Web UI
**********************

Assuming deployment is successfull, a VM will be created.  Typically the access point will be of the form ``http://yyy.cloudapp.net`` where
``yyy`` is the VM name chosen in step 1 above.

Once the VM is running, a web server will start. Connect to your instance via any web browser and you will be asked to provide a UI admin
username and password.  This can be the same as in step 1 above, but does not have to be.








.. toctree::
   :maxdepth: 1

   migration
