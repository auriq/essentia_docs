How to Use aq_pp
--------------------------

--------------------------------------------------------------------------------

**Required Files**

These tutorials use the *first five lines* of `tutorialdata.csv <https://s3.amazonaws.com/asi-public/etldata/fivecoltutorial.csv>`_. To run these commands, copy the following five lines and save them as tutorialdata.csv::

    float-col,integer-col,last-name,first-name,country
    99.91,5350,Lawrence,Lois,Philippines
    73.61,1249,Hamilton,Evelyn,Portugal
    45.29,8356,Wheeler,Sarah,Portugal
    3.53,9678,Kelley,Jacqueline,Philippines

These tutorials will also use a lookup file to compare values to. If you want to run these commands, copy the following five lines and save them as lookup.csv::

    grade,float_2,last_name,first-name,country
    A,12.3,Lawrence,Lois,Philippines
    C,96.6,Hamilton,Evelyn,Portugal
    F,89.0,Wheeler,Sarah,Portugal
    F,57.6,Kelley,Jacqueline,Philippines

\ 

--------------------------------------------------------------------------------

**Preamble:**

- :doc:`the-benefit-of-using-aq_pp` : A brief use case demonstrating why you should use ``aq_pp``.

**The Primary Processing Options:**

- :doc:`aq_pp tutorial` : A full introduction to the preprocessor, ``aq_pp``.

**Common Uses for Processing Options:**

- :doc:`combining-datasets` : The main options used to combine datasets in Essentia are ``-cat``, ``-cmb``, and ``-sub``.

  * ``-cat`` combines two datasets by **row**, resulting in a dataset with the every record of its constituent datasets.
  * ``-cmb`` combines two datasets by **column**. The resulting dataset will have all of the columns that were in the input datasets and they will be joined by the columns that they had in common.
  * ``-sub`` combines two datasets by **one column**. The values in that column are compared to the value in a column in the lookup dataset and, if the values match, they are replaced by the values in another column of the lookup dataset.
  
- :doc:`mapping-strings` : ``aq_pp`` provides ``-evlc``, ``-mapf``, ``-mapfrx``, ``-mapc``, ``-map``, and ``maprx`` to help you rearrange any string data. 

  * ``-evlc`` can create or modify entire columns or even change the type of a column (say if a string actually just contained a quoted number and you wanted to extract that number as a float). 
  * ``-mapf`` and ``-mapc`` allow you to extract some or all of the data from one or more columns and put that data into another column or columns. 
  * ``-mapfrx`` and ``-mapc`` does that same as ``-mapf`` and ``-mapc`` but uses Regular Expression syntax, allowing you to form powerful pattern matching steps that extract a very specific portion or portions of the data. 
  * ``-map`` and ``-maprx`` extract the data similarly to the two sets of map functions above (``-maprx`` uses Regular Expression syntax), but act on only one column at a time. This allows simpler modification of data in a single string column. 
  
- :doc:`variables-and-operations` : The ``-var``, ``-evlc``, map, and ``-ovar`` options all work with variables.

  * ``-var`` allows you to defined new varibles and set their defauult value.
  * ``-evlc`` lets you modify existing variables and use them as part of your processing expression.
  * The map options contain variables in their extraction pattern strings that can be used to insert the values they contain into another column or columns.
  * ``-ovar`` limits the output to only include the variables you've defined and not the columns from the data.
  
- :doc:`filtering-data` : ``-filt``, ``-grep``, and ``-if ... -else ... -endif`` statements all let you control which data is processed.

  * ``-filt`` is the main filtering option and allows you to limit which data continues to be processed based on the results of the condition you define.
  * ``-grep`` compares the values of column from the input dataset against the values of a column in a lookup dataset. It only lets each record continue in the processing chain if the value of the specified column was present in both datasets.
  * ``-if ... -else ... -endif`` statements allow you to use many of the other options in ``aq_pp`` to create conditional expressions that each record is subject to. 