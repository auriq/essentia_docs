.. |<br>| raw:: html

   <br>

======
aq_ord
======

In-memory record sort


Synopsis
========

::

  aq_ord [-h] Global_Opt Input_Spec Sort_Spec Output_Spec

  Global_Opt:
      [-verb] [-stat]

  Input_Spec:
      [-f[,AtrLst] File [File ...]] [-d ColSpec [ColSpec ...]]

  Sort_Spec:
      -sort[,AtrLst] ColName [ColName ...]

  Output_Spec:
      [-blk NumRec FilPrefix] [-o[,AtrLst] File] [-c ColName [ColName ...]] |
      [-blk_only NumRec FilPrefix]


Description
===========

``aq_ord`` sorts input records according to the value of the sort columns.
Sort is done in memory, so it is fast.
The program offers three sort modes:

.. _`All at once sort`:

1) All at once sort

   In this mode, the sort is done by loading the entire data set into memory.
   This is the default sort mode.
   The requirement for this mode is:

   * There is enough memory to handle the entire data sets (plus overhead).

.. _`Block sort`:

2) Block sort

   Data is sorted in blocks of a given number of records. The blocks are first
   saved to files, then loaded and merged to produce the final result.
   The requirements for this mode are:

   * There is enough memory to handle at least a single block (plus overhead).
   * There is enough disk space to store all the intermediate block results.
   
.. _`Merge only`:

3) Merge only

   This will merge the input files/streams into a single output. The inputs
   must already be sorted in the same order as desired for the output. There
   is no memory requirement in this mode regardless of the data size,
   This support can be used to implement parallel sorts on large data sets
   over multiple machines.


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

    aq_ord: rec=Count err=Count


.. _`-f`:

``-f[,AtrLst] File [File ...]``
  Set the input attributes and files.
  See the `aq_tool input specifications <aq-input.html>`_ manual for details.

  Example:

   ::

    $ aq_ord ... -f,+1l file1 file2 ...

  * Skip the first line from both files before loading.


.. _`-d`:

``-d ColSpec [ColSpec ...]``
  Optionally define the input data columns.
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

    $ aq_ord ... -d s:Col1 s,lo:Col2 i,trm:Col3 ...

  * Col1 is a string. Col2 is also a string, but the input value will be
    converted to lower case. Col3 is an unsigned integer, the ``trm``
    attribute removes blanks around the value before it is converted to
    an internal number.


``-sort[,AtrLst] ColName [ColName ...]``
  Define the sort column(s).
  ``ColNames`` must already be defined under `-d`_.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``ncas`` - Do case insensitive match (default is case sensitive).
    For ASCII data only.
  * ``dec`` - Sort in descending order. Default order is ascending.
    Descending sort is done by inverting the ascending sort result.
  * ``mrg`` - Enable the `Merge only`_ mode. The inputs are simply merged
    according to the sort order, no actual sort is done.

  Example:

   ::

    $ aq_ord ... -d i:Col1 s:Col2 ... -sort Col2 Col1

  * Sort records according to the string value of the 2nd column and the
    numeric value of the 1st column in ascending order.


.. _`-blk`:

``-blk NumRec FilPrefix``
  Enable the `Block sort`_ mode.
  Data is loaded and sorted in blocks of ``NumRec`` records at a time.
  The results are saved to ``FilPrefix-BlkNo.bin`` files in aq_tool's internal
  binary format. ``BlkNo`` is the block number, it starts from 1 and increments
  for each ``NumRec`` records until the entire input is consumed.
  When this is done, the ``FilPrefix-BlkNo.bin`` files will be merged to
  produce the final result.


.. _`-blk_only`:

``-blk_only NumRec FilPrefix``
  Same as the `-blk`_ option except that the ``FilPrefix-BlkNo.bin`` files
  are not merged afterwards. No final result is produced.


.. _`-o`:

``[-o[,AtrLst] File] [-c ColName [ColName ...]]``
  Output data rows.
  Can be used with any of the sort modes except for `-blk_only`_
  Multiple sets of "``-o ... -c ...``" can be specified.

  Optional "``-o[,AtrLst] File``" sets the output attributes and file.
  See the `aq_tool output specifications <aq-output.html>`_ manual for details.

  Optional "``-c ColName [ColName ...]``" selects the columns to output.
  Normally, each selection is a column name.
  In addition, these special forms are supported:

  * ``*`` - An asterisk adds all columns to the output.
  * ``ColName[:NewName][+NumPrintFormat]`` - Add ``ColName`` to the output.
    If ``:NewName`` is given, it will be used as the output label.
    The ``+NumPrintFormat`` spec is for numeric columns. It overrides the
    print format of the column (*be careful with this format - a wrong spec
    can crash the program*).
  * ``^ColName[:NewName][+NumPrintFormat]`` - Same as the above, but with a
    leading ``^`` mark. It is used to *modify* the output label and/or format
    of a previously selected output column called ``ColName``.
    If ``^ColName[...]`` is the first selection after ``-c``, then ``*`` will be
    included automatically first.
  * ``~ColName`` - The leading ``~`` mark is used to *exclude* a previously
    selected output column called ``ColName``.
    If ``~ColName`` is the first selection after ``-c``, then ``*`` will be
    included automatically first.

  If ``-o`` is given without a ``-c``, then ``*`` is assumed.
  If ``-c`` is given without a prior ``-o``, the selected columns will
  be output to stdout.

  Example:

   ::

    $ aq_ord ... -d s:Col1 s:Col2 s:Col3 ... -o - -c Col2 Col1

  * Output Col2 and Col1 (in that order) to stdout.


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

