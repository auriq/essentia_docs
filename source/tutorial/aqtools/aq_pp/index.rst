:tocdepth: 3

*****
aq_pp
*****

The Benefit of Using ``aq_pp``
==============================

To demonstrate the utility of ``aq_pp``, lets look at the following problem:

We have sales data from a fictional store that caters to international clients.  We record the amount spent for each
purchase and the currency it was purchased with.  We wish to compute the total sales in US Dollars.
We have 2 files to process.  The first contains the time, currency type, and amount spent, and the second is a lookup
table that has the country code and USD exchange rate:

sales data::

   transaction_date,currency,amount
   2013-08-01T07:50:00,USD,81.39
   2013-08-01T08:22:00,USD,47.96
   2013-08-01T08:36:00,CAD,62.59

exchange data::

   currency,rate
   EUR,1.34392
   CAD,0.91606
   USD,1.00000

Lets compare 2 solutions against ``aq_pp``

**SQL**::

  select ROUND(sum(sales.amount*money.rate),2) AS total from sales INNER JOIN exchange ON sales.currency = exchange.currency;

SQL is straightforward and generally easy to understand.  It will execute this query very quickly,
but this overlooks the hassle of actually importing it into the database.

**AWK**::

  awk 'BEGIN {FS=","} NR==1 { next } FNR==NR { a[$1]=$2; next } $2 in a { $2=a[$2]; sum += $2*$3} END {print sum}' exchange.csv sales.csv

AWK is an extremely powerful text processing language, and has been a part of Unix for about 40 years.  This legacy
means that it is stress tested and has a large user base.  But it is also not very user friendly in some
circumstances.  The language
complexity scales with the difficulty of the problem you are trying to solve.  Also, referencing the columns by
positional identifiers ($1, $2 etc) makes AWK code more challenging to develop and maintain.


**AQ_PP**::

  aq_pp -f,+1 sales.csv -d s:date s:currency f:amount -cmb,+1 exchange.csv s:currency f:rate -var f:sum 0.0 -evlc 'sum' 'sum+(amount*rate)' -ovar -

The AuriQ preprocessor is similar in spirit to AWK, but it simplifies many issues.
We'll detail the specifics in the rest of the documentation, but even without knowing all of the syntax, the
intent of the command is fairly easy to discern. Instead of positional arguments, columns
are named, therefore making an ``aq_pp`` command more human readable.
Additionally, it is very fast, in fact an order of magnitude faster in this example.

In the documentation that follows, we will expand on how this and other Essentia tools can simplify and empower your
data processing workflow.

Required Files
==============

These tutorials require a few small files: :download:`chemistry.csv` and :download:`physics.csv` contain
fictional grades from two college courses.  We limit the number of students to just a few in order to make the
tutorial more clear. :download:`grades.csv` contains a lookup table that maps letter grades to a 'PASS/FAIL'
designation.


Tutorials
---------



- :doc:`overview` : Getting acquainted with ``aq_pp``.
- :doc:`combining-datasets` : Joins and lookup tables with ``aq_pp``.

  * ``-cat`` combines two datasets by **row**, resulting in a dataset with the every record of its constituent datasets.
  * ``-cmb`` combines two datasets by **column**. The resulting dataset will have all of the columns that were in the
    input datasets and they will be joined by the columns that they had in common.
  * ``-sub`` combines two datasets by **one column**. The values in that column are compared to the value in a column
    in the lookup dataset and, if the values match, they are replaced by the values in another column of the lookup
    dataset.
  
- :doc:`data-transform` : Math and string operations on input data.

  * ``-evlc`` can create or modify entire columns or even change the type of a column (say if a string actually just
    contained a quoted number and you wanted to extract that number as a float).
  * ``-mapf`` and ``-mapc`` allow you to extract some or all of the data from one or more columns and put that data
    into another column or columns.
  * ``-mapfrx`` and ``-mapc`` does that same as ``-mapf`` and ``-mapc`` but uses Regular Expression syntax, allowing
    you to form powerful pattern matching steps that extract a very specific portion or portions of the data.
  * ``-map`` and ``-maprx`` extract the data similarly to the two sets of map functions above (``-maprx`` uses Regular
    Expression syntax), but act on only one column at a time. This allows simpler modification of data in a single
    string column.
  
- :doc:`variables` : Create and use new variables during processing.

  * ``-var`` allows you to define new global variables and set their default value.
  * ``-evlc`` lets you create or modified record based variables and use them as part of your processing expression.
  * ``-map*`` handles string manipulation
  * ``-ovar`` limits the output to only include the global variables you've defined and not the columns from the data.
  
- :doc:`conditionals` : ``-filt``, ``-grep``, and ``-if ... -else ... -endif`` statements all let you control which
  datais processed.

  * ``-filt`` is the main filtering option and allows you to limit which data continues to be processed based on the
    results of the condition you define.
  * ``-grep`` compares the values of column from the input dataset against the values of a column in a lookup dataset.
    It only lets each record continue in the processing chain if the value of the specified column was present in both
    datasets.
  * ``-if ... -else ... -endif`` statements allow you to use many of the other options in ``aq_pp`` to create
    conditional expressions that each record is subject to.


.. toctree::
   :hidden:

   overview
   combining-datasets
   data-transform
   variables
   conditionals