********************
Data Processing: Part 2
********************

The goal of this tutorial is to highlight how to perform complex data transformation and validation operations,
and output the results either to disk or a database. 


TODO 
====

* syntax highlighting
* DONE: table of contents
* terminology section 
  * colSPec
  * ??

* DONE: prerequisite


.. contents:: Table of Contents
   :depth: 3


Essentia Data Processing and the aq_pp command
================================================

This tutorial is a continuation of :doc:`../essentiatutorials/etl`. That tutorial involved a rather trivial Data Processing example involving counting the number of lines in a series of files.  

More typical cases involve validating the data, filtering data, and
deriving entirely new columns based on some mathematical operations or string processing. For that,
we developed a set of command line programs called the "**AQ tools**", which are part of the Essentia distribution.

Written in ``C`` to achieve a high level of performance, the AQ tools are able to manipulate and transform raw input
data into a format more easily handled by other AQ or third party tools.  

In particular,
the ``aq_pp`` program does the heavy lifting for all Data Processing operations.


The command structure of ``aq_pp`` consists of:

* **input specification** (:doc:`../../reference/manpages/aq-input`) specifying which file(s) to take the data from,
* various **processing specifications** to determine how data is processed, 
* and **output specifications** (:doc:`../../reference/manpages/aq-output`) describing how and where to put the results of your command.
    
There are also a variety of **global options** that modify the environment and default variables used in ``aq_pp``.

The following provides some working examples of ``aq_pp`` commands.  Data and scripts are found under
``tutorials/etl-engine`` in the git repository.

For further details of aq_pp command, check out the documentation at :doc:`/source/reference/manpages/aq_pp`

Prerequisites
-------------

In this tutorial, we'll assume that you're familiar with

* basic understanding of `bash and linux command line <http://linuxcommand.org/lc3_learning_the_shell.php>`_
* `Regex <https://regexone.com/>`_ for string manipulation

Now we're ready, let's get started!

  

Input Specifications
--------------------

First let's create a simple command that **imports** our example file ``chemistry.csv`` and **defines** its columns.

This is what the original csv data looks like.::
        
    studentid,lastname,firstname,midterm,final
    1,Dawson,Leona,76.5,B-
    2,Jordan,Colin,25.9,D
    3,Malone,Peter,97.2,A+

Here is the command.

.. code-block:: bash

        aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin
        ls -a

* ``-f`` specifies the file to operate on (chemistry.csv).  It accepts an optional ATTRIBUTEs in ``,+1``, which
  means to skip the first line (header in this case)
* ``-d`` defines the column names and data types.  The format is ``t,attribute:name`` with 't' being the data type.  An ``X``
  means to ignore a column.  In this example, we load the names and final grades as strings (forcing the last name to
  be upper case by ``up`` attribute), the student id as an integer, and the midterm grade as a float.

Since there are no processing or output specifications given, then the output is simply::

  "id","lastname","firstname","chem_mid","chem_fin"
  1,"DAWSON","Leona",76.5,"B-"
  2,"JORDAN","Colin",25.899999999999999,"D"
  3,"MALONE","Peter",97.200000000000003,"A+"

If we did provide `X` instead of ``chem_mid`` column, like this, 

``aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname X s:chem_fin``

the output won't display ``chem_mid`` column.

.. code-block:: bash

   "id","lastname","firstname","final"
   1,"DAWSON","Leona","B-"
   2,"JORDAN","Colin","D"
   3,"MALONE","Peter","A+"


Instead of providing the file name to input specification, we could have used the linux command ``cat`` to write the data in our example file ``chemistry.csv`` to standard output and then use ``-f`` to accept that data from standard input. ``cat chemistry.csv | aq_pp -f,+1 - -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin``


* ``-f`` still specifies the file to operate on; however, the file specified is ``-``. This ``-`` value tells aq_pp to read the data that is coming from standard input (in this case, chemistry.csv).

The output is the same::

  "id","lastname","firstname","chem_mid","chem_fin"
  1,"DAWSON","Leona",76.5,"B-"
  2,"JORDAN","Colin",25.899999999999999,"D"
  3,"MALONE","Peter",97.200000000000003,"A+"

By default, ``aq_pp`` will validate the input against the data type you defined it as.  For instance if a letter grade
was accidentally placed in lieu of the midterm percentage, the program will exit with an error.  By specifying the
optional ``eok`` attribute along with ``-f,+1``, the program will simply ignore/skip the input row that causes the error, and keep executing.
This feature makes it easy to produce validated output.

.. Note::
        Just in case if you're wondering, `Do I have to type in all of the column names and types every time I want to execute the command?`
        You can use :doc:`../../reference/manpages/loginf` command with ``-o_pp_col`` option, to get estimated column spec. For more details, `PUT LINK TO THE AQ_PP SAMPLE LINK HERE<https://google.com>`_


For more details about input specification, take a look at aq-input page :doc:`../../reference/manpages/aq-input`


Process Specifications
----------------------

The process specs define transformation operations on your data.  They fall into three groups:

* Conversion operations (between different datatypes, such as string to numeric and vice versa)
* Numerical operations (math etc)
* String operations (merge strings, extract substrings, etc)

In this section, we'll cover numerical operation example. But applications of the other 2 will be covered in `Data Transforms`_ section in this tutorial.

For a simple example, let's say that the midterm grades for the chemistry final need to be revised downward so that
the distribution falls within acceptable limits (i.e. grading on a curve)::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
        -eval 'chem_mid' 'chem_mid*0.8'

  "id","lastname","firstname","chem_mid","chem_fin"
  1,"DAWSON","Leona",61.200000000000003,"B-"
  2,"JORDAN","Colin",20.719999999999999,"D"
  3,"MALONE","Peter",77.760000000000005,"A+"

Here we use the math option ``-eval`` to adjust the chem_mid column down 20%.

``-eval`` option takes 2 arguments, in a form of ``-eval ColSpec|ColName Expression``, where 

* ``ColSpec``: Destination of the evaluated value. Name of existing column name or new column. 
* ``Expression``: expression you'd like to have the command evalueated.
Note that both of the arguments needs to be inside of single / double quotations. I personally recommend using single quotes for expression, in case of string being present within ``Expression``.

Take a look at :ref:`-eval <-eval>` option's section for more details.


Output Specifications
---------------------

By default, all known columns are output to stdout.  The :ref:`-o <-o>` option allows users to specify an output file, and
the :ref:`-c <-o>` option allows one to designate explicitly what columns to output.

For example::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
        -c id chem_fin

  "id","chem_fin"
  1,"B-"
  2,"D"
  3,"A+"

This simply restricts the output to the two designated columns::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
        -o newtable.csv -c id chem_fin

Similar, but the output is to a file named ``newtable.csv`` instead of the stdout. More details about output to file are available at :doc:`/source/reference/manpages/aq-output`

.. Note:
        Note that reversing the order of ``-o`` and ``-c`` options will cause the command to write all of the columns data into the designated file, while outputting the designated columns to stdout. Make sure you're using the 2 options in correct order.
        
Instead of the output being routed into the stdout or a file, it can also be directly imported into the UDB, which is
an extremely powerful part of the Essentia toolkit.  We expand on this more in the :doc:`in-memory-db` tutorial.

Combining Datasets
------------------


There are a number of scenarios (particularly with log data) where merging two different types of files is useful.
There are 3 options available combining/joining datasets in aq_pp.

1. :ref:`-cat <-cat>`: Merge datasets (stack the datasets vertically, roughly speaking)
2. :ref:`-cmb <-cmb>`: Joining datasets (combine the datasets horizontally by joining rows, roughly speaking)
3. :ref:`-sub <-sub>`: replace a value on string column on current data set with provided lookup table.

For the example below, we'll use the same chemistry.csv data as well as physics.csv, shown below.

.. csv-table:: Chemistry Table
   :header: "id", "lastname", "firstname", "midterm", "final"
   :widths: 5, 15, 15, 15, 15

   1, "Dawson", "Leona", 76.5, "B-"
   3, "Jordan", "Colin", 25.9, "D"
   4, "Malone", "Peter", 97.2, "A+"


.. csv-table:: Physics Table
   :header: "id", "lastname", "firstname", "midterm", "final"
   :widths: 5, 15, 15, 15, 15

   1, "Dawson", "Leona", 88.5, "A"
   3, "Malone", "Peter", 77.2, "B"
   4, "Cannon", "Roman", 55.8, "C+"


cat for merging datasets
^^^^^^^^^^^^^^^^^^^^^^^^

Lets consider the case where we want to merge our chemistry and physics grades into a single table. We'll use other file called physics.csv, besides chemistry.csv. For clearity, let us show what both tables looks like again.

Merging this data into the chemistry.csv with command below will result in::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
        -cat,+1 physics.csv i:id s,up:lastname s:firstname f:phys_mid s:phys_fin
        
  "id","lastname","firstname","chem_mid","chem_fin","phys_mid","phys_fin"
  1,"DAWSON","Leona",76.5,"B-",0,
  2,"JORDAN","Colin",25.899999999999999,"D",0,
  3,"MALONE","Peter",97.200000000000003,"A+",0,
  1,"DAWSON","Leona",0,,88.5,"A"
  3,"MALONE","Peter",0,,77.200000000000003,"B"
  4,"CANNON","Roman",0,,55.799999999999997,"C+"


As a table, the result will look like

.. csv-table:: Result of -cat, chemistry and physics
   :header: "id","lastname","firstname","chem_mid","chem_fin","phys_mid","phys_fin"
   :widths: 5, 15, 15, 10, 10, 10, 10

   1,"DAWSON","Leona",76.5,"B-",0,""
   2,"JORDAN","Colin",25.899999999999999,"D",0,""
   3,"MALONE","Peter",97.200000000000003,"A+",0,""
   1,"DAWSON","Leona",0,"",88.5,"A"
   3,"MALONE","Peter",0,"",77.200000000000003,"B"
   4,"CANNON","Roman",0,"",55.799999999999997,"C+"



The ``-cat`` option is used for such a merge, and it is easiest to think of it as the ``aq_pp`` specific version of
the unix command of the same name.  The difference here is that ``aq_pp`` will create new columns in the output,
while simply concatenating the two files will result in just the same 5 columns as before.

The ``-cat`` option stacked the rows from ``physics.csv`` to the bottom of ``chemistry.csv`` table. Also note that aq_tool fills empty data with 0s for numerical column, and empty string for string column. In the case above, newly created column that did not exist before in the table are left empty or 0.

|

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

As a table, the result is

.. csv-table:: Result of -cmb, chemistry and physics
   :header: "id", "lastname", "firstname", "chem_mid", "chem_fin", "phys_mid", "phys_fin"
   :widths: 5, 15, 15, 10, 10, 10, 10
   
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


Good way to think of ``-cmb`` option is that it's stacking 2 tables horizontally, only for the records which shares same key values, while ``-cat`` option can be thought as vertical stacking of the data intuitively.



sub for lookup tables
^^^^^^^^^^^^^^^^^^^^^

An important type of dataset joining is replacing some value in a file with a matching entry in a lookup table.
In the following example, we wish to convert a students letter grade from 'A,B,C...' etc into a simple PASS/FAIL by substituting the value of chem_fin with pass or fail from ``grades.csv``,which looks like this::

        grade,result
        A*,PASS
        B*,PASS
        C*,PASS
        D+,PASS
        D*,FAIL
        E*,FAIL
        F*,FAIL


Now let's take a look at the command and the result::


  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
  -sub,+1,pat chem_fin grades.csv

  "id","lastname","firstname","chem_mid","chem_fin"
  1,"DAWSON","Leona",76.5,"PASS"
  2,"JORDAN","Colin",25.899999999999999,"FAIL"
  3,"MALONE","Peter",97.200000000000003,"PASS"


As a table, 

.. csv-table:: -sub result with chemistry and grades
   :header: "id", "lastname", "firstname", "chem_mid", "chem_fin"
   :widths: 5, 15, 15, 15, 15

   1,"DAWSON","Leona",76.5,"PASS"
   2,"JORDAN","Colin",25.899999999999999,"FAIL"
   3,"MALONE","Peter",97.200000000000003,"PASS"



Note the use of the ``pat`` attribute when we designate the lookup table.  This means that column 1 of the lookup
table can have a pattern instead of a static value.  In our case, we can cover grades 'A+,A,
and A-' by the pattern 'A*'.

More options for the pattern is available at :ref:`-sub<-sub>`


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

The :ref:`-eval <-eval>` option allows users to overwrite or create entirely new columns based on some operation with existing
columns or built-in variables.  The types of operations are broad, covering both string and numerical data.

Basic rule for syntax again for review, is ``... -eval ColSpec|ColName Expression`` where ``Expression`` is the computation / expression you'd like to evaluate, and ``ColSpec|ColName`` is the destination of the result, either existing column or new column.

For example, if we want to merge our id, 'first' and 'last' name columns from the chemistry file to create a new
column, we can do::

  aq_pp -f,+1 chemistry.csv -d i:id s:lastname s:firstname f:chem_mid s:chem_fin \
        -eval s:fullname 'ToS(id)+"-"+firstname+" "+lastname'

  "id","lastname","firstname","chem_mid","chem_fin","fullname"
  1,"Dawson","Leona",76.5,"B-","1-Leona Dawson"
  2,"Jordan","Colin",25.899999999999999,"D","2-Colin Jordan"
  3,"Malone","Peter",97.200000000000003,"A+","3-Peter Malone"


.. csv-table:: -eval result
   :header: "id", "lastname", "firstname", "chem_mid", "chem_fin", "fullname"
   :widths: 5, 15, 15, 15, 15, 20

   1,"Dawson","Leona",76.5,"B-","1-Leona Dawson"
   2,"Jordan","Colin",25.899999999999999,"D","2-Colin Jordan"
   3,"Malone","Peter",97.200000000000003,"A+","3-Peter Malone"

Note that the expression is surrounded by single quotations, and string within with double quotations. Expression for ``-eval`` options always needs to be surrounded by them, while colName requires no quotations.

Also note the use of a built in function ``ToS`` which converts a numeric to a string. There are many such :doc:`built in
functions<../../reference/manpages/aq-emod>`, and users are free to write their own to plug into the AQ tools.  Note also that since we created a new
column, we had to provide the 'column spec', which in this case is ``s:fullname`` to designate a string labeled
"fullname".

Built in Variables
^^^^^^^^^^^^^^^^^^

It may be useful to display the the record number or a random integer in the output table.  The ``aq_pp`` handles this via built-in variables.  In the example below, we augment the output with a row number.  We add 1 to it to compensate for
skipping the header via the ``-f,+1`` flag ::

  aq_pp -f,+1 chemistry.csv -d i:id s:lastname s:firstname f:chem_mid s:chem_fin \
        -eval i:row '$RowNum+1'

  "id","lastname","firstname","chem_mid","chem_fin","row"
  1,"Dawson","Leona",76.5,"B-",2
  2,"Jordan","Colin",25.899999999999999,"D",3
  3,"Malone","Peter",97.200000000000003,"A+",4


.. csv-table:: data with row numbers
   :header: "id", "lastname", "firstname", "chem_mid", "chem_fin", "row"
   :widths: 5, 15, 15, 15, 15, 5

   1,"Dawson","Leona",76.5,"B-",2
   2,"Jordan","Colin",25.899999999999999,"D",3
   3,"Malone","Peter",97.200000000000003,"A+",4


Another built-in variable is ``$Random`` for random number generation.
More options for built in variables are available on :ref:`-eval section of aq_pp manual <-eval>`

|

String Manipulation
^^^^^^^^^^^^^^^^^^^

With raw string data, it is often necessary to extract information based on a a pattern or regular expression.
There are 2 types of options that we can use for this purpose, such as ones below.

* :ref:`-map <-map>`
* :ref:`-mapf <-mapf>` & :ref:`-mapc <-mapc>`

Using ``-map`` option
"""""""""""""""""""""

Consider the simple case of extracting a 5 digit zip code from data which looks like this ::

  91101
  91101-1234
  zipcode: 91101 1234

A unix regular expression of ``([0-9]{5})`` would easily capture the 5 digit zip code. 
We'll first input the file as a single string column named zip, and use ``-map`` option to specify the column to extract zip code from. Basic syntax of this option is::

        ... -map[,AttrLst] ColName MapFrom MapTo ...

where 

* ``[,AttrLst]``: list of attributes to use.
* ``ColName``: string column name to extract the pattern from.
* ``MapFrom``: regular expression specifying the pattern to extract.
* ``MapTo``: specify how the extracted string will be mapped to the column.

Now let's extract the zip from the data, and map it in a format of ``zip=91101``::

  aq_pp -f zip.csv -d s:zip -map,rx_extended zip "([0-9]{5})" 'zip=%%1%%'
  
  "zip"
  "zip=91101"
  "zip=91101"
  "zip=91101"


With ``-map,rx_extended`` option, we're using the attribute of ``rx_extended`` to specify the the type of regex we'd like to use, as well as providing the column name (``zip``) to extract data from.
The captured value (in this case the first group, or '1', is mapped to a string using ``%%1%%``.  The output string can contain other text. :ref:`Details of the MapTo syntax <MapToSyntax>` is also available.


Using ``-mapf ... -mapc`` options
"""""""""""""""""""""""""""""""""

The previous example highlights extraction and overwriting a single column.  We can also merge regex matching from multiple columns to overwrite or create a new column, using ``-mapf ... -mapc`` option pair. These options works together in pair, which would look like this::

        ... -mapf[,AtrLst] ColName MapFrom -mapc ColSpec|ColName MapTo ...

Looking at the syntax above, you've probably noticed that some of the arguments are same as ``-map`` option we've seen previously.
Only difference between these options is that these options map the extracted string on new column (``ColSpec``) or on existing column (``Colname``, but not on the original column where the string was extracted), while ``-map`` option maps the extracted pattern back to the original column. 

Same syntax rules from ``-map`` apply to other arguments, such as ``[,ArtList]``, ``MapFrom`` and ``MapTo``. 

Note that these two options **can be used multiple times in one command**, and **both options have to exist within a command**.

For example, we can take our chemistry students example (data available in the `Combining Datasets`_ section) and create nicknames
for them based on the first three letters of their first name, and last 3 letters of their last name::

  aq_pp -f,+1 chemistry.csv -d i:id s:lastname s:firstname f:chem_mid s:chem_fin \
  -mapf,rx_extended firstname "^(.{3})" -mapf,rx_extended lastname "(.{3})$" -mapc s:nickname "%%1%%%%2%%"

  "id","lastname","firstname","chem_mid","chem_fin","nickname"
  1,"Dawson","Leona",76.5,"B-","Leoson"
  2,"Jordan","Colin",25.899999999999999,"D","Coldan"
  3,"Malone","Peter",97.200000000000003,"A+","Petone"

We use multiple ``-mapf,rx_extended`` options to extract stringsg from multiple columns, and then ``-mapc`` to map the matches to a new nickname column. ``%%1%%`` and ``%%2%%`` are placeholders for thextracted data. 

Some useful resources regarding to string manipulations

* :ref:`-mapf/c <-mapf>`
* :ref:`MapFrom Syntax <MapFromSyntax>`
* :ref:`MapTo Syntax <MapToSyntax>`
* :ref:`Regex Attributes used in mapping options <RegexAttributes>`
* `Regular Expression Tutorial <https://www.regular-expressions.info/tutorial.html>`


Variables
^^^^^^^^^

Often it is necessary to use a global variable that is not output as a column but rather acts as an aid to calculation.

Consider the following where we wish to sum a column::

  echo -e "1\n2\n3" | aq_pp -f - -d i:x -var 'i:sum' 0 -eval 'sum' 'sum+x' -ovar -

  "sum"
  6

We defined a 'sum' global variable and for each validated record we added a value to it.  Finally, we use ``-ovar -``
to output our variables to the stdout(instead of the columns).
Details of ``-ovar`` is available at :ref:`here <-ovar>`


Filters and Conditionals
------------------------

Filters and if/else statements are used by ``aq_pp`` to help clean and process raw data.

Following options will be covered in this section.
* :ref:`-filt <-filt>`
* :ref:`-grep <-grep>`
* :ref:`-grep <-grep>`
* :ref:`-if -else <ConditionalProcessingGroups>`


Using Filter Option
"""""""""""""""""""

``-filt`` is used to define and apply filtering conditions to the data, so we can filter out certain records. Basic syntax looks like this::

        ... -filt FilterSpec ...

where ``FilterSpec`` is **single quoted** logical expression that evaluates to true or false on each record. Logical expression is composed of ``LeftHandSide [<compare> RightHandSide]`` where Left/RightHandSide is column name or constant value(**unquoated**), and compare is comparison operators. 

As an example, from the chemistry table, we will select only those Chemistry students who had a midterm score greater than 50%::

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


Data Processing at Scale
=========================

In the first part of this tutorial, we demonstrated how we can use Essentia to select a set of log files and pipe the
contents to the unix ``wc`` command.  In a similar manner, we can pipe the data to ``aq_pp`` to apply more complex Data Processing operations on a large set of files. 

Cleaning the 'browse' data
--------------------------

First, lets switch back to the ``tutorials/woodworking`` directory.
For our first example, we are tasked with generating a cleaned version of each file,
and saving it as a comma separated file with bz2 compression::

  $ mkdir bz2
  $ ess stream browse 2014-09-01 2014-09-30 "aq_pp -f,+1,eok - -d %cols -o,notitle - | bzip2 - -c > ./bz2/%file.bz2"

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
    -o,notitle - -c purchaseDate userID articleID price refID \
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



