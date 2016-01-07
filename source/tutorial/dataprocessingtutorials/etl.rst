********************
ETL Engine: Part 2
********************

The goal of this tutorial is to highlight how to perform complex data transformation and validation operations,
and output the results to either to disk or a database.  This is commonly referred to as **ETL** for
Extract-Transform-Load.

Essentia ETL and the aq_pp command
======================================

This tutorial is a continuation of :doc:`../essentiatutorials/etl`. That tutorial involved a rather trivial ETL example.  

More typical cases involve validating the data, filtering data, and
deriving entirely new columns based on some math operations or string processing. For that,
we developed a set of command line programs called the "**AQ tools**", which are part of the Essentia distribution.

Written in ``C`` to achieve a high level of performance, the AQ tools are able to manipulate and transform raw input
data into a format more easily handled by other AQ or third party tools.  

In particular,
the ``aq_pp`` program does the heavy lifting for all ETL operations.


The command structure of ``aq_pp`` consists of:

* an **input specification** specifying which file(s) to take the data from,
* various **processing specifications** to determine how data is processed, 
* and **output specifications** describing how and where to put the results of your command.
    
There are also a variety of **global options** that modify the environment and default variables used in ``aq_pp``.

The following provides some working examples of ``aq_pp`` commands.  Data and scripts are found under
``tutorials/etl-engine`` in the git repository.

Input Specifications
--------------------

First let's create a simple command that **imports** our example file ``chemistry.csv`` and **defines** its columns.

``aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin``

* ``-f`` specifies the file to operate on (chemistry.csv).  It accepts an optional ATTRIBUTE in ``,+1``, which
  means to skip the first line (header in this case)
* ``-d`` defines the column names and types.  The format is ``t,attribute:name`` with 't' being the type.  An 'X'
  means to ignore a column.  In this example, we load the names and final grades as strings (forcing the last name to
  be upper case), the student id as an integer, and the midterm grade as a float.

Since there are no processing or output specifications given, the the output is simply::

  "id","lastname","firstname","chem_mid","chem_fin"
  1,"DAWSON","Leona",76.5,"B-"
  2,"JORDAN","Colin",25.899999999999999,"D"
  3,"MALONE","Peter",97.200000000000003,"A+"

By default, ``aq_pp`` will validate the input against the type you defined it as.  For instance if a letter grade
was accidentally placed in lieu of the midterm percentage, the program will exit with an error.  By specifying the
optional ``eok`` attribute along with ``-f,+1``, the program will simply ignore the input row.
This feature makes it easy to produce validated output.


Process Specifications
----------------------

The process specs define transformation operations on your data.  They fall into three groups:

* Conversion operations (string to numeric and vice versa)
* Numerical operations (math etc)
* String operations (merge strings, extract substrings, etc)

For a simple example, let's say that the midterm grades for the chemistry final need to be revised downward so that
the distribution falls within acceptable limits (i.e. grading on a curve)::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
        -eval 'chem_mid' 'chem_mid*0.8'

  "id","lastname","firstname","chem_mid","chem_fin"
  1,"DAWSON","Leona",61.200000000000003,"B-"
  2,"JORDAN","Colin",20.719999999999999,"D"
  3,"MALONE","Peter",77.760000000000005,"A+"

Here we use the math switch ``eval`` to adjust the chem_mid column down 20%.


Output Specifications
---------------------

By default, all known columns are output to stdout.  The ``-o`` switch allows users to specify an output file, and
the ``-c`` switch allows one to designate explicitly what columns to output.

For example::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
        -c id chem_fin

  "id","chem_fin"
  1,"B-"
  2,"D"
  3,"A+"

This simply restricts the output to the two designate columns::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
        -o newtable.csv -c id chem_fin

Similar, but the output is to a file named ``newtable.csv`` instead of the stdout.

Instead of the output being routed into the stdout or a file, it can also be directly imported into the UDB, which is
an extremely powerful part of the Essentia toolkit.  We expand on this more in the :doc:`in-memory-db` tutorial.

Combining Datasets
------------------

cat for merging datasets
^^^^^^^^^^^^^^^^^^^^^^^^

There are a number of scenarios (particularly with log data) where merging two different types of files is useful.
Lets consider the case where we want to merge our chemistry and physics grades into a single table::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
        -cat,+1 physics.csv i:id s,up:lastname s:firstname f:phys_mid s:phys_fin
        
  "id","lastname","firstname","chem_mid","chem_fin","phys_mid","phys_fin"
  1,"DAWSON","Leona",76.5,"B-",0,
  2,"JORDAN","Colin",25.899999999999999,"D",0,
  3,"MALONE","Peter",97.200000000000003,"A+",0,
  1,"DAWSON","Leona",0,,88.5,"A"
  3,"MALONE","Peter",0,,77.200000000000003,"B"
  4,"CANNON","Roman",0,,55.799999999999997,"C+"


The ``-cat`` option is used for such a merge, and it is easiest to think of it as the ``aq_pp`` specific version of
the unix command of the same name.  The difference here is that ``aq_pp`` will create new columns in the output,
while simply concatenating the two files will result in just the same 5 columns as before.

cmb for joining datasets
^^^^^^^^^^^^^^^^^^^^^^^^

However most users will want to JOIN datasets based on common values between two files.  In this case, the first and
last name, as well as the country, are the common columns between the two files.  The ``-cmb`` option is similar to
``-f`` and ``-d`` since it defines the number of lines to skip and the column specification for the second file.
Records will be matched based on all the columns that share the same names between the two files.  For example::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
        -cmb,+1 physics.csv i:id X X f:phys_mid s:phys_fin
        
  "id","lastname","firstname","chem_mid","chem_fin","phys_mid","phys_fin"
  1,"DAWSON","Leona",76.5,"B-",88.5,"A"
  2,"JORDAN","Colin",25.899999999999999,"D",0,
  3,"MALONE","Peter",97.200000000000003,"A+",77.200000000000003,"B"


Users familiar with SQL will recognize this as a LEFT OUTER JOIN. All the data from the first file is preserved,
while data from the second file is included when there is a match.  Where there is no match,
the value is 0 for numeric columns, or the empty string for string columns.  In this case,
since the label ``i:id`` is common between both file specifications, that is the join key.
We could also have joined based off multiple keys as well: For example matching first AND last
names will achieve the same result::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
  -cmb,+1 physics.csv X s,up:lastname s:firstname f:phys_mid s:phys_fin


sub for lookup tables
^^^^^^^^^^^^^^^^^^^^^

An important type of dataset joining is replacing some value in a file with a matching entry in a lookup table.
In the following example, we wish to convert a students letter grade from 'A,B,C...' etc into a simple PASS/FAIL::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
  -sub,+1,pat chem_fin grades.csv

  "id","lastname","firstname","chem_mid","chem_fin"
  1,"DAWSON","Leona",76.5,"PASS"
  2,"JORDAN","Colin",25.899999999999999,"FAIL"
  3,"MALONE","Peter",97.200000000000003,"PASS"

Note the use of the ``pat`` attribute when we designate the lookup table.  This means that column 1 of the lookup
table can have a pattern instead of a static value.  In our case, we can cover grades 'A+,A,
and A-' by the pattern 'A*'.


The ``-cmb`` can be used substituting data, but for situations similar to the one above, ``-sub`` is preferred because:

1. It does not create additional columns like ``-cmb`` does.  Values are modified in place.
2. ``-sub`` can match regular expressions and patterns, while ``-cmb`` is limited to exact matches.
3. ``-sub`` is faster.


Data Transforms
---------------

The input specification defines all the input columns we have to work with.  The goal of the process spec is to
modify these data according to various rules.

eval
^^^^

The ``-eval`` switch allows users to overwrite or create entirely new columns based on some operation with existing
columns or built-in variables.  The types of operations are broad, covering both string and numerical data.

For example, if we want to merge our id, 'first' and 'last' name columns from the chemistry file to create a new
column, we can do::

  aq_pp -f,+1 chemistry.csv -d i:id s:lastname s:firstname f:chem_mid s:chem_fin \
        -eval s:fullname 'ToS(id)+"-"+firstname+" "+lastname'

  "id","lastname","firstname","chem_mid","chem_fin","fullname"
  1,"Dawson","Leona",76.5,"B-","1-Leona Dawson"
  2,"Jordan","Colin",25.899999999999999,"D","2-Colin Jordan"
  3,"Malone","Peter",97.200000000000003,"A+","3-Peter Malone"

Note the use of a built in function ``ToS`` which converts a numeric to a string. There are many such built in
functions, and users are free to write their own to plug into the AQ tools.  Note also that since we created a new
column, we had to provide the 'column spec', which in this case is ``s:fullname`` to designate a string labeled
"fullname".

Built in Variables
^^^^^^^^^^^^^^^^^^

It may be useful to note the the record number or a random integer in the output table.  The ``aq_pp`` handles this via
built-in variables.  In the example below, we augment the output with a row number.  We add 1 to it to compensate for
skipping the header via the ``-f,+1`` flag ::

  aq_pp -f,+1 chemistry.csv -d i:id s:lastname s:firstname f:chem_mid s:chem_fin \
        -eval i:row '$RowNum+1'

  "id","lastname","firstname","chem_mid","chem_fin","row"
  1,"Dawson","Leona",76.5,"B-",2
  2,"Jordan","Colin",25.899999999999999,"D",3
  3,"Malone","Peter",97.200000000000003,"A+",4

Another built-in variable is ``$Random`` for random number generation.

String Manipulation
^^^^^^^^^^^^^^^^^^^

With raw string data, it is often necessary to extract information based on a a pattern or regular expression.
Consider the simple case of extracting a 5 digit zip code from data which looks like this ::

  91101
  91101-1234
  zipcode: 91101 1234

A unix regular expression of ``([0-9]{5})`` would easily capture the 5 digit zip code.  In this 1 column example the
command would be::

  aq_pp -f zip.csv -d s:zip -map,rx_extended zip "([0-9]{5})" 'zip=%%1%%'
  
  "zip"
  "zip=91101"
  "zip=91101"
  "zip=91101"


``aq_pp`` has a number of options related to pattern matching.  First and formost, it supports regular expressions
and a format developed for another product called RT metrics.  Regex is more widespread, but the RT format has
certain advantages for parsing log based data.  Full details can be found in the :doc:`../../reference/manpages/aq_pp`
manual.

Back to the example above, we use the ``-map,rx_extended`` switch to identify the column to work with and the type of regex we want to use.  
Finally, the captured value (in this case the
first group, or '1', is mapped to a string using ``%%1%%``.  The output string can contain other text.

This example highlights extraction and overwriting a single column.  We can also merge regex matching from multiple
columns to overwrite or create a new column.  For example, we can take our chemistry students and create nicknames
for them based on the first three letters of their first name, and last 3 letters of their last name::

  aq_pp -f,+1 chemistry.csv -d i:id s:lastname s:firstname f:chem_mid s:chem_fin \
  -mapf,rx_extended firstname "^(.{3})" -mapf,rx_extended lastname "(.{3})$" -mapc s:nickname "%%1%%%%2%%"

  "id","lastname","firstname","chem_mid","chem_fin","nickname"
  1,"Dawson","Leona",76.5,"B-","Leoson"
  2,"Jordan","Colin",25.899999999999999,"D","Coldan"
  3,"Malone","Peter",97.200000000000003,"A+","Petone"

Instead of ``-map,rx_extended``, we use multiple ``-mapf,rx_extended`` statements and then ``-mapc`` to map the matches to a new nickname
column.


Variables
^^^^^^^^^

Often it is necessary to use a global variable that is not output as a column but rather acts as an aid to calculation.

Consider the following where we wish to sum a column::

  echo -e "1\n2\n3" | aq_pp -f - -d i:x -var 'i:sum' 0 -eval 'sum' 'sum+x' -ovar -

  "sum"
  6

We defined a 'sum' global variable and for each validated record we added a value to it.  Finally, we use ``-ovar -``
to output our variables to the stdout (instead of the columns).


Filters and Conditionals
------------------------

Filters and if/else statements are used by ``aq_pp`` to help clean and process raw data.

For example, if we want to select only those Chemistry students who had a midterm score greater than 50%, we can do::

  aq_pp -f,+1 chemistry.csv -d i:id s:lastname s:firstname f:chem_mid s:chem_fin \
        -filt 'chem_mid > 50.0'

  "id","lastname","firstname","chem_mid","chem_fin"
  1,"Dawson","Leona",76.5,"B-"
  3,"Malone","Peter",97.200000000000003,"A+"




Another useful option is the ``-grep`` flag, which has utility similar to the Unix command of the same name.  Given a
file containing a 'whitelist' of students, we are asked to select only the matching students from our Chemistry class::

  aq_pp -f,+1 chemistry.csv -d i:id s:lastname s:firstname f:chem_mid s:chem_fin \
        -grep lastname whitelist.csv X FROM

  "id","lastname","firstname","chem_mid","chem_fin"
  2,"Jordan","Colin",25.899999999999999,"D"

The format of the ``grep`` switch allows the whitelist to contain multiple columns.  We select the column to use via
the 'FROM' designator.  ``grep`` also accepts attributes.  For instance with ``grep,ncas``, we would have matched
Peter Malone as well in the example above.


A final yet incredibly useful technique for processing your data is to use conditional statements 'if, else, elif,
and endif'

Let's extend the previous example by boosting the midterm scores of anyone in the whitelist by a factor of 2, and
leaving the others untouched::

  aq_pp -f,+1 chemistry.csv -d i:id s:lastname s:firstname f:chem_mid s:chem_fin \
        -if -grep lastname whitelist.csv X FROM -eval chem_mid 'chem_mid*2' -endif

  "id","lastname","firstname","chem_mid","chem_fin"
  1,"Dawson","Leona",76.5,"B-"
  2,"Jordan","Colin",51.799999999999997,"D"
  3,"Malone","Peter",97.200000000000003,"A+"


ETL at Scale
============

At the start of this tutorial, we demonstrated how we can use Essentia to select a set of log files and pipe the
contents to the unix ``wc`` command.  In a similar manner, we can do with with ``aq_pp``,
enabling us to apply more complex ETL operations on a large set of files.  In this tutorial we will focus on
'extract and transform', and detail how to load the data onto other platforms in other sections.

Cleaning the 'browse' data
--------------------------

First, lets switch back to the ``tutorials/woodworking`` directory.
For our first example, we are tasked with generating a cleaned version of each file,
and saving it as a comma separated file with bz2 compression::

  $ mkdir bz2
  $ ess stream browse 2014-09-01 2014-09-30 "aq_pp -f,+1,eok - -d %cols -notitle | bzip2 - -c > ./bz2/%file.bz2"

We can break down the command (everything within the double quotes) as follows:

f,+1,eok -
    This tells ``aq_pp`` that the first line should be skipped **(+1)**, that errors are OK  **(eok)**
    and that the input is being piped in via stdin.
    With ``eok`` set, whenever ``aq_pp`` sees
    an articleID (which we defined as an integer) with a string value, it will reject it. This takes care of the 'TBD'
    entries.  Normally ``aq_pp`` would halt upon seeing an error.  This allows users to use ``aq_pp`` as both a data
    validator and a data cleaner.

d %cols
    Tells ``aq_pp`` what the column specification is.  We determined this in the previous tutorial where we setup our
    datastore and categorized our files.  The ``%cols`` is a substitution string.  Instead of having to enter the
    columns each time by hand, Essentia will lookup the column spec from your datastore settings and place it here.
    There are several substitution strings that can be used, and they are listed in the section:
    :doc:`../../reference/tables/index`

notitle
    A switch to turn off the header line when generating output

bzip2 - -c > /data/%file.bz2
    Finally pipe the output of the command to the ``bzip`` utility.  We use the substitution string ``%file`` to
    generate the same filename as the input, except with a ``bz2`` extension.


Cleaning the 'purchase' data
----------------------------

The purchase data needs the articleID corrected for all dates on and after the 15th of September.  There are a few
ways to achieve this, but the most robust is the following:

.. code-block:: sh
   :linenos:
   :emphasize-lines: 3,4,5,6,7

    $ ess stream purchase 2014-09-01 2014-09-30 \
    "aq_pp -f,+1,eok,qui - -d %cols \
    -eval is:t 'DateToTime(purchaseDate,\"Y.m.d.H.M.S\") - DateToTime(\"2014-09-15\",\"Y.m.d\")' \
    -if -filt 't>0' \
      -eval articleID 'articleID+1' \
    -endif \
    -c purchaseDate userID articleID price refID \
    -notitle \
    | bzip2 - -c > ./bz2/%file.bz2"

.. note::

  The use of quotations in Unix commands invariably leads to a need to ``escape`` characters in order
  for them to be recognized.

Line 3 creates a new column 't', which is a signed integer, and it is assigned a value equal to the difference between
the time of the current record and the cutoff time of September 15.  Positive values of 't' indicate that the record
was collected after the 15th.

Line 4 creates a filter condition, which is triggered for all records on or after the 15th.

Line 5 adjusts the articleID to correct for the website error.

Line 6 ends the block

Line 7 specifies the output columns.  If not provided, it would also output our new 't' column which we used only for
temporary purposes.

We could have just issued 2 Essentia commands, one with dates selected before the 15th and another for dates after.
In this case it would have been easy, but there are other scenarios where it becomes more problematic.



Final Notes
===========

This tutorial was designed to teach users how to use ``aq_pp``, but did not compare it against other possible solutions.
To demonstrate the utility of ``aq_pp``, let's look at the following problem:

We have sales data from a fictional store that caters to international clients.  We record the amount spent for each
purchase and the currency it was purchased with.  We wish to compute the total sales in US Dollars.
We have 2 files to process.  The first contains the time, currency type, and amount spent, and the second is a lookup
table that has the country code and USD exchange rate.

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

Let's compare 2 solutions against ``aq_pp``.  If you wish to execute the commands to see for yourself,
the data are in the ``tutorial/etl-engine`` directory.

**SQL**::

  select ROUND(sum(sales.amount*exchange.rate),2) AS total from sales INNER JOIN exchange ON sales.currency = exchange.currency;

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

  aq_pp -f,+1 sales.csv -d s:date s:currency f:amount -cmb,+1 exchange.csv s:currency f:rate -var f:sum 0.0 -eval 'sum' 'sum+(amount*rate)' -ovar -

The AuriQ preprocessor is similar in spirit to AWK, but it simplifies many issues.
We'll detail the specifics in the rest of the documentation, but even without knowing all of the syntax, the
intent of the command is fairly easy to discern. Instead of positional arguments, columns
are named, therefore making an ``aq_pp`` command more human readable.
Additionally, it is very fast, in fact an order of magnitude faster in this example.



