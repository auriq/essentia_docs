********
Overview
********

The command structure of aq_pp consists of an **input specification** specifying which file(s) to take the data from,
various **processing specifications** to determine how data is processed, and **output specifications** describing how
and where to put the results of your command.
There are also a variety of global options that modify the environment and default variables used in ``aq_pp``.


Input Specifications
====================

First let's create a simple command that **imports** our example file ``chemistry.csv`` and **defines** its columns.

``aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin``

* ``-f`` specifies the file to operate on (chemistry.csv).  It accepts an optional ATTRIBUTE in ``,+1``, which
  means to skip the first line (header in this case)
* ``-d`` defines the column names and types.  The format is t,attribute:name with 't' being the type.  An 'X' means to
  ignore a column.  In this example, we load the names and final grades as strings (forcing the last name to be upper
  case), the student id as an integer, and the midterm grade as a float.

Since there are no processing or output specifications given, the the output is simply::

  "id","lastname","firstname","chem_mid","chem_fin"
  1,"DAWSON","Leona",76.5,"B-"
  2,"JORDAN","Colin",25.899999999999999,"D"
  3,"MALONE","Peter",97.200000000000003,"A+"

By default, ``aq_pp`` will validate the input against the type you defined it as.  For instance if a string is seen
in the 'float_col', the program will exit with an error.  By specifying the optional ``eok`` attribute along with
``-f,+1``, the program will simply ignore the input row.  This feature makes it easy to produce validated output.




Process Specifications
======================




Output Specifications
=====================

Now that you've completed your preprocessing of the data, its time to output your results. The output goes to **standout output** by default.

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -o -``

* This outputs the tutorial data to standard out. 

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country``

* This command does the same thing since aq_pp's default output spec is to standard out ('-o -'). The output is::
 
    "float_col","integer_col","last_name","first_name","country"
    99.909999999999997,5350,"Lawrence","Lois","Philippines"
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal"
    45.289999999999999,8356,"Wheeler","Sarah","Portugal"
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines"
    
You can also specify that you want the output to be **saved to a file**, which columns you want output, and whether you want the output to have a header.
 
``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -o outputfile.csv -c first_name last_name -notitle``

* This saves first_name and then last_name of tutorialdata.csv without a header to a file called outputfile.csv. The output the file contains is::
 
    "Lois","Lawrence"
    "Evelyn","Hamilton"
    "Sarah","Wheeler"
    "Jacqueline","Kelley"
    
Another form of output is to **only output the variables** you've defined and modified in your previous analysis. This is accomplished with the ``-ovar`` option.

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -var 'f:rolling_sum' 0 -var 'f:record_count' 0 -evlc 'rolling_sum' 'rolling_sum + float_col' -evlc 'record_count' 'record_count + 1' -evlc 'f:rolling_average' 'rolling_sum / record_count' -ovar -``

* This command initializes two new variables: a float called rolling_sum set to zero and a float called record_count set to zero. It then adds the value of float_col to rolling_sum, increases record_count by one, and divides rolling_sum by record_count for each record in the input data. 
* The columns are not included in the standard output, only the variables are included. The output is::
 
    "rolling_sum","record_count"
    222.33999999999997,4

If you just want to preprocess your data then you can pretty much stop there. But, if you want to continue to analyze your data and utilize the true power of Essentia then you should **import your data into the Essentia Database (Udb)**.

The Udb database allows you to store your preprocessed and modified data in tables and vectors, organized by the unique values of a primary key (pkey) column. It then allows you to apply attributes to the data as it is imported into these tables and vectors, when more than one record contains the unique value of the key column. 

Thus ou can condense your data to just the number of unique values of the specified column, with all of the relevant records for each unique value of that column combined by the attributes you specify.

Say you have a **database** called my_database that contains a vector called country_grouping which has the column specification ``s,hash:country s:full_name i,+add:integer_col f,+max:float_col s:extra_column``. Running the following code will **import the data into your vector and apply the attributes listed there**.
 
``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -evlc s:full_name 'first_name + " " + last_name' -ddef -udb_imp my_database:country_grouping"``

* The output from exporting the vector to standard out (see aq_udb documentation) is::
 
    "country","full_name","integer_col","float_col","extra_column"
    "Portugal","Sarah Wheeler",9605,73.609999999999999,
    "Philippines","Jacqueline Kelley",15028,99.909999999999997,
    
To learn more about the Essentia Database, please review our aq_udb Tutorial.



Conditional Option Groups
=========================

A final yet incredibly useful technique for processing your data is to use conditional statements to modify your data based on the results of the conditions. In aq_pp these are contained in ``-if``, ``-elif``, and ``else`` statements.

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -if -filt 'country == "Portugal"' -evlc s:Is_Portugese '"TRUE"' -else -evlc Is_Portugese '"FALSE"' -endif``

* This creates an -if -else statement that creates the column Is_Portugese and gives it a value of TRUE if the country is 'Portugal' and FALSE otherwise. The output is::
 
    "float_col","integer_col","last_name","first_name","country","Is_Portugese"
    99.909999999999997,5350,"Lawrence","Lois","Philippines","FALSE"
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal","TRUE"
    45.289999999999999,8356,"Wheeler","Sarah","Portugal","TRUE"
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines","FALSE"
 
``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -filt '(float_col > 0) && (float_col <=100)' -if -filt '(float_col > 0) && (float_col <= 25)' -evlc s:quartile '"first"' -elif -filt '(float_col > 25) && (float_col <= 50)' -evlc quartile '"SECOND"' -elif -filt '(float_col > 50) && (float_col <= 75)' -evlc quartile '"THIRD"' -else -evlc quartile '"FOURTH"' -endif``

* This command filters to make sure only records that have a value in float_col between 0 and 100 continue to be processed. It then creates an -if -elif -else statement that creates the column quartile and gives it the value of FIRST if float column is between 0 and 25, SECOND if float_col is between 25 and 50, THIRD if float_col is between 50 and 75, and FOURTH otherwise. The output is::
 
    "float_col","integer_col","last_name","first_name","country","quartile"
    99.909999999999997,5350,"Lawrence","Lois","Philippines","FOURTH"
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal","THIRD"
    45.289999999999999,8356,"Wheeler","Sarah","Portugal","SECOND"
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines","FIRST"
    
These conditional statements can be used to set values for only certain subsets of your data or set different values for different subsets of your data and are very powerful. 

You should now have a better understanding of the main options used in the aq_pp command and how aq_pp commands should be structured. It is highly recommended that you now review our aq_udb tutorial to learn how to utilize the incredible scability of the Essentia Database.