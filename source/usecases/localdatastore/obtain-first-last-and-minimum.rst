*******************************
Obtain First, Last, and Minimum
*******************************

To highlight some of the power of Essentia for batch processing operations, we have created a series of short
demos.  They use data from a fictional online casino. Data can be found in the ``casestudies/casino`` directory of
the git repository.  The data provides the username, time, bet (integer, US Dollars),
winnings (float, US Dollars), and country of origin of their customers.


In this demo, we are interested in a summary table that provides the first time a user was seen in the system,
the amount of the last bet they made, and the result of the 'worst' bet (lowest winnings,
where negative indicates a loss).

In this script, we take the first time, last bet, and minimum winnings (worst loss) for each unique username in
each unique country. We then order the results by the minimum winnings.
This demonstrates the ease with which Essentia can apply attributes to your data and return the results you want in the order you want them.


Primary Lines in this Script
============================

**Line 11, 12**

* Store a table called grouping in the database worstloss that keeps track of the first value of the time column, last value of the bet column, and minimum value in the winnings column for each unique 
  value of the country and user columns. :ref:`Attributes <vec_attr>` are used to achieve this.

**Line 17**

* Tell Essentia to look for data on your local datastore.

**Line 19**

* Create a new rule to take any files in your home directory with 'onlinecasino' in their name and put them in the casino category. Also tell Essentia not to look for a date in the filenames.

**Line 24**

* Pipe all files in the category casino to the aq_pp command. 
* In the aq_pp command, tell the preprocessor to take data from stdin, ignoring errors and skipping the first line (the header). 
* Then define the incoming data's columns and import the data to the vector in the worstloss database so the attributes 
  listed there can be applied.

**Line 27**

* Internally sort the records in the database, within each unique country, by winnings. Since this is internal, it has no output.

**Line 29**

* Export the modified and sorted data from the database and then save the results to a csv file.

.. literalinclude:: ../../EssentiaPublic/casestudies/casino/worstloss.sh
   :language: bash
   :linenos:
   :emphasize-lines: 11,12,17,19,24,27,29
    
..   ess drop database worstloss
   ess create database worstloss --ports=1
    
   ess create table grouping s,pkey:country s,+key:user s,+first:time i,+last:bet f,+min:winnings
    
   ess udbd start
    
   ess select local
    
   ess category add casino "$HOME/*onlinecasino*" --dateformat none
    
   ess summary
    
   ess stream casino "*" "*" "aq_pp -f,+1,eok - -d s:user s:time i:bet f:winnings s:country -udb -imp worstloss:grouping" --debug
    
   ess exec "aq_udb -db worstloss -ord grouping winnings" --debug
   ess exec "aq_udb -db worstloss -exp grouping -o worstloss.csv" --debug
    
   ess udbd stop
