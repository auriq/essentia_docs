************************************
R Integration - Tutorial Data
************************************

The R Package
=============

In order to use R with Essentia, you must install the RESS package from C-RAN. Open R and then run::

   install.packages("RESS")


This package contains three R functions that can be used to capture the output of Essentia commands into
R.

* **read.essentia** takes an Essentia script and captures the output csv data into R, where you can save the output to a dataframe or stream it directly into additional analysis. The output can only contain the csv formatted data that you want to read into R.
* **essQuery** is used to directly query the database using a single statement. You can call **essQuery** multiple times to run different statements. You can save the output to a dataframe or stream it directly into additional analysis.
* **capture.essentia**, on the other hand, takes a file containing any number of Essentia commands and captures the output of the specified statements into R dataframes. Thus if you plan to run multiple statements that may be somewhat related to each other, you may want to use **capture.essentia**.

Essentia's Environment
======================

All three functions require an Essentia Bash script to be executed that sets up the Essentia environment and optionally loads data into the UDB database. Thus they require you to run ::

    sh **load_script_name**.sh

In this tutorial we just want to setup a simple Essentia environment, one that runs on our local computer and scans our local 
filesystem for the browse and purchase data located in the ``tutorials/woodworking`` directory. 
If you are not already in the ``tutorials/woodworking`` directory used in the previous tutorials, switch into it now.
We save the following commands to essentia_setup.sh::

    ess select local
    
    ess category add browse "$HOME/*/woodworking/diy_woodworking/*browse*gz"
    
    ess category add purchase "$HOME/*/woodworking/diy_woodworking/*purchase*gz"


and then run ::

    sh essentia_setup.sh
    
read.essentia
=============

With the environment setup, we can now use **read.essentia** to stream the browse and purchase files into two R dataframes. 

The **read.essentia** function takes one argument: ``file``, which can contain any arguments that you could typically pass to a bash script. 

The output can be saved into an R dataframe :: 

    **my_dataframe_name** <- read.essentia(file)
    
**read.essentia** requires you to store the essentia query in a bash script. Thus we save the following statement to read_browse.sh::

    ess stream browse '*' '*' "aq_pp -f,+1,eok - -d %cols -notitle" #Rinclude #R#browsedata#R#
        
and the following statement to read_purchase.sh::

    ess stream purchase '*' '*' "aq_pp -f,+1,eok - -d %cols -notitle" #Rinclude #R#purchasedata#R#

and then simply have R run::

    library(RESS)           # load Essentia's R Integration package
    
    browsedata <- read.essentia('read_browse.sh')          # call read.essentia to execute the essentia statement written in read_browse.sh and save its output into R as a dataframe called browsedata
    
    purchasedata <- read.essentia('read_purchase.sh')          # call read.essentia to execute the essentia statement written in read_puchase.sh and save its output into R as a dataframe called purchasedata
   
We are now free to analyze these files using the massive variety of R functions and methods. To get a quick count of the total number of rows and columns in each dataset we ran::

    nrow(browsedata)
    #[1] 299725
    ncol(browsedata)
    #[1] 3
    nrow(purchasedata)
    #[1] 41031
    ncol(purchasedata)
    #[1] 5 
      
essQuery
========
    
We could also have used **essQuery** to stream the browse and purchase files into two R dataframes. 

The **essQuery** function takes three arguments: ``essentia_command``, ``aq_command``, and ``flags``. 

The output can be saved into an R dataframe :: 

    **my_dataframe_name** <- essQuery(essentia_command, aq_command, flags)

or directly analyzed in R. For demonstration purposes, we'll save the output of each **essQuery** call to a dataframe.

First we must open an R script or the R interactive prompt and type ::

   library(RESS)
   
to tell R to use the installed RESS package. Then we run ::
    
   browsedata <- essQuery("ess stream browse '*' '*'", "aq_pp -f,+1,eok - -d %cols -notitle", "#Rinclude")

to import the browse files into R and save them as a dataframe called browsedata. 

Here ``essentia_command`` is an ``ess stream`` 
command pulling all of the browse data and sending it to aq_command. This aq_command then uses the ETL Engine's preprocessor, aq_pp, to import the files with the columns defined in the scan 
of the data (from the Essentia's Environment step) and export them in csv format with no header line. The ``#Rinclude`` flag tells **essQuery** to take the output of this statement and return it to R.

Similarly we run ::
    
   purchasedata <- essQuery("ess stream purchase '*' '*'", "aq_pp -f,+1,eok - -d %cols -notitle", "#Rinclude")
   
to import the purchase files into R and save them as a dataframe called purchasedata. 

Alternatively, we could use ``ess query`` commands with **essQuery** to stream the browse and purchase data into dataframes in R. We would run ::

    querybrowse <- essQuery("ess query", "select * from browse:*:*", "#-notitle #Rinclude")
    
to import the browse data and ::

    querypurchase <- essQuery("ess query", "select * from purchase:*:*", "#-notitle #Rinclude")
    
to import the purchase data.

We are now free to analyze these files using the massive variety of R functions and methods. To get a quick count of the total number of rows and columns in each dataset we ran::

    nrow(browsedata)
    #[1] 299725
    ncol(browsedata)
    #[1] 3
    nrow(purchasedata)
    #[1] 41031
    ncol(purchasedata)
    #[1] 5
    nrow(querybrowse)
    #[1] 299725
    ncol(querybrowse)
    #[1] 3
    nrow(querypurchase)
    #[1] 41031
    ncol(querypurchase)
    #[1] 5
    
As you can see, both the stream and query methods of importing the files into R result in the same number of rows and columns when used on the same data over the same date range. 

capture.essentia
================

An alternative way to send the files to R is to use **capture.essentia**.

The capture.essentia function requires one argument, ``scriptcall``, and can take two optional arguments, ``linenumber`` and ``separator``.  

**capture.essentia** requires you to store the essentia queries in a bash script and then pass that script's name as ``scriptcall`` when you call capture.essentia in R. Thus we save the following statements to myqueries.sh::

    ess stream browse '*' '*' "aq_pp -f,+1,eok - -d %cols -notitle" #Rinclude #R#browsedata#R#
    ess stream purchase '*' '*' "aq_pp -f,+1,eok - -d %cols -notitle" #Rinclude #R#purchasedata#R#
    ess query "select * from browse:*:*" #-notitle #Rinclude #R#querybrowse#R#
    ess query "select * from purchase:*:*" #-notitle #Rinclude #R#querypurchase#R#

and then simply have R run::

    library(RESS)           # load Essentia's R Integration package
    
    capture.essentia("myqueries.sh")          # call capture.essentia to execute the essentia statements written in myqueries.sh and save them to R dataframes browsedata, purchasedata, querybrowse, and querypurchase
    
    nrow(browsedata)
    ncol(browsedata)
    nrow(purchasedata)
    ncol(purchasedata)
    nrow(querybrowse)
    ncol(querybrowse)
    nrow(querypurchase)
    ncol(querypurchase)

The output is the same as before::

    299725
    3
    41031
    5
    299725
    3
    41031
    5
            
Next Steps
==========

This tutorial was meant as a simple introduction to Essentia's R Integration and demonstrated how to use the
functions inside the RESS package to send data through Essentia's preprocessor and into R.
We analyzed simple compressed, csv files and ran incredibly basic analysis. The next tutorial, :doc:`rtutorial2`, 
will work with more complex logs that need to be converted and analyzed before being loaded into R, where we will 
plot the resulting data. To see more advanced analysis of much more complex datasets, 
please read through our :doc:`../usecases/rapache` use case.
