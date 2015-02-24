*************************
Calculate Sum and Maximum
*************************

This script imports the first three columns of a five column dataset.
It then adds the floating point value in the first column and takes the maximum integer value in the second column for
each unique value of the string-type third column. Selecting only the necessary subset of columns is good practice
for larger datasets, as it allows you to fit more of the relevant data into memory and thus increases the efficiency
of your analysis.

Primary Lines in this Script
============================

**Line 5**

* Store a vector in the database fivecoltutorial that keeps track of the maximum value of the integer column and aggregates the values in the float column for each unique value of the string column.

**Line 9**

* Tells Essentia to look for data on your current machine under the directory ../../data.

**Line 13**

* Create a new rule to take any files with 'fivecoltutorial' in their name and put them in the tutorialdata category.

**Line 18**

* Pipe all files in the category tutorialdata to the aq_pp command.
* In the aq_pp command, tell the preprocessor to take data from stdin, ignoring errors and skipping the first line (the header).
* Then define the incoming data's columns, skipping the fourth and fifth columns, and import the data to the vector in the fivecoltutorial database so the attributes listed there can be applied.

**Line 20**

* Export the modified and aggregated data from the database and save the results to a csv file.

.. code-block:: sh
   :linenos:
   :emphasize-lines: 5,9,13,18,20

   ess instance local
   ess spec drop database fivecoltutorial
   ess spec create database fivecoltutorial --ports=1

   ess spec create vector vector1 s,pkey:string_col i,+max:integer_col f,+add:float_col

   ess udbd start

   ess datastore select ../../data

   ess datastore scan

   ess datastore rule add "*fivecoltutorial*" "tutorialdata" "YYMMDD"

   ess datastore probe tutorialdata --apply
   ess datastore summary

   ess task stream tutorialdata "*" "*" "aq_pp -f,+1,eok - -d f:float_col i:integer_col s:string_col X X -ddef -udb_imp fivecoltutorial:vector1" --debug

   ess task exec "aq_udb -exp fivecoltutorial:vector1 -o fivecoltutorialresults.csv" --debug

   ess udbd stop
