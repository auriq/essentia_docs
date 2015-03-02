******************************
Obtain First, Last, and Minimum
******************************

Data exploration and anlysis requires many different operations to be apllied in various ways to various types of data. 
In the case of our online casino, it requires us to utilize all five columns of the data: username, time, bet (integer, US Dollars), winnings (float, US Dollars), and customer's country of origin.

In this script, we take the first time, last bet, and minimum winnings (worst loss) for each unique username in each unique country. We then order the results by the 
This demonstrates the ease with which Essentia can apply attributes to your data and return the results you want in the order you want them.


Primary Lines in this Script
============================

**Line 5**

* Store a table called grouping in the database worstloss that keeps track of the first value of the time column, last value of the bet column, and minimum value in the winnings column for each unique 
  value of the country and user columns.

**Line 9**

* Tell Essentia to look for data in your current directory.

**Line 13**

* Create a new rule to take any files with 'onlinecasino' in their name and put them in the casino category.

**Line 18**

* Pipe all files in the category casino to the aq_pp command. 
* In the aq_pp command, tell the preprocessor to take data from stdin, ignoring errors and skipping the first line (the header). 
* Then define the incoming data's columns and import the data to the vector in the worstloss database so the attributes 
  listed there can be applied.

**Line 20**

* Internally sort the records in the database, within each unique country, by winnings. Since this is internal, it has no output.

**Line 20**

* Export the modified and sorted data from the database and then save the results to a csv file.

.. code-block:: sh
   :linenos:
   :emphasize-lines: 5,9,13,18,20,21
    
   ess instance local
   ess spec drop database worstloss
   ess spec create database worstloss --ports=1
    
   ess spec create table grouping s,pkey:country s,+key:user s,+first:time i,+last:bet f,+min:winnings
    
   ess udbd start
    
   ess datastore select .
    
   ess datastore scan
    
   ess datastore rule add "*onlinecasino*" "casino" 
    
   ess datastore probe casino --apply
   ess datastore summary
    
   ess task stream casino "*" "*" "aq_pp -f,+1,eok - -d s:user s:time i:bet f:winnings s:country -udb_imp worstloss:grouping" --debug
    
   ess task exec "aq_udb -db worstloss -ord grouping winnings" --debug
   ess task exec "aq_udb -db worstloss -exp grouping -o worstloss.csv" --debug
    
   ess udbd stop