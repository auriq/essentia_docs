*********************
6. R Integration
*********************

6.1 The R Package
-----------------

In order to use R with Essentia, you must install the RESS package from C-RAN (see installation instructions). 
This package contains two R functions that can be used to capture the output of essentia commands into R, **essQuery** and **read.udb**.

* **essQuery** is used to directly query the database using a single statement. You can call essQuery multiple times to run different statements.
* **read.udb**, on the other hand, reads all of the statements in a file. Thus if you plan to run multiple statements
  that may be somewhat related to each other, it is recommended that you use **read.udb**.

6.2 Essentia's Environment
--------------------------

Both functions require an Essentia Bash script to be executed that sets up the Essentia environment and optionally loads data into the UDB database. Thus they require you to run ::

    bash **load_script_name**.sh

In this tutorial we just want to setup a simple Essentia environment, one that runs on our local computer and scans our local filesystem for the browse and purchase data. 
Thus we save the following commands to my_setup_script.sh::

    ess instance local
    
    ess datastore select ../woodworking/diy_woodworking
    ess datastore scan
    
    ess datastore rule add "*browse*gz" "browse" "YYYYMMDD"
    ess datastore probe browse --apply
    ess datastore category change browse dateFormat "Y.m.d.H.M.S"
    ess datastore category change browse TZ GMT
    
    ess datastore rule add "*purchase*gz" purchase "YYYYMMDD"
    ess datastore probe purchase --apply
    ess datastore category change purchase dateFormat "Y.m.d.H.M.S"
    ess datastore category change purchase TZ GMT
    
6.3 essQuery
------------    
    
With the environment setup, we can now use essQuery to stream the browse and purchase files into two R dataframes. 

The essQuery function takes three arguments: ``essentia_command``, ``aq_command``, and ``flags``. 

The output can be saved into an R dataframe :: 

    **my_dataframe_name** <- essQuery(essentia_command, aq_command, flags)

or directly analyzed in R. For demonstration purposes, we'll save the output of each essQuery call to a dataframe.

First we must open an R script or the R interactive prompt and type ::

   library(RESS)
   
to tell R to use the installed RESS package. Then we run ::
    
   browsedata <- essQuery("ess task stream browse '*' '*'", "aq_pp -f,+1,eok - -d %cols -notitle", "#Rinclude")

to import the browse files into R and save them as a dataframe called browsedata. 

Here ``essentia_command`` is an ``ess task stream`` 
command pulling all of the browse data and sending it to aq_command. This aq_command then uses the ETL Engine's preprocessor, aq_pp, to import the files with the columns defined in the scan 
of the data (from the Essentia's Environment step) and export them in csv format with no header line. The ``#Rinclude`` flag tells essQuery to take the output of this statement and return it to R.

Similarly we run ::
    
   purchasedata <- essQuery("ess task stream purchase '*' '*'", "aq_pp -f,+1,eok - -d %cols -notitle", "#Rinclude")
   
to import the purchase files into R and save them as a dataframe called purchasedata. 

We are now free to analyze these files using the massive variety of R functions and methods. To get a quick count of the total number of rows and columns in each dataset we ran::

    nrow(browsedata)
    #[1] 299725
    
    ncol(browsedata)
    #[1] 3
    
    nrow(purchasedata)
    #[1] 41031
    
    ncol(purchasedata)
    #[1] 5

6.4 read.udb
------------

An alternative way to send the files to R is to use **read.udb**.

**read.udb** requires you to store the essentia queries in a bash script and then store that script's filename as ``file`` in R. Thus we save the following statements to myqueries.sh::

    ess task stream browse '*' '*' "aq_pp -f,+1,eok - -d %cols -notitle" #Rinclude #R#browsedata#R#
    ess task stream purchase '*' '*' "aq_pp -f,+1,eok - -d %cols -notitle" #Rinclude #R#purchasedata#R#

and then simply have R run::

    file <- "myqueries.sh"  # store myqueries.sh as file
    library(RESS)           # load Essentia's R Integration package
    
    read.udb(file)          # call read.udb to execute the essentia statements written in myqueries.sh and save them to R dataframes browsedata and purchasedata
    
    nrow(browsedata)
    ncol(browsedata)
    nrow(purchasedata)
    ncol(purchasedata)

The output is the same as before::

    299725
    3
    41031
    5
            
6.5 Next Steps
--------------

This tutorial was meant as a simple introduction to Essentia's R Integration and demonstrated how to use the functions inside the RESS package to send data through Essentia's preprocessor and into R.
We analyzed simple compressed, csv files and ran incredibly basic analysis. To see more advanced analysis of much more complex datasets, please read through our Apache Analysis Case Study.