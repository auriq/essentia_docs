======
aq_ord
======

In-memory record sort


Synopsis
========

::

  aq_ord [-h] Global_Opt Input_Spec Sort_Spec Output_Spec

  Global_Opt:
      [-verb] [-stat] [-bz ReadBufSiz]

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

    $ aq_ord ... -f,+1l,eok file1 -f file2 ...

  * File1 and file2 can have different attributes.


.. _`-d`:

``-d ColSpec [ColSpec ...]`` or ``-d [SepSpec] ColSpec [[SepSpec] ColSpec ...]``
  Define the columns in the input records from all the `-f`_ specs.
  Only needed in `Parsed sort mode`_.
  Up to 2048 ``ColSpec`` can be defined (excluding ``X`` type columns).
  ``ColSpec`` has the form ``Type[,AtrLst]:ColName``.
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

  * ``n=Len`` - Extract exactly ``Len`` source bytes. Use this for a fixed
    length data column.
  * ``esc`` - Denote that the input field uses '\\' as escape character. Data
    exported from databases (e.g. MySQL) sometimes use this format. Be careful
    when dealing with multibyte character set because '\\' can be part of a
    multibyte sequence.
  * ``clf`` - Denote that the input field uses these encoding methods:

    * Non-printable bytes encoded as '\\xHH' where ``HH`` is the hex value of
      the byte.
    * '"' and '\\' encoded as '\\"' and '\\\\'.
    * Selected whitespaces encoded as '\\r', '\\n', '\\t', '\\v' and '\\f'.

  * ``noq`` - Denote that the input field is not quoted. Any quotes in or around
    the field are considered part of the field value.
  * ``hex`` - For numeric type. Denote that the input field is in hexdecimal
    notation. Starting ``0x`` is optional. For example, ``100`` is
    converted to 256 instead of 100.
  * ``trm`` - Trim leading/trailing spaces from input field value.
  * ``lo``, ``up`` - For ``S`` type. Convert input field to lower/upper case.

  ``ColName`` is case insensitive. It can have up to 31 alphanumeric and '_'
  characters. The first character must not be a digit.

  The alternate column definition involving ``SepSpec`` is designed for
  input data that have multibyte separators and/or varying separators from
  field to field. In these cases, *all* the separators must be individually
  specified. ``SepSpec`` has the form ``SEP:SepStr`` where ``SEP``
  (case insensitive) is a keyword and ``SepStr`` is a literal separator of one
  or more bytes. A ``SepSpec`` is generally needed between any two columns
  unless the former column has a length spec.

  Example:

   ::

    $ aq_ord ... -d s:Col1 s,lo:Col2 i,trm:Col3 ...

  * Col1 is a string. Col2 is also a string, but the input value will be
    converted to lower case. Col3 is an unsigned integer, the ``trm``
    attribute removes blanks around the value before it is converted to
    an internal number.

   ::

    $ aq_ord ... -d sep:' [' s:time_s sep:'] "' s,clf:url sep:'"' ...

  * This parses data of the form: [01/Apr/2016:01:02:03 +0900] "/index.html".


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
  If ``File`` is a '-' (a single dash), data will be written to stdout.
  Optional ``AtrLst`` is described under `Output File Attributes`_.

  In the `Raw sort mode`_, most output attributes have no effect since
  the records are not altered (only their order).
  The ``-c`` option is not applicable either.

  In the `Parsed sort mode`_,
  optional "``-c ColName [ColName ...]``" selects the columns to output.
  ``ColName`` refers to a column in the data set.
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
* 11 - Input open error.
* 12 - Input read error.
* 13 - Input processing error.
* 21 - Output open error.
* 22 - Output write error.


Input File Attributes
=====================

Each input option can have a list of comma separated attributes:

* ``eok`` - Make input error non-fatal. If there is an input parse error,
  program will try to skip over bad/broken record. If there is an input data
  processing error, program will just discard the record.
* ``qui`` - Quiet; i.e., do not print any input error message.
* ``csv`` - Input is in CSV format. This is the default.
* ``sep=c`` or ``sep=\xHH`` - Input is in 'c' (single byte) separated value
  format. '\xHH' is a way to specify 'c' via its HEX value ``HH``.
  Note that ``sep=,`` is not the same as ``csv`` because CSV is a more
  advanced format.
* ``fix`` - Input columns are all fixed width. There is no field separator.
  Individual column width is specified as a column attribute.
* ``tab`` - Input is in HTML table format - columns must be enclosed in
  "``<td>data</td>``" or "``<td ...>data</td>``" and rows must be terminated
  by a "``</tr>``".
* ``bin`` - Input is in aq_tool's internal binary format.
* ``esc`` - '\\' is an escape character in input fields (non binary).
* ``noq`` - No quotes around fields (CSV).
* ``+Num[b|r|l]`` - Specifies the number of bytes (``b`` suffix), records (``r``
  suffix) or lines (no suffix or ``l`` suffix) to skip before processing.

If no input format attribute is given, CSV is assumed.


Output File Attributes
======================

Each output option can have a list of comma separated attributes:

* ``notitle`` - Suppress the column name label row from the output.
  A label row is normally included by default.
* ``app`` - When outputting to a file, append to it instead of overwriting.
* ``csv`` - Output in CSV format. This is the default.
* ``sep=c`` or ``sep=\xHH`` - Output in 'c' (single byte) separated value
  format. '\xHH' is a way to specify 'c' via its HEX value ``HH``.
  Note that ``sep=,`` is not the same as ``csv`` because CSV is a more
  advanced format.
* ``bin`` - Output in aq_tool's internal binary format.
* ``esc`` - Use '\\' to escape the field separator, '"' and '\\' (non binary).
* ``noq`` - Do not quote string fields (CSV).
* ``fmt_g`` - Use "%g" as print format for ``F`` type columns. Only use this
  to aid data inspection (e.g., during integrity check or debugging).

If no output format attribute is given, CSV is assumed.


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udbd <udbd.html>`_ - Udb server
* `aq_udb <aq_udb.html>`_ - Udb server interface

