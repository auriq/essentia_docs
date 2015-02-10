aq_pp Tutorials
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

**The Primary Processing Options:**

- :doc:`aq_pp tutorial` : A full introduction to the preprocessor, ``aq_pp``

**Common Uses for Processing Options:**

- :doc:`combining-datasets` : The main options used to combine datasets in Essentia are ``-cat``, ``-cmb``, and ``-sub``.

  * ``-cat`` combines two datasets by **row**, resulting in a dataset with the every record of its constituent datasets.
  * ``-cmb`` combines two datasets by **column**. The resulting dataset will have all of the columns that were in the input datasets and they will be joined by the columns that they had in common.
  * ``-sub`` combines two datasets by **one column**. The values in that column are compared to the value in a column in the lookup dataset and, if the values match, they are replaced by the values in another column of the lookup dataset.
  
- :doc:`mapping-strings` : ``aq_pp`` provides ``-evlc``, ``-mapf``, ``-mapfrx``, ``-mapc``, ``-map``, and ``maprx`` to help you rearrange your strings. 

  * 
  
- :doc:`variables-and-operations` : ``-var``, (``$RowNum``), (``$FileId``), ``-evlc``, map functions technically, ``-ovar``.
  
- :doc:`filtering-data` : ``-filt``, ``-grep``, ``-if ... -else ... -endif`` statements.