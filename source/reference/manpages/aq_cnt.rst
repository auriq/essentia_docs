.. |<br>| raw:: html

   <br>

======
aq_cnt
======

Data row/key count


Synopsis
========

::

  aq_cnt [-h] Global_Opt Input_Spec Count_Spec Output_Spec

  Global_Opt:
      [-verb] [-stat]

  Input_Spec:
      [-f[,AtrLst] File [File ...]] -d ColSpec [ColSpec ...]

  Count_Spec:
      [-k KeyName ColName [ColName ...]]

  Output_Spec:
      [-kx|-kX[,AtrLst] File KeyName ColName [ColName ...]]
      [-o[,AtrLst] File]


Description
===========

``aq_cnt`` counts and reports unique keys in a data set.

* First, it reads data from the input in various formats (e.g., CSV)
  according to the input spec.
* Then it converts the input into internal data rows
  according to the column spec.
* Key columns are then stored and counted according to the key spec.
  Each key can have one or more columns.
  Multiple keys can be counted within a run.
* At the end, a summary containg row and key counts is output by default.
  Values of the unique keys can also be output to key specific files.

Since the program needs to store all the unique keys in memory in order to
count them, its capacity is limited by the amount of physical memory in a
machine.
In case there is a capacity issue, an `aq_pp <aq_pp.html>`_ and `Udb <udbd.html>`_ combination can
be used to implement a scalable key counting solution.


Options
=======

.. _`-verb`:

``-verb``
  Verbose - print program progress to stderr while processing.
  Usually, a marker is printed for each 10,000,000 records processed.


.. _`-stat`:

``-stat``
  Print a record count summary line to stderr at the end of processing.
  The line has the form:

   ::

    aq_cnt: rec=Count err=Count


.. _`-f`:

``-f[,AtrLst] File [File ...]``
  Set the input attributes and files.
  See the `aq_tool input specifications <aq-input.html>`_ manual for details.

  Example:

   ::

    $ aq_cnt ... -f,+1l file1 file2 ...

  * Skip the first line from both files before loading.


.. _`-d`:

``-d ColSpec [ColSpec ...]``
  Define the input data columns.
  See the `aq_tool input specifications <aq-input.html>`_ manual for details.
  In general, ``ColSpec`` has the form ``Type[,AtrLst]:ColName``.
  Supported ``Types`` are:

  * ``S`` - String.
  * ``F`` - Double precision floating point.
  * ``L`` - 64-bit unsigned integer.
  * ``LS`` - 64-bit signed integer.
  * ``I`` - 32-bit unsigned integer.
  * ``IS`` - 32-bit signed integer.
  * ``IP`` - v4/v6 address.

  Optional ``AtrLst`` is a comma separated list of column specific attributes.
  ``ColName`` is the column name (case insensitive). It can contain up to
  31 alphanumeric and '_' characters. Its first character cannot be a digit.

  Example:

   ::

    $ aq_cnt ... -d s:Col1 s,lo:Col2 i,trm:Col3 ...

  * Col1 is a string. Col2 is also a string, but the input value will be
    converted to lower case. Col3 is an unsigned integer, the ``trm``
    attribute removes blanks around the value before it is converted to
    an internal number.


.. _`-k`:

``-k KeyName ColName [ColName ...]``
  Define a key named ``KeyName`` and its associated columns by ``ColNames``.
  The key count will appear in the overall count summary (see `-o`_).
  ``KeyName`` may be optionally preceeded by a ``wqy:`` to indicate a
  Web Query key.  In this case, only one column is allowed in the key.
  The value of the column will be automatically splitted at the '&'
  separator; each of the resulting elements will be counted as as a key
  value.


.. _`-kx`:

``-kx[,AtrLst] File KeyName ColName [ColName ...]``
  Define a key and its columns as in `-k`_.
  Additionally, output the unique key columns
  to ``File`` in this form:

   ::

    "ColName","ColName",...
    ColVal,ColVal,...
    ...

  See the `aq_tool output specifications <aq-output.html>`_ manual for details
  on ``AtrLst``.

  **Note**: If this option is given, overall count summary output will be
  suppressed unless `-o`_ is specified explicitly.


``-kX[,AtrLst] File KeyName ColName [ColName ...]``
  Define a key and its columns as in `-k`_.
  Additionally, output the unique key columns and their occurrence count
  to ``File`` in this form:

   ::

    "ColName","ColName",...,"Count"
    ColVal,ColVal,...,Num
    ...

  See the `aq_tool output specifications <aq-output.html>`_ manual for details
  on ``AtrLst``.

  **Note**: If this option is given, overall count summary output will be
  suppressed unless `-o`_ is specified explicitly.


.. _`-o`:

``-o[,AtrLst] File``
  Set the output attributes and file for the overall count summary.
  The summary has this form:

   ::

    "row","KeyName","KeyName",...
    Num,Num,Num,...

  where "row" gives the row count and "KeyNames"
  (from `-k`_, `-kx`_ and `-kX`_) give their unique key counts.

  See the `aq_tool output specifications <aq-output.html>`_ manual for details
  on ``AtrLst``.

  If this option is not given and there is no `-kx`_ or `-kX`_ option,
  a summary will be output to stdout by default.

  Example:

   ::

    $ aq_cnt ... -d s:Col1 s:Col2 ip:Col3 ...
        -k Key1 Col1 -kX File2 Key2 Col3 Col2 ...
        -o -

  * Define two keys. Key1 is a single column key. Key2 is a composite key.
    Summary counts of Key1 and Key2 go to stdout.
    In addition, unique values and occurrence counts of Key2 go to File2.


Exit Status
===========

If successful, the program exits with status 0. Otherwise, the program exits
with a non-zero status code along error messages printed to stderr.
Applicable exit codes are:

* 0 - Successful.
* 1 - Memory allocation error.
* 2 - Command option spec error.
* 3 - Initialization error.
* 4 - System error.
* 5 - Missing or invalid license.
* 11 - Input open error.
* 12 - Input read error.
* 13 - Input processing error.
* 21 - Output open error.
* 22 - Output write error.


See Also
========

* `aq-input <aq-input.html>`_ - aq_tool input specifications
* `aq-output <aq-output.html>`_ - aq_tool output specifications
* `aq_pp <aq_pp.html>`_ - Record preprocessor

