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
      -sort[,AtrLst] ColTyp:ColNum | -sort[,AtrLst] ColName [ColName ...]

  Output_Spec:
      [-o[,AtrLst] File] [-c ColName [ColName ...]]


Description
===========

``aq_ord`` sorts input records according to the value of the sort columns.
Sort is done in memory, so it is fast.
However, the entire data set must fit into a single machine's main memory.
The program offers two sort modes. One is fast and simple but less flexible.
The other requires more processing overhead but is more versatile.

.. _`Raw sort mode`:

1) Raw sort mode

   In this mode, raw input rows are stored in memory *as-is*.
   Column values are not interpreted except for the sort column.
   Advantages are:

   * Simple spec. Only need the sort column index and type.
   * Fast. Only the sort column's value needs to be interpreted.
   * Output rows and input rows are identical because rows are stored as-is.
   * Rows can have varying number of columns as long as the sort column is
     always at the same position.

   Disadvantages are:

   * Only one sort column.
   * Input cannot be binary (from another aq_* program).
   * Cannot discard unwanted columns from input.
   * Cannot select or reposition columns on output.
   * Cannot output a title row, even if the input has one.
   * Memory intensive. The entire data set must be buffered, plus an additional
     sort array.

.. _`Parsed sort mode`:

2) Parsed sort mode

   In this mode, a column spec must be defined.
   Columns are converted before they are stored in memory -
   numeric and IP address types are stored in binary forms,
   string type is hashed and the pointer to the hash entry is stored.
   Advantages are:

   * Support composite sort key.
   * Input can be binary (from another aq_* program). In this format,
     the input columns need not be converted, so it is more efficient.
   * Can discard unwanted columns from input.
   * Can select and reposition columns on output.
   * Can control output title row.
   * Potentially more memory efficient when string values are repetitive.

   Disadvantages are:

   * More complex spec. Require all column types and names.
   * Slower due to the column conversions during input and output.
   * Output may not resemble the input. For example, an input numeric column
     of value "" will become "0" on output.
   * May use more memory than the size of the input if strings are mostly
     unique and numbers are small (e.g., integer values less than 1000).


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
  Only needed in `Parsed sort mode`_.
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


.. _`-sort`:

``-sort[,AtrLst] ColTyp:ColNum``
  Define the `Raw sort mode`_ sort column.
  ``ColTyp`` specifies the sort column's data type. See `-d`_ for a list of
  types,``X`` is not supported.
  ``ColNum`` specifies the column number (one-based) of the sort column in
  each row.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``dec`` - Sort in descending order. Default order is ascending.
    Descending sort is done by inverting the ascending sort result.

  Example:

   ::

    $ aq_ord ... -sort s:2

  * Sort records according to the string value of the 2nd column in ascending
    order.
  * This uses the `Raw sort mode`_, so no column spec is needed.


``-sort[,AtrLst] ColName [ColName ...]``
  Define the `Parsed sort mode`_ sort columns.
  ``ColNames`` must already be defined under `-d`_.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``dec`` - Sort in descending order. Default order is ascending.
    Descending sort is done by inverting the ascending sort result.

  Example:

   ::

    $ aq_ord ... -d i:Col1 s:Col2 ... -sort Col2 Col1

  * Sort records according to the string value of the 2nd column and the
    numeric value of the 1st column in ascending order.
  * This uses `Parsed sort mode`_, so more than one sort column can be
    specified.


.. _`-o`:

``[-o[,AtrLst] File] [-c ColName [ColName ...]]``
  Output data rows.
  Optional "``-o[,AtrLst] File``" sets the output attributes and file.
  See the `aq_tool output specifications <aq-output.html>`_ manual for details.

  In the `Raw sort mode`_, most output attributes have no effect since
  the records cannot be altered (only their order).
  The ``-c`` option is not applicable either.

  In the `Parsed sort mode`_,
  optional "``-c ColName [ColName ...]``" selects the columns to output.
  ``ColName`` refers to a column defined under `-d`_.
  A ``ColName`` can be preceeded with a ``~`` (or ``!``) negation mark.
  This means that the column is to be excluded.
  Without ``-c``, all columns are selected by default.
  If ``-c`` is specified without a previous ``-o``, output to stdout is
  assumed.

  Multiple sets of "``-o ... -c ...``" can be specified.

  Example:

   ::

    $ aq_ord ... -d s:Col1 s:Col2 s:Col3 ... -o,esc,noq - -c Col2 Col1

  * Output Col2 and Col1 (in that order) to stdout in a format suitable for
    Amazon Cloud.


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

