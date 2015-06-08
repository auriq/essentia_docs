***********************
Example aq_udb Commands
***********************


**Required Files**


This tutorial assumes you already imported the following data into udb::

    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Portugal","Hamilton","Evelyn",1249,73.609999999999999,0,,
    "Portugal","Wheeler","Sarah",8356,45.289999999999999,0,,
    "Portugal","Hamilton","Evelyn",0,0,96.599999999999994,"C",
    "Portugal","Wheeler","Sarah",0,0,89,"F",
    "Philippines","Lawrence","Lois",5350,99.909999999999997,0,,
    "Philippines","Kelley","Jacqueline",9678,3.5299999999999998,0,,
    "Philippines","Lawrence","Lois",0,0,12.300000000000001,"A",
    "Philippines","Kelley","Jacqueline",0,0,57.600000000000001,"F",

This data was imported using aq_pp and the example data provided in the aq_pp documentation. To get this data imported you can run the following commands::

    ess spec create database my_database --ports=1
    ess spec create vector country_vector "s,hash:country s,+first:last_name s,+first:first_name i,+add:integer_col f,+max:float_col f,+min:float_2 s:grade s:extra_column"
    ess spec create table country_table "s,hash:country s:last_name s:first_name i:integer_col f:float_col f:float_2 s:grade s:extra_column"
    ess spec create variable "i:defined_integer_var s:defined_string_var"
    ess udbd start
    aq_pp -f,+1 exampledata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -ddef -udb_imp my_database:country_table
    aq_pp -f,+1 lookup.csv -d s:grade f:float_2 s:last_name s:first_name s:country -ddef -udb_imp my_database:country_table



**Overview**


aq_udb is how Essentia interacts with the Udb database. It specializes in exporting data from the database, providing quick counts or otherwise pre-processing the data, and then outputting the results to wherever you may need them. 

The command structure of aq_udb consists of a global specification specifying which database to export the data from, 
various export specifications to determine how the data is modified and where the output is sent, and an optional output specification describing how to order the data in the output.

For a full list and description of the available options, see the aq_udb Documentation.

This tutorial will emphasize the most commonly used options for aq_udb and how to use them to provide a simple modification or analysis of the data in the example data in the udb database. These options are:

* **Global Specification:** -db.
* **Export Specifications:** -exp, -cnt, -exp_usr, -cnt_usr, -lim_usr, -lim_rec, -var, -pp, -filt, -eval, -bvar, -filt, -o, -c, -notitle, and -sort.
* **Order Specification:** -ord.



**Global Specifications**


Udb can contain many databases each with its own data being stored in it and its own attributes being applied to that data. The first necessary step when exporting data from Udb is to specify **which specific database you want to export the data from**. 

This is accomplished with the -db option.

``aq_udb -db my_database -exp country_table``

* This command sets the database to my_database and then exports the table country_table. The output is::

    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Portugal","Hamilton","Evelyn",1249,73.609999999999999,0,,
    "Portugal","Wheeler","Sarah",8356,45.289999999999999,0,,
    "Portugal","Hamilton","Evelyn",0,0,96.599999999999994,"C",
    "Portugal","Wheeler","Sarah",0,0,89,"F",
    "Philippines","Lawrence","Lois",5350,99.909999999999997,0,,
    "Philippines","Kelley","Jacqueline",9678,3.5299999999999998,0,,
    "Philippines","Lawrence","Lois",0,0,12.300000000000001,"A",
    "Philippines","Kelley","Jacqueline",0,0,57.600000000000001,"F",



**Export Specifications**


The next step is to actually export the data from your database using the ``-exp`` option. This will take **all** of the data from the table or vector in the database you specify and stream it into the rest of your export specifications or into your output. 

For simplicity, you can include which database to pull the data from in this option by adding the database name followed by a ``:`` before your table or vector name.

``aq_udb -exp my_database:country_table``

* This **exports** the table country_table from my_database. The output is::
 
    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Portugal","Hamilton","Evelyn",1249,73.609999999999999,0,,
    "Portugal","Wheeler","Sarah",8356,45.289999999999999,0,,
    "Portugal","Hamilton","Evelyn",0,0,96.599999999999994,"C",
    "Portugal","Wheeler","Sarah",0,0,89,"F",
    "Philippines","Lawrence","Lois",5350,99.909999999999997,0,,
    "Philippines","Kelley","Jacqueline",9678,3.5299999999999998,0,,
    "Philippines","Lawrence","Lois",0,0,12.300000000000001,"A",
    "Philippines","Kelley","Jacqueline",0,0,57.600000000000001,"F",

You can also produce a simple **count** of the number of records and unique values in the table or vector using the ``-cnt`` option. 

``aq_udb -cnt my_database:country_table``

* This command counts the number of rows and the number of unique values in the primary_key column (country in this case) in country_table from my_database and outputs the results to standard out. The output is::
 
    "field","count"
    "pkey",2
    "row",8

There may be times when you dont want just the number of unique values in your table or vector but the **actual values** themselves. This is what ``-exp_user`` is for.

``aq_udb -db my_database -exp_usr``

* This sets database to my_database and exports the unique values in the primary_key column (country in this case). The output is::
    
    "pkey"
    "Portugal"
    "Philippines"

If you want just the **number of unique values** in your table or vector, a simple way to get it is with ``-cnt_usr``.

``aq_udb -db my_database -cnt_usr``

* Sets database to my_database and counts the number of unique values in the primary_key column (country in this case). The output is::
    
    "field","count"
    "pkey",2
    
To **limit the number of unique users** in your output, use the ``-lim_usr`` option.

``aq_udb -exp my_database:country_table -lim_usr 1``

* This command exports country_table from my_database and limits the number of unique users output to 1. The output is::
    
    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Portugal","Hamilton","Evelyn",1249,73.609999999999999,0,,"476707713"
    "Portugal","Wheeler","Sarah",8356,45.289999999999999,0,,"1186278907"
    "Portugal","Hamilton","Evelyn",0,0,96.599999999999994,"C","505671508"
    "Portugal","Wheeler","Sarah",0,0,89,"F","2137716191"

You can similarly **limit the number of records** in your output by including the ``-lim_rec`` option.

``aq_udb -exp my_database:country_table -lim_rec 6``

* This exports country_table from my_database and limits the number of records output to 6. The output is::
    
    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Portugal","Hamilton","Evelyn",1249,73.609999999999999,0,,"476707713"
    "Portugal","Wheeler","Sarah",8356,45.289999999999999,0,,"1186278907"
    "Portugal","Hamilton","Evelyn",0,0,96.599999999999994,"C","505671508"
    "Portugal","Wheeler","Sarah",0,0,89,"F","2137716191"
    "Philippines","Lawrence","Lois",5350,99.909999999999997,0,,"936145377"
    "Philippines","Kelley","Jacqueline",9678,3.5299999999999998,0,,"1215825599"
    
You can also use ``-var`` to define **global variables** just as you could in aq_pp; however, in order to process that variable or any of your other exported data you need to define a ``-pp`` group.

This ``-pp`` group specifies which table or vector you want to process and you use a series of ``-eval``, ``-bvar``, and ``-filt`` rules to modify it.

You can have multiple groups and each group can have multiple rules so you can form extremely powerful **processing chains** by stringing these groups and rules together.

With a single variable definition followed by a single ``-pp`` group and two simple ``-eval`` rules you can easily enter meaningful values into the extra column we have in my_database.

``aq_udb -db my_database -exp country_table -var defined_integer_var 0 -pp country_table -eval defined_integer_var 'defined_integer_var + 1' -eval extra_column '"Row : " + ToS(defined_integer_var)' -endpp``

* This command exports country_table from my_database and initializes the previously defined variable to 0. It then establishes a pp (pre-processing) group for country_table. 
* For each record in the table, it increases the variable defined_integer_var by 1 and stores that value preceded by 'Row : ' in extra_column as a string. The output is::
    
    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Portugal","Hamilton","Evelyn",1249,73.609999999999999,0,,"Row : 1"
    "Portugal","Wheeler","Sarah",8356,45.289999999999999,0,,"Row : 2"
    "Portugal","Hamilton","Evelyn",0,0,96.599999999999994,"C","Row : 3"
    "Portugal","Wheeler","Sarah",0,0,89,"F","Row : 4"
    "Philippines","Lawrence","Lois",5350,99.909999999999997,0,,"Row : 5"
    "Philippines","Kelley","Jacqueline",9678,3.5299999999999998,0,,"Row : 6"
    "Philippines","Lawrence","Lois",0,0,12.300000000000001,"A","Row : 7"
    "Philippines","Kelley","Jacqueline",0,0,57.600000000000001,"F","Row : 8"

A pp group can also have its own **local variable** using ``-bvar``. This allows the variable to be defined and modified only within the pp group, enabling a command very similar to the one we just ran but with a slighly different output.

``aq_udb -db my_database -exp country_table -pp country_table -bvar defined_integer_var 0 -eval defined_integer_var 'defined_integer_var + 1' -eval extra_column '"Row : " + ToS(defined_integer_var)' -endpp``

* This exports country_table from my_database and establishes a pp (pre-processing) group for country_table. 
* For each record in a bucket in the table, it increases the variable defined_integer_var by 1 and stores that value preceded by 'Row : ' in extra_column as a string. The output is::
 
    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Portugal","Hamilton","Evelyn",1249,73.609999999999999,0,,"Row : 1"
    "Portugal","Wheeler","Sarah",8356,45.289999999999999,0,,"Row : 2"
    "Portugal","Hamilton","Evelyn",0,0,96.599999999999994,"C","Row : 3"
    "Portugal","Wheeler","Sarah",0,0,89,"F","Row : 4"
    "Philippines","Lawrence","Lois",5350,99.909999999999997,0,,"Row : 1"
    "Philippines","Kelley","Jacqueline",9678,3.5299999999999998,0,,"Row : 2"
    "Philippines","Lawrence","Lois",0,0,12.300000000000001,"A","Row : 3"
    "Philippines","Kelley","Jacqueline",0,0,57.600000000000001,"F","Row : 4"

As you can see, the variable defined_integer_var was reset to 0 when the pp group got to a record that had a different unique value for the primary key (a different bucket, as we sometimes call them).

``aq_udb -db my_database -exp country_table -if -filt 'PatCmp(last_name, "^H.*$", "ncas,rx")' -eval extra_column '"This record belongs to a user with a last name starting with h"' -else -eval extra_column '"The record does not"' -endif``
    
.. .. Every pp rule in a pp group can also use action codes to tell aq_udb how to proceed when an evaluated expression in the pp rule is successful and what to do when its unsuccessful.

.. .. Action codes are letters or numbers following any pp rule as a comma-separated attribute, and tell aq_udb **whether and how far it should move forward in the processing chain** when the expression is successful and in the case it is unsuccessful.

 * This exports country_table from my_database and then establishes a pp (pre-processing) group for country_table. 
 * For each record, this command uses a globular pattern comparison to check whether the value in the last_name column begins with an 'h'. If it does, the next pp rule is run (the first ``-eval``) and a value of 'This record belongs to a user with a last name starting with h' is assigned to extra_column. 
 * If it does not, the next pp rule is skipped and the following pp rule is run instead (another ``-eval``). This second pp rule gives extra_column a value of 'The record does not'. The output is::

    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Portugal","Hamilton","Evelyn",1249,73.609999999999999,0,,"This record belongs to a user with a last name starting with h"
    "Portugal","Wheeler","Sarah",8356,45.289999999999999,0,,"The record does not"
    "Portugal","Hamilton","Evelyn",0,0,96.599999999999994,"C","This record belongs to a user with a last name starting with h"
    "Portugal","Wheeler","Sarah",0,0,89,"F","The record does not"
    "Philippines","Lawrence","Lois",5350,99.909999999999997,0,,"The record does not"
    "Philippines","Kelley","Jacqueline",9678,3.5299999999999998,0,,"The record does not"
    "Philippines","Lawrence","Lois",0,0,12.300000000000001,"A","The record does not"
    "Philippines","Kelley","Jacqueline",0,0,57.600000000000001,"F","The record does not"
            
While filtering record by record with ``-filt`` is useful, sometimes you just want to **filter the entire set of exported data**. 

``aq_udb`` includes a ``-filt`` option identical to the one in ``aq_pp`` to provide an easy way to limit the data sent to your output.

``aq_udb -db my_database -exp country_table -filt 'PatCmp(last_name, "^H.*$", "ncas,rx")'``

* This command exports country_table from my_database and limits the output to only records that have an 'h' as the first letter in last_name. The output is::
    
    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Portugal","Hamilton","Evelyn",1249,73.609999999999999,0,,
    "Portugal","Hamilton","Evelyn",0,0,96.599999999999994,"C",

Just as in aq_pp, you can save your results to a file or output to standard out.

``aq_udb -db my_database -exp country_table -o -``

* This exports country_table from my_database and sends the output to standard out. The output is::
    
    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Portugal","Hamilton","Evelyn",1249,73.609999999999999,0,,
    "Portugal","Wheeler","Sarah",8356,45.289999999999999,0,,
    "Portugal","Hamilton","Evelyn",0,0,96.599999999999994,"C",
    "Portugal","Wheeler","Sarah",0,0,89,"F",
    "Philippines","Lawrence","Lois",5350,99.909999999999997,0,,
    "Philippines","Kelley","Jacqueline",9678,3.5299999999999998,0,,
    "Philippines","Lawrence","Lois",0,0,12.300000000000001,"A",
    "Philippines","Kelley","Jacqueline",0,0,57.600000000000001,"F",

You can also limit which columns are sent to the output.

``aq_udb -db my_database -exp country_table -c country last_name first_name``

* This command exports country_table from my_database and outputs to standard out. It then limits the output columns to just country, last_name, and first_name. The output is::
    
    "country","last_name","first_name"
    "Portugal","Hamilton","Evelyn"
    "Portugal","Wheeler","Sarah"
    "Portugal","Hamilton","Evelyn"
    "Portugal","Wheeler","Sarah"
    "Philippines","Lawrence","Lois"
    "Philippines","Kelley","Jacqueline"
    "Philippines","Lawrence","Lois"
    "Philippines","Kelley","Jacqueline"

If you want your output without the header line, you can remove it with ``-notitle``.

``aq_udb -db my_database -exp country_table -c country last_name first_name -notitle``

* This exports country_table from my_database and outputs to standard out. It limits the output columns to just country, last_name, and first_name. 
* The ``-notitle`` option then tells aq_pp not to include a header line in the output. The output is::
    
    "Portugal","Hamilton","Evelyn"
    "Portugal","Wheeler","Sarah"
    "Portugal","Hamilton","Evelyn"
    "Portugal","Wheeler","Sarah"
    "Philippines","Lawrence","Lois"
    "Philippines","Kelley","Jacqueline"
    "Philippines","Lawrence","Lois"
    "Philippines","Kelley","Jacqueline"

Many analyses need the results ordered by the values in a single column instead of the random output of grouping by unique hash value. 

You can use the ``-sort`` option to **sort the exported data by an existing column** so that the output contains the results in the correct order. 

``aq_udb -db my_database -exp country_table -sort country``

* This command exports country_table from my_database and orders the output rows by their values in the country column. The output is::
    
    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Philippines","Lawrence","Lois",5350,99.909999999999997,0,,
    "Philippines","Kelley","Jacqueline",9678,3.5299999999999998,0,,
    "Philippines","Lawrence","Lois",0,0,12.300000000000001,"A",
    "Philippines","Kelley","Jacqueline",0,0,57.600000000000001,"F",
    "Portugal","Hamilton","Evelyn",1249,73.609999999999999,0,,
    "Portugal","Wheeler","Sarah",8356,45.289999999999999,0,,
    "Portugal","Hamilton","Evelyn",0,0,96.599999999999994,"C",
    "Portugal","Wheeler","Sarah",0,0,89,"F",

The column you sort by can be **any of the existing columns** in the exported table or vector.

``aq_udb -db my_database -exp country_table -sort last_name``

* This exports country_table from my_database and orders the output rows by their values in the last_name column. The output is::
    
    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Portugal","Hamilton","Evelyn",1249,73.609999999999999,0,,
    "Portugal","Hamilton","Evelyn",0,0,96.599999999999994,"C",
    "Philippines","Kelley","Jacqueline",9678,3.5299999999999998,0,,
    "Philippines","Kelley","Jacqueline",0,0,57.600000000000001,"F",
    "Philippines","Lawrence","Lois",5350,99.909999999999997,0,,
    "Philippines","Lawrence","Lois",0,0,12.300000000000001,"A",
    "Portugal","Wheeler","Sarah",8356,45.289999999999999,0,,
    "Portugal","Wheeler","Sarah",0,0,89,"F",

The ``-sort`` option also includes **sub options** that allow you to change the direction in which values are ordered (ascending is the default) and the number of records included in the output.

``aq_udb -db my_database -exp country_table -sort last_name -dec -top 5``

* This command exports country_table from my_database and orders the output rows by their values in the country column in descending order (Z's to A's, reverse alphabetical). 
* It also limits the number of output records to 5. The output is::
    
    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Portugal","Wheeler","Sarah",0,0,89,"F",
    "Portugal","Wheeler","Sarah",8356,45.289999999999999,0,,
    "Philippines","Lawrence","Lois",0,0,12.300000000000001,"A",
    "Philippines","Lawrence","Lois",5350,99.909999999999997,0,,
    "Philippines","Kelley","Jacqueline",0,0,57.600000000000001,"F",
    
A final useful feature of aq_pp is its ability to order the records by their values in a single column within the table or vector itself. 

Thus the data that is being stored is modified and **sorted within the database** using the ``-ord`` option.
    
``aq_udb -db my_database -ord country_table last_name``       ## then run

``aq_udb -db my_database -exp country_table``

* The first statement orders country_table from my_database by last_name. This ordering occurs internally in the udb database and does not output anything to standard out. 
* The second bash statement exports the newly-ordered country_table from my database to standard output. The output of this statement is::
    
    "country","last_name","first_name","integer_col","float_col","float_2","grade","extra_column"
    "Portugal","Hamilton","Evelyn",1249,73.609999999999999,0,,
    "Portugal","Hamilton","Evelyn",0,0,96.599999999999994,"C",
    "Portugal","Wheeler","Sarah",8356,45.289999999999999,0,,
    "Portugal","Wheeler","Sarah",0,0,89,"F",
    "Philippines","Kelley","Jacqueline",9678,3.5299999999999998,0,,
    "Philippines","Kelley","Jacqueline",0,0,57.600000000000001,"F",
    "Philippines","Lawrence","Lois",5350,99.909999999999997,0,,
    "Philippines","Lawrence","Lois",0,0,12.300000000000001,"A",
    
As you can see, the data was sorted by its values in the last_name column for each unique value of the primary key column (country). 

You should now have a greater understanding of the structure of the aq_udb command and its commonly-used options. To
see how to use the higher level Essentia commands please review the `Data Classification <http://www.auriq.com/documentation/source/tutorial/data_organization.html>`_ Tutorial.