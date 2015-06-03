*************************
Calculate Sum and Maximum
*************************

To highlight some of the power of Essentia for batch processing operations, we have created a series of short
demos.  They use data from a fictional online casino. Data can be found in the ``casestudies/casino`` directory of
the git repository.  The data provides the username, time, bet (integer, US Dollars),
winnings (float, US Dollars), and country of origin of their customers.


In this demo, we are interested in a summary table that contains the total winnings and maximum bet that each user made.


This script imports columns 1, 3, and 4 of this dataset. It then takes the maximum of the bet values and adds
the winnings (which can also be negative) for
each unique username. Selecting only the necessary subset of columns is good practice for larger datasets, 
as it allows you to fit more of the relevant data into memory and thus increases the efficiency of your analysis.

Primary Lines in this Script
============================

**Line 4**

* Store a vector myvector in the database totalwinnings that keeps track of the maximum value of the bet column and aggregates the values in the winnings column for each unique value of the user column.

**Line 8**

* Tell Essentia to look for data on your local datastore.

**Line 10**

* Create a new rule to take any files with 'onlinecasino' in their name and put them in the casino category.

**Line 14**

* Pipe all files in the category casino to the aq_pp command. 
* In the aq_pp command, tell the preprocessor to take data from stdin, ignoring errors and skipping the first line (the header). 
* Then define the incoming data's columns, skipping the second and fifth columns (time and country), and import the data to the vector in the totalwinnings database so the attributes 
  listed there can be applied.

**Line 16**

* Export the modified and aggregated data from the database and save the results to a csv file.

.. code-block:: sh
   :linenos:
   :emphasize-lines: 4,8,10,14,16
    
   ess spec drop database totalwinnings
   ess spec create database totalwinnings --ports=1
    
   ess spec create vector myvector s,pkey:user i,+max:bet f,+add:winnings
    
   ess udbd start
    
   ess datastore select local
    
   ess datastore category add casino "$HOME/*onlinecasino*" --dateformat none
    
   ess datastore summary
    
   ess task stream casino "*" "*" "aq_pp -f,+1,eok - -d s:user X i:bet f:winnings X -udb_imp totalwinnings:myvector" --debug
    
   ess task exec "aq_udb -exp totalwinnings:myvector -o totalwinnings.csv" --debug
    
   ess udbd stop