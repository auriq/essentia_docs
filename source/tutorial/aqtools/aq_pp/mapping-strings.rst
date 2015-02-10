Mapping Strings
==================

--------------------------------------------------------------------------------

``-evlc`` has the capability to create entirely new columns or modify existing ones. To act on columns, you need to to give ``-evlc`` a column name or column specification as its argument.

The difference between a column name and a column specification is that a column name is the name of an existing column whereas a column specification is the type you want the new column to be followed by a ``:`` and the name of the new column.

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -evlc last_name 'first_name + " " + last_name' -evlc integer_col 'float_col * integer_col' -evlc s:mixed_col 'country + " : " + ToS(integer_col)' -c last_name mixed_col``

* This command adds the value of first_name and last_name separated by a space and saves this combined string into last_name, overriding the existing value for that record in that column. It then multiplies the float_col by the integer_col and saves this product into integer_col, overriding the existing value. 
* Finally, it creates a new column called mixed_col that contains the value of country followed by ' : ' and the string-converted value of the modified integer_col. It then limits the columns that are output to just the last_name and mixed_col columns (see the -o option further on in this documentation). The output is::
 
    "last_name","mixed_col"
    "Lois Lawrence","Philippines : 534518"
    "Evelyn Hamilton","Portugal : 91938"
    "Sarah Wheeler","Portugal : 378443"
    "Jacqueline Kelley","Philippines : 34163"
    
--------------------------------------------------------------------------------
    
While ``-evlc`` is incredibly powerful when acting on numerical columns and many of its functions can be useful in processing string columns, a lot of analysis needs more advanced parsing and combination of string type columns than ``-evlc`` can provide. 

Thus aq_pp contains a variety of mapping functions to **allow values from certain columns to be extracted and recombined into the same or different columns**. The first two sets of mapping functions are ``-mapf`` and ``-mapc``, and ``-mapfrx`` and ``-mapc``.

The diffference between these two sets of mapping functions is that the first one uses RT mapping syntax and matches the entire string everytime, whereas the second uses Regular Expression Syntax and can match either the entire string or subsets of the string.

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
    
--------------------------------------------------------------------------------

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