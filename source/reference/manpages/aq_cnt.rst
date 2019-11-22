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
      [-f[,AtrLst]|-fX[,AtrLst] File [File ...]] [-d ColSpec [ColSpec ...]]

  Count_Spec:
      [-k KeyName ColName [ColName ...]]

  Output_Spec:
      [-kx[,AtrLst] File KeyName ColName [ColName ...]]
      [-kX[,AtrLst] File KeyName ColName [ColName ...] [STATS:ColName [STATS:ColName ...]]]
      [-o[,AtrLst] File]


Description
===========

``aq_cnt`` counts and reports unique keys in a data set. Unique keys in this context means unique values in arbitrary column(s). Users are able to specify column(s) to count the keys on.

* First, it reads data from the input in various formats (e.g., CSV)
  according to the input spec.
* Then it converts the input into internal data rows
  according to the column spec.
* Keys are then stored and counted according to the key specs.
  Each key can have one or more columns.
  Multiple keys can be counted within a run.
* Additional statistics (sum, average, standard deviation, minimum and maximum)
  for associated columns can be tracked along with each unique key combination.
* At the end, a summary containg row and key counts is output by default.
  Values of the unique keys can also be output to key specific files.

Since the program needs to store all the *unique* keys in memory in order to
count them, its capacity is limited by the amount of physical memory in a
machine.
In case there is a capacity issue, an `aq_pp <aq_pp.html>`_ and
`Udb <udbd.html>`_ combination can
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

``-f[,AtrLst]|-fX[,AtrLst] File [File ...]``
  Set the input attributes and files.
  See the `aq_tool input specifications <aq-input.html>`_ manual for details.

  * Use ``-f`` for a normal key counting operation on the input data.
  * Use ``-fX`` to merge input data produced by one or more
    `aq_cnt ... -kX ... <#kx2>`__ commands.

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
  * ``STAT`` - For `-fX <#f>`__ only. It represents a corresponding ``STAT``
    column in the `-kX <#kx2>`__ output to be merged.

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

   ::

    $ aq_cnt ... -d s:Col1 s,lo:Col2 i,trm:Col3 -kX,notitle - - Col1 Col2 stats:Col3 | aq_cnt -fX - -d s:Col1 s:Col2 stats:Col3 -kX - - Col1 Col2 stats:Col3

  * The first command in the pipe outputs extended statistics for Col3.
  * The second command in the pipe merges the input and output the merged
    result.
  * The example is for syntax demonstration only. In practice, a merge would
    take the results from several ``aq_cnt .. -kX ..`` commands as input.

   ::

    $ aq_cnt ... -d s:Col1 s,lo:Col2 i,trm:Col3 -kX,aq - - Col1 Col2 stats:Col3 | aq_cnt -fX,aq - -kX - - Col1 Col2 stats:Col3

  * The same as the above example except that no column spec is needed with
    the use of the ``aq`` attribute.


.. _`-k`:

``-k KeyName ColName [ColName ...]``
  Define a key to count.
  The resulting unique key count will be outputted in the `-o`_ overall
  count summary.
  ``KeyName`` is a unique label for this key combination.
  ``ColNames`` are the columns forming the key.


.. _`-kx1`:

``-kx[,AtrLst] File KeyName ColName [ColName ...]``
  Define a key to count and output the unique key combinations to ``File``.
  See the `aq_tool output specifications <aq-output.html>`_ manual for details
  on ``AtrLst``.

  * ``KeyName`` is a unique label for this key combination.
    If given, the resulting unique key count will be reported in the `-o`_
    overall count summary. But if it is a blank or a ``-`` (a single dash),
    its count will not be reported there.
  * ``ColNames`` are the columns forming the key.

  The result in ``File`` has this form:

   ::

    "KeyCol1","KeyCol2",...
    Val1,Val2,...
    ...


.. _`-kx2`:

``-kX[,AtrLst] File KeyName ColName [ColName ...] [STATS:ColName [STATS:ColName ...]]``
  Define a key to count and output the unique key combinations as well as
  their occurrence counts to ``File``.
  See the `aq_tool output specifications <aq-output.html>`_ manual for details
  on ``AtrLst``.
  Note that this report may be generated even when this option is not given.
  See `Default output`_ for details.

  * ``KeyName`` is a unique label for this key combination.
    If given, the resulting unique key count will be reported in the `-o`_
    overall count summary. But if it is a blank or a ``-`` (a single dash),
    its count will not be reported there.
  * ``ColNames`` are the columns forming the key.
    The ``STATS:ColName`` spec is for the extended statistics of an associated
    numeric column. The statistics include its sum, average, standard deviation,
    minimum and maximum for each unique key combination. They are output as
    double precision floating point numbers following the occurrence count.
  * If `-fX <#f>`__ is specified, a ``.`` (a single dot) can be used in place
    of the column spec. This will automatically add all the input columns to
    the column spec.

  The result in ``File`` has this form:

   ::

    "KeyCol1","KeyCol2",...,"Count"
    Val1,Val2,...,Occurrence
    ...

  If ``STATS:ColName`` are used, the result will be:

   ::

    "KeyCol1","KeyCol2",...,"Count","StatsCol1.sum","StatsCol1.avg","StatsCol1.stddev","StatsCol1.min","StatsCol1.max",...
    Val1,Val2,...,Occurrence,Sum1,Avg1,StdDev1,Min1,Max1,...
    ...


.. _`-o`:

``-o[,AtrLst] File``
  Set the output attributes and file for the overall count summary.
  See the `aq_tool output specifications <aq-output.html>`_ manual for details
  on ``AtrLst``.
  Note that this report may be generated even when this option is not given.
  See `Default output`_ for details.

  The summary has this form:

   ::

    "row","KeyName1","KeyName2",...
    Rows,Count1,Count2,...

  where "row" gives the sample count and "KeyNames"
  (from `-k`_, `-kx <#kx1>`__ and `-kX <#kx2>`__) give their unique key counts.

  Example:

   ::

    $ aq_cnt ... -d s:Col1 s:Col2 ip:Col3 ...
        -k Key1 Col1 -kX File2 Key2 Col3 Col2 ...
        -o -

  * Define two keys. Key1 is a single column key. Key2 is a composite key.
    Summary counts of Key1 and Key2 go to stdout.
    In addition, unique key combinations and occurrence counts of Key2
    go to File2.


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


Default Output
==============

Outputs can be set explicitly via the `-kx <#kx1>`__, `-kX <#kx2>`__ and `-o`_
options. The program may also generate certain outputs by default without any
explicit setting.

* If there is one or more `-k`_ specs, but there is not `-o`_ spec,
  a summary will be output to stdout by default.
* If `-fX <#f>`__ is specified, but there is no `-kx <#kx1>`__, `-kX <#kx2>`__
  or `-o`_ spec, a `-kX <#kx2>`__ spec having the same columns as the
  input will be output to stdout by default.


See Also
========

* `aq-input <aq-input.html>`_ - aq_tool input specifications
* `aq-output <aq-output.html>`_ - aq_tool output specifications
* `aq_pp <aq_pp.html>`_ - Record preprocessor

