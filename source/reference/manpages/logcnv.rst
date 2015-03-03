======
logcnv
======


Synopsis
========

::

  logcnv [-h] Global_Opt Input_Spec Output_Spec

  Global_Opt:
      [-test] [-verb] [-bz ReadBufSiz]

  Input_Spec:
      [-f[,AtrLst] File [File ...]] [-d ColSpec [ColSpec ...]]

  Output_Spec:
      [[-o[,AtrLst] File] [-c ColName [ColName ...]] [-notitle]]


Description
===========

``logcnv`` is a stream-based log converter.
It processes input log files with a given column/separator spec and
outputs the same data in CSV or binary format.
Supported log format is:

 ::

  [separator]data_col[separator[data_col ...]][\r]\n

* Separators are literals that separate data columns.
* Data columns are typed - numbers, string and IP.
  They can have attributes that turn on special processing steps.

With its stream-based design, ``logcnv`` can process an unlimited amount of
data using a constant amount of memory. The output can either be stored
in a file or piped into another data processing component such as `aq_pp <aq_pp.html>`_.


Options
=======

.. _`-test`:

``-test``
  Test command line arguments and exit.

  * If all specs are good, the exit code will be 0.
  * If there is an error, the exit code will be non-zero. Usually, an error
    message will also be printed to stderr.


.. _`-verb`:

``-verb``
  Verbose - print program progress to stderr while processing.
  Usually, a marker is printed for each 10,000,000 records processed.


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
  If no `-f`_ option is specified, stdin is assumed.

  Example:

   ::

    $ logcnv ... -f,+1l,eok file1 -f file2 ...

  * File1 and file2 can have different attributes.


.. _`-d`:

``-d ColSpec [ColSpec ...]``
  Define the data columns and separators of the input records from all
  `-f`_ specs.
  Supported record format is:

   ::

    [separator]data_col[separator[data_col ...]][\r]\n

  For a separator, ``ColSpec`` has the form ``SEP:SepStr`` where ``SEP``
  (case insensitive) is a keyword and ``SepStr`` is the literal separator
  (1 to 31 bytes long).

  For a data column,``ColSpec`` has the form ``Type[,AtrLst]:ColName``.
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

  Up to 256 ``ColSpec`` can be defined (excluding ``X`` type columns).
  Optional ``AtrLst`` is a comma separated list containing:

  * ``clf`` - Denote that the input field uses Apache 2.0.46 and up escape
    sequences:

    * Non-printable => '\\xhh' where hh is the hex value of the byte.
    * '"' and '\\' => '\\"' and '\\\\'.
    * Some whitespaces => '\\r', '\\n', '\\t', '\\v', '\\f', etc.

  * ``esc`` - Denote that the input field uses '\\' as escape character.
    This is different from ``clf`` in that each '\\' only escape one
    following byte.
  * ``hex`` - For numeric type. Denote that the input field is in hexdecimal
    notation. Starting ``0x`` is optional. For example, ``100`` is
    converted to 256 instead of 100.
  * ``tim`` - For ``I`` or ``IS`` type. Denote that the input field is in
    Apache default timestamp format (e.g., '14/Feb/2009:08:31:30 +0900').
    The field will be converted back to UNIX seconds (e.g., 1234567890).
  * ``hl1`` - For ``S`` type. Denote that the input field contains the
    HTTP request line 1 as in:

     ::

      GET /index.html?query HTTP/1.0

    The field will be
    broken up into ``ColName_f1`` ("GET"), ``ColName_f2`` ("/index.html?query")
    and ``ColName_f3`` ("HTTP/1.0") on output.

  ``ColName`` restrictions:

  * Cannot exceed 31 bytes long.
    Recall that an input column with an ``hl1`` attribute is splitted into 3
    columns - ``ColName_f1``, ``ColName_f2`` and ``ColName_f3``;
    in this case, ``ColName`` must not exceed 28 bytes long.
  * Contain only alphanumeric and '_' characters. The first character
    cannot be a digit.
  * It is case insensitive. However, this spec may change in the future.

  Example:

   ::

    $ logcnv ... -d
        IP:h SEP:' ' S:l SEP:' ' S:u SEP:' [' I,tim:t SEP:'] "'
        S,clf,hl1:r SEP:'" ' I:s SEP:' ' I:b ...

  * Process records in the default common log columns.


.. _`-o`:

``[-o[,AtrLst] File] [-c ColName [ColName ...]] [-notitle]``
  Output data rows.
  Optional "``-o[,AtrLst] File``" sets the output attributes and file.
  If ``File`` is a '-' (a single dash), data will be written to stdout.
  Optional ``AtrLst`` is described under `Output File Attributes`_.

  Optional "``-c ColName [ColName ...]``" selects the columns to output.
  Recall that an input column with an ``hl1`` attribute is splitted into 3
  columns on output - ``ColName_f1``, ``ColName_f2`` and ``ColName_f3``;
  selection must be done on those 3 names individually.
  Without ``-c``, all columns are selected by default.
  If ``-c`` is specified without a previous ``-o``, output to stdout is
  assumed.

  Optional ``-notitle`` suppresses the column name label row from the output.
  A label row is normally included by default.

  Multiple sets of "``-o ... -c ... -notitle``" can be specified.

  Example:

   ::

    $ logcnv ... -d s:Col1 s:Col2 s:Col3 ... -o,esc,noq - -c Col2 Col1

  * Output Col2 and Col1 (in that order) to stdout in a format suitable for
    Amazon Cloud.


Exit Status
===========

If successful, the program exits with status 0. Otherwise, the program exits
with a non-zero status code along error messages printed to stderr.
Applicable exit codes are:

* 0 - Successful.
* 1-9 - Program initial preparation error.
* 10-19 - Input file load error.
* 20-29 - Result output error.


Input File Attributes
=====================

Each input file can have these comma separated attributes:

* ``eok`` - Make error non-fatal. If there is an input error, program will
  try to skip over bad/broken records. If there is a record processing error,
  program will just discard the record.
* ``qui`` - Quiet; i.e., do not print any input/processing error message.
* ``+Num[b|r|l]`` - Specifies the number of bytes (``b`` suffix), records (``r``
  suffix) or lines (no suffix or ``l`` suffix) to skip before processing.


Output File Attributes
======================

Some output file can have these comma separated attributes:

* ``app`` - Append to file; otherwise, file is overwritten by default.
* ``bin`` - Input in binary format (default is CSV).
* ``esc`` - Use '\\' to escape ',', '"' and '\\' (CSV).
* ``noq`` - Do not quote string fields (CSV).
* ``fmt_g`` - Use "%g" as print format for ``F`` type columns. Only use this
  to aid data inspection (e.g., during integrity check or debugging).

By default, output is in CSV format. Use the ``esc`` and ``noq`` attributes to
set output characteristics as needed.


Apache Format Reference
=======================

The following table shows the corresponding logcnv column spec for some
common format strings:

* %a => IP:Ip (Remote IP-address.)
* %A => IP:Ip (Local IP-address.)
* %B => I:Num (Size of response in bytes, excluding HTTP headers.)
* %b => I:Num (Like %B, but in CLF format, i.e. a '-' rather than a 0 when no
  bytes are sent.)
* %{Foobar}C => S:Str or S,clf:Str (The contents of cookie Foobar in the
  request sent to the server. Only version 0 cookies are fully supported.)
* %D => I:Num (The time taken to serve the request, in microseconds.)
* %{FOOBAR}e => S:Str or S,clf:Str (The contents of the environment variable
  FOOBAR.)
* %f => S:Str or S,clf:Str (Filename.)
* %h => S:Str or IP:ip (Remote host if HostnameLookups is set, IP otherwise.)
* %H => S:Str (The request protocol.)
* %{Foobar}i => S,clf:Str (The contents of Foobar: header line(s) in the
  request sent to the server.)
* %k => I:Num (Number of keepalive requests handled on this connection.)
* %l => S:Str or S,clf:Str (Remote logname.)
* %m => S:Str (The request method.)
* %{Foobar}n => S:Str or S,clf:Str (The contents of note Foobar from another
  module.)
* %{Foobar}o => S,clf:Str (The contents of Foobar: header line(s) in the reply.)
* %p => I:Num (The canonical port of the server serving the request.)
* %{format}p => I:Num (The canonical port of the server serving the request or
  the server's actual port or the client's actual port. Valid formats are
  canonical, local, or remote.)
* %P => I:Num (The process ID of the child that serviced the request.)
* %{format}P => I:Num (The process ID or thread id of the child that serviced
  the request. Valid formats are pid, tid, and hextid.)
* %q => S:Str (The query string prepended with a '?' or a blank if there is no
  query.)
* %r => S,clf:Str or S,clf,hl1:Str (First line of request.)
* %R => S:Str (The handler generating the response.)
* %s or %>s => I:Num (Status.)
* %t => I,tim:Num (Time the request was received in standard format.)
* %{format}t => Not supported.
* %T => I:Num (The time taken to serve the request, in seconds.)
* %u => S:Str or S,clf:Str (Remote user.)
* %U => S:Str (The URL path requested, not including any query string.)
* %v => S:Str (The canonical ServerName of the server serving the request.)
* %V => S:Str (The server name according to the UseCanonicalName setting.)
* %X => S:Str (Connection status when response is completed - 'X', '+' or '-'.)
* %I => I:Num (Bytes received, including request and headers.)
* %O => I:Num (Bytes sent, including headers.)

Separator specs must be added to complete the record description.
For example, consider this Common Log Format spec string:

 ::

  %h %l %u %t \"%r\" %>s %b

It can be represented by these column spec:

 ::

  IP:h SEP:' ' S:l SEP:' ' S:u SEP:' [' I,tim:t SEP:'] "'
  S,clf,hl1:r SEP:'" ' I:s SEP:' ' I:b


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udbd <udbd.html>`_ - User (Bucket) Database server
* `aq_udb <aq_udb.html>`_ - Interface to Udb server

