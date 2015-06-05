======
aq_cnt
======


Synopsis
========

::

  aq_cnt [-h] Global_Opt Input_Spec Count_Spec Output_Spec

  Global_Opt:
      [-verb] [-stat] [-bz ReadBufSiz]

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

    aq_cnt:TagLab rec=Count err=Count


.. _`-bz`:

``-bz ReadBufSiz``
  Set input buffer length.
  It is also the maxium record length. If a record exceeds this length, it is
  considered broken and will cause the program to abort or the record to be
  discarded.
  Default length is 64KB. Use this option if a longer record is expected.
  ``ReadBufSiz`` is a number in bytes.


.. _`-f`:

``-f[,AtrLst] File [File ...]``
  Set the input attributes and files.
  If the data come from stdin, set ``File`` to '-' (a single dash).
  Optional ``AtrLst`` is described under `Input File Attributes`_.
  If this option is not given, stdin is assumed.

  Example:

   ::

    $ aq_cnt ... -f,+1l,eok file1 -f file2 ...

  * File1 and file2 can have different attributes.


.. _`-d`:

``-d ColSpec [ColSpec ...]``
  Define the columns of the input records from all `-f`_ specs.
  ``ColSpec`` has the form ``Type[,AtrLst]:ColName``.
  Up to 256 ``ColSpec`` can be defined (excluding ``X`` type columns).
  Supported ``Types`` are:

  * ``S`` - String.
  * ``F`` - Double precision floating point.
  * ``L`` - 64-bit unsigned integer.
  * ``LS`` - 64-bit signed integer.
  * ``I`` - 32-bit unsigned integer.
  * ``IS`` - 32-bit signed integer.
  * ``IP`` - v4/v6 address.
  * ``X[Type]`` - marks an unwanted input column.
    Type is optional. It can be one of the above (default is ``S``).
    ColName is also optional. Such a name is simply discarded.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``esc`` - Denote that the input field uses '\\' as escape character. Data
    exported from databases (e.g. MySQL) sometimes use this format. Be careful
    when dealing with multibyte character set because '\\' can be part of a
    multibyte sequence.
  * ``noq`` - Denote that the input field is not quoted. Any quotes in or around
    the field are considered part of the field value.
  * ``hex`` - For numeric type. Denote that the input field is in hexdecimal
    notation. Starting ``0x`` is optional. For example, ``100`` is
    converted to 256 instead of 100.
  * ``trm`` - Trim leading/trailing spaces from input field value.
  * ``lo``, ``up`` - For ``S`` type. Convert input field to lower/upper case.

  ``ColName`` restrictions:

  * Cannot exceed 31 bytes long.
  * Contain only alphanumeric and '_' characters. The first character
    cannot be a digit.
  * It is case insensitive. However, this spec may change in the future.

  Example:

   ::

    $ aq_cnt ... -d s:Col1 s,lo:Col2 i,trm:Col3 ...

  * Col1 is a string. Col2 also a string, but the input value will be converted
    to lower case. Col3 is an unsigned integer, the ``trm`` attribute removes
    blanks around the value before it is converted to an internal number.


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

  If ``File`` is a '-' (a single dash), data will be written to stdout.
  Optional ``AtrLst`` is described under `Output File Attributes`_.

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

  If ``File`` is a '-' (a single dash), data will be written to stdout.
  Optional ``AtrLst`` is described under `Output File Attributes`_.

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

  If ``File`` is a '-' (a single dash), data will be written to stdout.
  Optional ``AtrLst`` is described under `Output File Attributes`_.

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
* 11 - Input open error.
* 13 - Input processing error.
* 21 - Output open error.
* 22 - Output write error.


Input File Attributes
=====================

Each input file can have these comma separated attributes:

* ``eok`` - Make error non-fatal. If there is an input error, program will
  try to skip over bad/broken records. If there is a record processing error,
  program will just discard the record.
* ``qui`` - Quiet; i.e., do not print any input/processing error message.
* ``tsv`` - Input is in TSV format (default is CSV).
* ``sep=c`` - Use separator 'c' (single byte) as column separactor.
* ``bin`` - Input is in binary format (default is CSV).
* ``esc`` - '\\' is an escape character in input fields (CSV or TSV).
* ``noq`` - No quotes around fields (CSV).
* ``+Num[b|r|l]`` - Specifies the number of bytes (``b`` suffix), records (``r``
  suffix) or lines (no suffix or ``l`` suffix) to skip before processing.

By default, input files are assumed to be in formal CSV format. Use the
``tsv``, ``esc`` and ``noq`` attributes to set input characteristics as needed.


Output File Attributes
======================

Some output file can have these comma separated attributes:

* ``app`` - Append to file; otherwise, file is overwritten by default.
* ``bin`` - Input in binary format (default is CSV).
* ``esc`` - Use '\\' to escape ',', '"' and '\\' (CSV).
* ``noq`` - Do not quote string fields (CSV).
* ``fmt_g`` - Use "%g" as print format for ``F`` type columns. Only use this
  to aid data inspection (e.g., during integrity check or debugging).
* ``notitle`` - Suppress the column name label row from the output.
  A label row is normally included by default.

By default, output is in CSV format. Use the ``esc`` and ``noq`` attributes to
set output characteristics as needed.


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udbd <udbd.html>`_ - User (Bucket) Database server
* `aq_udb <aq_udb.html>`_ - Interface to Udb server

