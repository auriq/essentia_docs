Filtering Data
============================

In order to perform powerful analysis of your data you need to be able to **limit which data continues on to the rest of your analysis**. 

This is where the ``-filt`` option comes in handy. ``-filt`` makes it easy to limit your data based on their values or ranges in values of various columns.

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -filt '(country == "Portugal") && (integer_col >= 4000)'``

* This command filters the data so that only records where the country column has a value of "Portugal" and the integer_col column is at least 4000 will continue to be analyzed. In this case, only one record passes the filter. The output is::
 
    "float_col","integer_col","last_name","first_name","country"
    45.289999999999999,8356,"Wheeler","Sarah","Portugal"

--------------------------------------------------------------------------------
    
Another option is useful is the ``-grep`` option, which compares the values of one of the columns in your dataset to those of a column in a different dataset. 

To use ``grep``, you only to tell it the file that contains your lookup values and which column in the file contains these lookup values.

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -grep last_name lookup.csv X X FROM X X``

* This command filters the data to include only values in last_name that match any of the values in the third column of lookup.csv. In this case all of the records pass since the last_names are the same in both tutorialdata.csv and lookup.csv. The output is::
 
    "float_col","integer_col","last_name","first_name","country"
    99.909999999999997,5350,"Lawrence","Lois","Philippines"
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal"
    45.289999999999999,8356,"Wheeler","Sarah","Portugal"
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines"

--------------------------------------------------------------------------------
    
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