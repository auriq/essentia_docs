Variables and Operations
============================

--------------------------------------------------------------------------------

A very useful feature of aq_pp is the ability to **define, store, and modify variables**. 

The **creation** of variables is accomplished using the ``-var`` option and their **modification** is typically handled using the ever-useful ``-evlc`` option with the variable as its argument or its input.

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -var 'f:rolling_sum' 0 -var 'f:record_count' 0 -evlc 'rolling_sum' 'rolling_sum + float_col' -evlc 'record_count' 'record_count + 1' -evlc 'f:rolling_average' 'rolling_sum / record_count'``

* This initializes two new variables: a float called ``rolling_sum`` set to zero and a float called ``record_count`` set to zero. It then adds the value of float_col to rolling_sum, increases record_count by one, and divides rolling_sum by record_count for each record in the input data. 
* The variables are not included in the standard output, only the columns are included. The output is::

    "float_col","integer_col","last_name","first_name","country","rolling_average"
    99.909999999999997,5350,"Lawrence","Lois","Philippines",99.909999999999997
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal",86.759999999999991
    45.289999999999999,8356,"Wheeler","Sarah","Portugal",72.936666666666653
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines",55.584999999999994

\ 

As you can see, the ``-evlc`` option is incredibly useful since it allows you to create or modify columns or variables based on the results of an expression. This expression can reference literal values (such as 1 or "a string"), existing columns or variables, or any of the **default variables** that are built into aq_pp. 

One such default variable is ``$RowNum`` which simply keeps track of which record you are streaming from your input data file. This can be a useful value to add on to your exported data if you might need to reference your input data later in your analysis.
    
``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -evlc i:actual_row_number '$RowNum + 1'``

* This creates a new integer column called actual_row_number that adds 1 to the value of ``$RowNum`` for each record of the file. This corrects for the fact that we skipped the header line and thus represents the actual row number from tutorialdata.csv. The output is::

    "float_col","integer_col","last_name","first_name","country","actual_row_number"
    99.909999999999997,5350,"Lawrence","Lois","Philippines",2
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal",3
    45.289999999999999,8356,"Wheeler","Sarah","Portugal",4
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines",5
    
Another useful default variable is ``$FileId``. This allows you to keep track of which files your records are coming from so you can reference those files or group similar records at a later time. 

``aq_pp -fileid 5 -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -fileid 6 -cat,+1 lookup.csv s:grade f:float_2 s:last_name s:first_name s:country -evlc s:File_ID '"This record came from file " + ToS($FileId)'``

* This command gives tutorialdata.csv a fileid of 5 and lookup.csv a fileid of 6. It then concatenates tutorialdata.csv and lookup.csv together, skipping the top line (header) in each file, and including a column describing which file the record came from. The output is::

    "float_col","integer_col","last_name","first_name","country","grade","float_2","File_ID"
    99.909999999999997,5350,"Lawrence","Lois","Philippines",,0,"This record came from file 5"
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal",,0,"This record came from file 5"
    45.289999999999999,8356,"Wheeler","Sarah","Portugal",,0,"This record came from file 5"
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines",,0,"This record came from file 5"
    0,0,"Lawrence","Lois","Philippines","A",12.300000000000001,"This record came from file 6"
    0,0,"Hamilton","Evelyn","Portugal","C",96.599999999999994,"This record came from file 6"
    0,0,"Wheeler","Sarah","Portugal","F",89,"This record came from file 6"
    0,0,"Kelley","Jacqueline","Philippines","F",57.600000000000001,"This record came from file 6"

--------------------------------------------------------------------------------    

``-evlc`` is incredibly powerful when acting on numerical columns and many of its functions can be useful in processing string columns, but a lot of analysis needs more advanced parsing and combination of string type columns than ``-evlc`` can provide. 

Thus aq_pp contains a variety of mapping functions to **allow values from certain columns to be extracted and recombined into the same or different columns**. The first two sets of mapping functions are ``-mapf`` and ``-mapc``, and ``-mapfrx`` and ``-mapc``.

The diffference between these two sets of mapping functions is that the first one uses RT mapping syntax and matches the entire string everytime, whereas the second uses Regular Expression Syntax and can match either the entire string or subsets of the string.

RT mapping syntax allows you to define your own variables in the extraction string pattern, whereas Regular Expression mapping syntax defines variables ``%%0%%`` to ``%%n%%`` implicitly based on the number and order of matches in your extraction pattern.

``aq_pp -f,+1 tutorialdata.csv -d X X s:last_name s:first_name X -mapf last_name '%%last%%' -mapf first_name '%%first%%' -mapc s:full_name '%%first%% %%last%%'``

* This uses ``-mapf`` to extract the last name **from** the last_name column and store it temporarily as the variable ``%%last%%``. It then extracts the first name from the first_name column and stores it temporarily as the variable ``%%first%%``.
* Finally, it uses ``-mapc`` to define a new string column called full_name and **put** the values of first_name and last_name into it, separated by a space.
 
``aq_pp -f,+1 tutorialdata.csv -d X X s:last_name s:first_name X -mapfrx last_name '.*' -mapfrx first_name '.*' -mapc s:full_name '%%0%% %%1%%'``

* This command instead uses ``-mapfrx`` to match and extract the last name from the last_name column and store it temporarily as the implicit variable ``%%0%%``. It then matches and extracts the first name from the first_name column and stores it temporarily as the implicit variable ``%%1%%``.
* Finally, it again uses ``-mapc`` to define a new string column called full_name that contains the values of first_name and last_name, separated by a space.
 
Both of these commands **extract** data from last_name and first_name and then **put** the values that were in these columns into
a new column containing the full name. Note; however, that the **RegEx based "-mapfrx"** does not have named
variables for the extracted data; The variables are implicit:

* %%0%% - References the entire match in the first "-mapfrx"; i.e. the entire value in the last_name column.
* %%1%% - References the entire match in the second "-mapfrx"; the entire value in the first_name column.
 
The output of both of these commands is::
 
    "last_name","first_name","full_name"
    "Lawrence","Lois","Lawrence Lois"
    "Hamilton","Evelyn","Hamilton Evelyn"
    "Wheeler","Sarah","Wheeler Sarah"
    "Kelley","Jacqueline","Kelley Jacqueline"

--------------------------------------------------------------------------------

The first two sets of mapping functions allow you to take data from various columns and put them into other columns, however this isnt always necessary. Sometimes, all you want to do is **modify an existing column**. 

This is where you use the second two sets of mapping functions, ``-map`` and ``maprx``. Again, the difference between these two functions are that the former uses RT syntax and the latter uses Regular Expression Syntax.

``aq_pp -f,+1 tutorialdata.csv -d X X X s:first_name X -map first_name '%%first_initial:@nab:1-1%%%*' '%%first_initial%%.'``

* This takes the values in first_name and maps them to the first initial followed by a ".", using the RT mapping function ``-map`` and a map variable ``%%first_initial%%``. The output is::
 
    "first_name"
    "L."
    "E."
    "S."
    "J."

``aq_pp -f,+1 tutorialdata.csv -d X X X s:first_name X -maprx first_name '^\(.\).*$' '%%1%%.'``

* This command takes the values in first_name and maps them to the first initial followed by a ".", using the RegEx mapping function ``-maprx`` and the implicit variable ``%%1%%`` defined as the first match in the given extraction pattern. The output is::
 
    "first_name"
    "L."
    "E."
    "S."
    "J."

--------------------------------------------------------------------------------
    
To **only output the variables** you've defined and modified in your previous analysis, you need to use the ``-ovar`` option.

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -var 'f:rolling_sum' 0 -var 'f:record_count' 0 -evlc 'rolling_sum' 'rolling_sum + float_col' -evlc 'record_count' 'record_count + 1' -evlc 'f:rolling_average' 'rolling_sum / record_count' -ovar -``

* This command initializes two new variables: a float called ``rolling_sum`` set to zero and a float called ``record_count`` set to zero. It then adds the value of float_col to rolling_sum, increases record_count by one, and divides rolling_sum by record_count for each record in the input data. 
* The **columns are not included** in the standard output, **only the variables are included**. The output is::
 
    "rolling_sum","record_count"
    222.33999999999997,4