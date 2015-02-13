***************
Data Transforms
***************

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