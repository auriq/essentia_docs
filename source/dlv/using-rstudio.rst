***************
Using RStudio
***************

.. note::

    R and RStudio-Server are NOT part of our Essentia Platform. They are third party software that we enable users to install and integrate with AT THEIR OWN DISCRETION. This decision is up to the User and is not required to use any of AuriQ Systems Inc.'s solutions.

**Setting up RStudio**

.. sudo bash install-rstudio.sh

If you plan to use our RStudio Integration and you haven't enabled it yet, you need to:

1. Go to the AWS Console.
2. Right Click on your Instance and then click **Connect**.
3. Follow the Intructions on the page that appears to connect to your instance via the command line as the **ec2-user** (replace ``root@`` with ``ec2-user@``).
4. Once you are logged onto your instance in the ec2-user directory, run ``sudo bash /opt/essentia/install-rstudio.sh`` to install R and RStudio-Server on your instance.

**Accessing RStudio**

Go to the UI and then click the **RStudio** link in the top menu. If you just installed RStudio then you may need to refresh the UI page in order to see the RStudio menu option.

Enter **"essentia"** as the username and enter the **Instance ID** of your instance as your password.

You can now use all the capabilities of RStudio directly from your browser. 

**Running Essentia via RStudio**

First, Essentia's R Integration package must be installed by running ``install.packages("RESS")`` in R. Then, to access it, you simply need to enter the R command ``library(RESS)``. 
See our `R Integration Tutorial <../integrations/R/index.html>`_ to see how to use the RESS package to integrate R and Essentia.

To run an Essentia Bash Script that already exists on your file system, you can simply run it from within RStudio by navigating to the directory that contains your script and entering ``system("sh Your_Script_name.sh")``.

To create an Essentia Bash Script from within RStudio:

* Click **File** → **New File** → **Text File**
* Click **File** → **Save As**
* Enter your desired filename followed by **.sh** (Ex: Your_Script_Name.sh)

You are now free to enter any Essentia commands to accomplish your data preparation, integration, or analysis.

To Save your script, use a shortcut or click **File** → **Save**.

To run your script, navigate to the directory that contains your script and then either run ``system("sh Your_Script_name.sh")`` or click on **Run Script** in the top right of the Script Panel.