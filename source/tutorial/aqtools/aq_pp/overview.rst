********
Overview
********

The command structure of aq_pp consists of an **input specification** specifying which file(s) to take the data from,
various **processing specifications** to determine how data is processed, and **output specifications** describing how
and where to put the results of your command.
There are also a variety of global options that modify the environment and default variables used in ``aq_pp``.


This tutorial will emphasize the most commonly used options for aq_pp and how to use them to provide a simple
modification or analysis of the two input files, tutorialdata.csv and lookup.csv.

Input Specifications
====================

First let's create a simple command that **imports** our example file tutorialdata.csv and **defines** its columns.  

``aq_pp -f,+1 tutorialdata.csv -d f:float_col X s,up:last_name s:first_name X``

* ``-f`` specifies the file to operate on (tutorialdata.csv).  It accepts an optional ATTRIBUTE in ``,+1``, which
  means to skip the first line (header in this case)
* ``-d`` defines the column names and types.  The format is t,attribute:name with 't' being the type.  An 'X' means to
  ignore a column.  In this example, we load in a float, force the last name to be an upper case string, and finally
  load in the first_name as is.

Since there are no processing or output specifications given, the the output is simply::

    "float_col","last_name","first_name"
    99.909999999999997,"LAWRENCE","Lois"
    73.609999999999999,"HAMILTON","Evelyn"
    45.289999999999999,"WHEELER","Sarah"
    3.5299999999999998,"KELLEY","Jacqueline"

By default, ``aq_pp`` will validate the input against the type you defined it as.  For instance if a string is seen
in the 'float_col', the program will exit with an error.  By specifying the optional ``eok`` attribute along with
``-f,+1``, the program will simply ignore the input row.  This feature makes it easy to produce validated outout.


There are a number of scenarios (particularly with log data) where merging two different types of files is useful.
If file 1 contains 10 records and two string columns 'A','B' , and file 2 contains 5 records and columns labelled 'B',
'C', we can use ``-cat`` to form a table with 15 records and 3 columns 'A','B','C'.  Columns not existing in the
input data will be assigned with 0 (for numerical) or "" for string data.

However most users will want to JOIN datasets based on common values between two files.  In this case, the first and
last name, as well as the country, are the common columns between the two files.  The ``-cmb`` option is similar to
``-f`` and ``-d`` since it defines the number of lines to skip and the column specification for the second file.
Records will be matched based on all the columns that share the same names between the two files.  For example::

  aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -cmb,+1 lookup.csv
  s:grade f:float_2 s:last_name s:first_name s:country``

    "float_col","integer_col","last_name","first_name","country","grade","float_2"
    99.909999999999997,5350,"Lawrence","Lois","Philippines","A",12.300000000000001
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal","C",96.599999999999994
    45.289999999999999,8356,"Wheeler","Sarah","Portugal","F",89
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines","F",57.600000000000001

Users familiar with SQL will recognize this as an INNER JOIN.  A slight variant with the attributes allows us to JOIN
with REPLACEMENT.  Consider the following::

  aq_pp -f,+1 tutorialdata.csv -d s:float_col f:integer_col s:last_name s:first_name s:country -cmb,+1 lookup.csv
  s,cmb:float_col f,cmb:integer_col s,key:last_name s,key:first_name s,key:country``

    "float_col","integer_col","last_name","first_name","country"
    "A",12.300000000000001,"Lawrence","Lois","Philippines"
    "C",96.599999999999994,"Hamilton","Evelyn","Portugal"
    "F",89,"Wheeler","Sarah","Portugal"
    "F",57.600000000000001,"Kelley","Jacqueline","Philippines"

This is similar to the original JOIN but in this case we replace the columns in the input file with values in
the same columns from the second file designated by the ``,cmb`` attribute.

Process Specifications
======================

The input specification defines all the input columns we have to work with.  The goal of the process spec is to
modify these data according to various rules.

The **creation** of variables is accomplished using the ``-var`` option and their **modification** is typically
handled using the ever-useful ``-evlc`` option with the variable as its argument or its input.

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -var 'f:rolling_sum' 0 -var 'f:record_count' 0 -evlc 'rolling_sum' 'rolling_sum + float_col' -evlc 'record_count' 'record_count + 1' -evlc 'f:rolling_average' 'rolling_sum / record_count'``

* This initializes two new variables: a float called ``rolling_sum`` set to zero and a float called ``record_count``
  set to zero. It then adds the value of float_col to rolling_sum, increases record_count by one, and divides
  rolling_sum by record_count for each record in the input data.
* The variables are not included in the standard output, only the columns are included. The output is::

    "float_col","integer_col","last_name","first_name","country","rolling_average"
    99.909999999999997,5350,"Lawrence","Lois","Philippines",99.909999999999997
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal",86.759999999999991
    45.289999999999999,8356,"Wheeler","Sarah","Portugal",72.936666666666653
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines",55.584999999999994

While defining variables is incredibly useful, ``-evlc`` also has the capability to **create entirely new columns**
or **modify existing ones**. The only change necessary to act on columns is to give ``-evlc`` a column name or column
specification as its argument.


``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -evlc last_name 'first_name + " " + last_name' -evlc integer_col 'float_col * integer_col' -evlc s:mixed_col 'country + " : " + ToS(integer_col)' -c last_name mixed_col``

* This command adds the value of first_name and last_name separated by a space and saves this combined string into
  last_name, overriding the existing value for that record in that column. It then multiplies the float_col by the
  integer_col and saves this product into integer_col, overriding the existing value.
* Finally, it creates a new column called mixed_col that contains the value of country followed by ' : ' and the
  string-converted value of the modified integer_col. It then limits the columns that are output to just the last_name
  and mixed_col columns (see the -o option further on in this documentation). The output is::
 
    "last_name","mixed_col"
    "Lois Lawrence","Philippines : 534518"
    "Evelyn Hamilton","Portugal : 91938"
    "Sarah Wheeler","Portugal : 378443"
    "Jacqueline Kelley","Philippines : 34163"

As you can see, the ``-evlc`` option is incredibly useful since it allows you to create or modify columns based on the
results of an expression. This expression can reference literal values (such as 1 or "a string"), existing columns or
variables, or any of the **default variables** that are built into aq_pp.

One such default variable is ``$RowNum`` which simply keeps track of which record you are streaming from your input
data file. This can be a useful value to add on to your exported data if you might need to reference your input data
later in your analysis.
    
``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -evlc i:actual_row_number '$RowNum + 1'``

* This creates a new integer column called actual_row_number that adds 1 to the value of $RowNum for each record of the
  file. This corrects for the fact that we skipped the header line and thus represents the actual row number from
  tutorialdata.csv. The output is::

    "float_col","integer_col","last_name","first_name","country","actual_row_number"
    99.909999999999997,5350,"Lawrence","Lois","Philippines",2
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal",3
    45.289999999999999,8356,"Wheeler","Sarah","Portugal",4
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines",5
    
Another useful default variable is ``$FileId``. This allows you to keep track of which files your records are coming
from so you can reference those files or group similar records at a later time.

``aq_pp -fileid 5 -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -fileid 6 -cat,+1 lookup.csv s:grade f:float_2 s:last_name s:first_name s:country -evlc s:File_ID '"This record came from file " + ToS($FileId)'``

* This command gives tutorialdata.csv a fileid of 5 and lookup.csv a fileid of 6. It then concatenates
  tutorialdata.csv and lookup.csv together, skipping the top line (header) in each file, and including a column
  describing which file the record came from. The output is::

    "float_col","integer_col","last_name","first_name","country","grade","float_2","File_ID"
    99.909999999999997,5350,"Lawrence","Lois","Philippines",,0,"This record came from file 5"
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal",,0,"This record came from file 5"
    45.289999999999999,8356,"Wheeler","Sarah","Portugal",,0,"This record came from file 5"
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines",,0,"This record came from file 5"
    0,0,"Lawrence","Lois","Philippines","A",12.300000000000001,"This record came from file 6"
    0,0,"Hamilton","Evelyn","Portugal","C",96.599999999999994,"This record came from file 6"
    0,0,"Wheeler","Sarah","Portugal","F",89,"This record came from file 6"
    0,0,"Kelley","Jacqueline","Philippines","F",57.600000000000001,"This record came from file 6"

The expression in ``-evlc`` can use much more than existing columns and previously defined variables. There are also
a variety of **built-in functions** that can only be used in the ``-evlc`` option that allow much more sophisticated
analysis of your data.

See the aq_pp Documentation for a full list and example of these functions. For now I'll introduce the simpler
functions that allow you to find the minumum, maximum, and hash value of various columns.
    
``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -evlc i:minimum 'Min(float_col, integer_col)' -evlc i:maximum 'Max(float_col, integer_col)' -evlc i:hash 'SHash(country)' -c minimum maximum hash``

* This stores the minimum and maximum values of float_col and integer_col into columns minimum and maximum,
  respectively. It then calculates the integer hash value of country and stores it in a column called hash.
* The output columns are then limited to minimum, maximum, and hash. The output is::

    "minimum","maximum","hash"
    99,5350,4213117258
    73,1249,1264705971
    45,8356,1264705971
    3,9678,4213117258

While the ``-evlc`` option is useful when modifying your existing data or creating new data off of it, it does not
easily allow you to **limit which data continues on to the rest of your analysis**.

This is where the ``-filt`` option comes in handy. ``-filt`` makes it easy to limit your data based on their values or
ranges in values of various columns.

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -filt '(country == "Portugal") && (integer_col >= 4000)'``

* This command filters the data so that only records where the country column has a value of "Portugal" and the
  integer_col column is at least 4000 will continue to be analyzed. In this case, only one record passes the filter.
  The output is::
 
    "float_col","integer_col","last_name","first_name","country"
    45.289999999999999,8356,"Wheeler","Sarah","Portugal"

``-evlc`` is incredibly powerful when acting on numerical columns and many of its functions can be useful in processing
string columns, but a lot of analysis needs more advanced parsing and combination of string type columns than ``-evlc`` can provide.

Thus aq_pp contains a variety of mapping functions to **allow values from certain columns to be extracted and
recombined into the same or different columns**. The first two sets of mapping functions are ``-mapf`` and ``-mapc``,
and ``-mapfrx`` and ``-mapc``.

The diffference between these two sets of mapping functions is that the first one uses RT mapping syntax and matches
the entire string everytime, whereas the second uses Regular Expression Syntax and can match either the entire string
or subsets of the string.

``aq_pp -f,+1 tutorialdata.csv -d X X s:last_name s:first_name X -mapf last_name '%%last%%' -mapf first_name '%%first%%' -mapc s:full_name '%%first%% %%last%%'``

* This uses ``-mapf`` to extract the last name **from** the last_name column and store it temporarily as the variable %%last%%. It then extracts the first name from the first_name column and stores it temporarily as the variable %%first%%.
* Finally, it uses ``-mapc`` to define a new string column called full_name and **put** the values of first_name and last_name into it, separated by a space.
 
``aq_pp -f,+1 tutorialdata.csv -d X X s:last_name s:first_name X -mapfrx last_name '.*' -mapfrx first_name '.*' -mapc s:full_name '%%0%% %%1%%'``

* This command instead uses ``-mapfrx`` to match and extract the last name from the last_name column and store it temporarily as the implicit variable %%0%%. It then matches and extracts the first name from the first_name column and stores it temporarily as the implicit variable %%1%%.
* Finally, it again uses ``-mapc`` to define a new string column called full_name that contains the values of first_name and last_name, separated by a space.
 
Both of these commands **extract** data from last_name and first_name and then **put** the values that were in these columns into
a new column containing the full name. Note; however, that the **RegEx based "-mapfrx"** does not have named
placeholders for the extracted data; The placeholders are implicit:

* %%0%% - References the entire match in the first "-mapfrx"; i.e. the entire value in the last_name column.
* %%1%% - References the entire match in the second "-mapfrx"; the entire value in the first_name column.
 
The output of both of these commands is::
 
    "last_name","first_name","full_name"
    "Lawrence","Lois","Lawrence Lois"
    "Hamilton","Evelyn","Hamilton Evelyn"
    "Wheeler","Sarah","Wheeler Sarah"
    "Kelley","Jacqueline","Kelley Jacqueline"

The first two sets of mapping functions allow you to take data from various columns and put them into other columns, however this isnt always necessary. Sometimes, all you want to do is **modify an existing column**. 

This is where you use the second two sets of mapping functions, ``-map`` and ``maprx``. Again, the difference between these two functions are that the former uses RT syntax and the latter uses Regular Expression Syntax.

``aq_pp -f,+1 tutorialdata.csv -d X X X s:first_name X -map first_name '%%first_initial:@nab:1-1%%%*' '%%first_initial%%.'``

* This takes the values in first_name and maps them to the first initial followed by a ".", using the RT mapping function ``-map``. The output is::
 
    "first_name"
    "L."
    "E."
    "S."
    "J."

``aq_pp -f,+1 tutorialdata.csv -d X X X s:first_name X -maprx first_name '^\(.\).*$' '%%1%%.'``

* This command takes the values in first_name and maps them to the first initial followed by a ".", using the RegEx mapping function ``-maprx``. The output is::
 
    "first_name"
    "L."
    "E."
    "S."
    "J."

Mapping allows you to utilize and modify string type columns that are already in your dataset. But what if you want to **replace values of one of the columns in your dataset with values from another dataset**?

This is where you would use ``-sub``. By simply specifying which file contains the values you want to compare your data to and which values you want to replace your data with, you can easily overwrite an existing column with new values. 

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -sub last_name lookup.csv TO X FROM X X``

* This checks whether any values in last_name match any of the values in the third column of lookup.csv and, if they do, replaces those values with the value in the first column of lookup.csv. The output is::
 
    "float_col","integer_col","last_name","first_name","country"
    99.909999999999997,5350,"A","Lois","Philippines"
    73.609999999999999,1249,"C","Evelyn","Portugal"
    45.289999999999999,8356,"F","Sarah","Portugal"
    3.5299999999999998,9678,"F","Jacqueline","Philippines"

A similar task is to do the first half of the ``-sub`` option. That is, comparing values of one of the column in your dataset to those of a column in a different dataset. 

You can accomplish this with the ``-grep`` option, which only requires the file that contains your lookup values and which column in the file contains these lookup values.

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -grep last_name lookup.csv X X FROM X X``

* This command filters the data to include only values in last_name that match any of the values in the third column of lookup.csv. In this case all of the records pass since the last_names are the same in both tutorialdata.csv and lookup.csv. The output is::
 
    "float_col","integer_col","last_name","first_name","country"
    99.909999999999997,5350,"Lawrence","Lois","Philippines"
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal"
    45.289999999999999,8356,"Wheeler","Sarah","Portugal"
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines"


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