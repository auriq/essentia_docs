***************
R Integration
***************

These next tutorials demonstrate how to read data from various sources into R using the functions available in Essentia's R Integration package. 

Installing the R Package
========================

In order to use R with Essentia, you must install the RESS package from C-RAN. The t2.micro AWS intance does not have sufficient memory to install the RESS package, we recommend at least an m3.medium. Once you have an instance of sufficient size, open R and then run::

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

Examples of Essentia Environments are given in each of the tutorials below, as well as how to read the resulting data into R.

Tutorial Data
=============

We maintain a `GitHub repository <https://github.com/auriq/EssentiaPublic>`_ that contains test data and source code for
some of the tutorials you will find in this documentation.  

.. For AWS users, we also have a public S3 bucket (s3://asi-public) that stores the larger and more complex datasets used for training purposes.

To get started, pull the tutorial repository via::

  $ git clone https://github.com/auriq/EssentiaPublic.git

The data and scripts relevant for most of the tutorials are under ``tutorials`` and ``case studies``. This data is required in order to run any of the example code provided in this section.

Tutorials
=========

Users are encouraged to go through the tutorials in order.

.. toctree::
   :maxdepth: 2

   rtutorial
   rtutorial2
   rtutorial3
   rapache
   rpackage


   
