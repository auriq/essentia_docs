***************
Using RStudio
***************

*Disclaimer:* R and RStudio-Server are NOT part of our Essentia Platform. They are third party software that we enable users to install and integrate with AT THEIR OWN DISCRETION. This decision is up to the User and is not required to use any of AuriQ Systems Inc.'s solutions.

**Setting up RStudio**

.. sudo bash install-rstudio.sh

If you plan to use our RStudio Integration and you haven't enabled it yet, you need to:

1. Go to the AWS Console.
2. Right Click on your Instance and then click **Connect**.
3. Follow the Intructions on the page that appears to connect to your instance via the command line as the **ec2-user** (replace ``root@`` with ``ec2-user@``).
4. Once you are logged onto your instance in the ec2-user directory, run ``sudo su`` and then ``bash /opt/essentia/install-rstudio.sh`` to install R and RStudio-Server on your instance.
5. Open **/etc/httpd/conf/httpd.conf** with your favorite editor. For example, run ``nano /etc/httpd/conf/httpd.conf``.
6. Add the following lines to the bottom of **/etc/httpd/conf/httpd.conf**::

     <IfModule proxy_module>
       ProxyPass "/rstudio/" "http://localhost:8787/"
       ProxyPassReverse "/rstudio/" "http://localhost:8787/"
     </IfModule>

7. Run ``apachectl restart``.

**Accessing RStudio**

Go to the UI and then click the **RStudio** link in the top menu. If you just installed RStudio then you may need to refresh the UI page in order to see the RStudio menu option.

Enter **"essentia"** as the username and enter the **Instance ID** of your instance as your password.

You can now use all the capabilities of RStudio directly from your browser. 

If you wish to use the command line to access any of the analysis done in RStudio, you need to connect to your instance via the command line as 
the **ec2-user** (follow step 3 in **Setting up RStudio**) and then run ``sudo su essentia`` and ``cd /home/essentia``. 
This will put you in the home directory of the **essentia** user. This is the directory where all of the user's RStudio scripts and data are stored.

.. you need to connect to your instance via the command line as the **essentia** user (follow step 3 in **Setting up RStudio** and replace ``root@`` with ``essentia@``). 
.. The password is the **Instance ID** of your instance.

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
