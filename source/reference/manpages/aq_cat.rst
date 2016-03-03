======
aq_cat
======

Input multiplexer


Synopsis
========

::

  aq_cat [-h] Global_Opt Input_Spec Output_Spec

  Global_Opt:
      [-verb] [-stat] [-bz ReadBufSiz]

  Input_Spec:
      [-f[,AtrLst] File [File ...]] [-d ColSpec [ColSpec ...]]

  Output_Spec:
      [-o[,AtrLst] File] [-c ColName [ColName ...]]


Description
===========

``aq_cat`` is a multiplexer that concatenate multiple input streams into
a single output stream. The output can then be stored as a single unit or
piped to another command for further processing. Records from the streams
can be in delimiter-separated-values (e.g., CSV) format or aq_tool's internal
binary format.

The tool has two modes of actions:

* Without column spec - This is the simplest usage. The iuputs must be
  records of delimiter-separated-values. The output will be in the same
  format. All inputs should be in the same format; otherwise, the output
  will contain mixed format data. Alternative output format
  (e.g., binary mode) is not supported. Output columns can be selected
  by column numbers.

* With column spec - This mode is more versatile. The iuputs can be
  in delimiter-separated-values formats, aq_tool's internal binary format
  or a mix. The output can either be in CSV or aq_tool's internal binary
  format. Output columns can be selected by names.

The input *streams* for the tool are usually output from other commands.
Generally, the streams can be constructed using *named pipes* or ``bash``'s
*process substition* feature. For example,

 ::

  $ mkfifo stream_1 stream_2
  $ Command_1 > stream_1 &
  $ Command_2 > stream_2 &
  $ aq_cat ... -f stream_1 stream_2 | Command_3 ...
  $ rm -f stream_1 stream_2

* Directed the output from ``Command_1`` and ``Command_2`` into ``aq_cat``
  via named pipes.

 ::

  bash$ aq_cat ... -f <( Command_1 ) <( Command_1 ) | Command_3 ...

* This behaves like the previous example except that ``bash``'s
  process substition has been used to run ``Command_1`` and ``Command_2``
  and to manage their outputs.


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

    aq_cat: rec=Count err=Count out=Count


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
  Note that the input files are generally *streams*, as described under
  `Description`_.

  Example:

   ::

    $ aq_cat ... -f,+1l stream_1 -f stream_2 ...

  * Skip the first line from stream_1, but keep the entire stream_2.


.. _`-d`:

``-d ColSpec [ColSpec ...]``
  Optionally define the columns in the input records from all the `-f`_ specs.
  ``ColSpec`` has the form ``Type[,AtrLst]:ColName``.
  Up to 2048 ``ColSpec`` can be defined (excluding ``X`` type columns).
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

    $ aq_cat ... -d s:Col1 s,lo:Col2 i,trm:Col3 ...

  * Col1 is a string. Col2 is also a string, but the input value will be
    converted to lower case. Col3 is an unsigned integer, the ``trm``
    attribute removes blanks around the value before it is converted to
    an internal number.


.. _`-o`:

``[-o[,AtrLst] File] [-c ColName [ColName ...]]``
  Output data rows.
  Optional "``-o[,AtrLst] File``" sets the output attributes and file.
  If ``File`` is a '-' (a single dash), data will be written to stdout.
  Optional ``AtrLst`` is described under `Output File Attributes`_.
  However, if no `-d`_ column spec is given, most output attributes
  have no effect since the column data cannot be altered.

  Optional "``-c ColName [ColName ...]``" selects the columns to output.
  Normally, ``ColNames`` are names from the `-d`_ column spec.
  However, if no column spec is given, the desired column numbers
  (one-based) can specified instead;
  column ranges are also accepted (e.g "... -c 5-3 1 2 ...").
  Without ``-c``, all columns are selected by default.
  If ``-c`` is specified without a previous ``-o``, output will got to stdout.

  Note that this tool supports outputting the same column more than once.
  For example, both "... -c 1 1 ..." and "... -c Col1 Col1 ..." are valid.
  Most aq_tools do not support this though.

  Multiple sets of "``-o ... -c ...``" can be specified.

  Example:

   ::

    $ aq_cat ... -d s:Col1 s:Col2 s:Col3 ... -o,esc,noq - -c Col2 Col1

  * Output Col2 and Col1 (in that order) to stdout in a format suitable for
    Amazon Cloud.

   ::

    $ aq_cat ...  -o - -c 2 1

  * With no `-d`_ spec, columns can only be selected by their column numbers.
    Most output attributes are not applicable either.


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
* `aq_udb <aq_udb.html>`_ - Udb server interface

