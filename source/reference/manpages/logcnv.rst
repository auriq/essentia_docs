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
      [-o[,AtrLst] File] [-c ColName [ColName ...]]


Description
===========

``logcnv`` is a stream-based log format converter.
It processes input log files with a given column/separator spec and
outputs the same data in CSV or binary format.
Supported log format is:

 ::

  [separator]data_col[data_col ...][separator[data_col ...]][\r]\n

* Separators are literals that separate data columns.
* Data columns are typed - numbers, string and IP.
  They can have attributes that turn on special processing steps.
* A data column is usually followed by a separator or end-of-record.
  However, this is not necessary if the data column has a length sepc.
  See the `-d`_ option specification for details.

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

    [separator]data_col[data_col ...][separator[data_col ...]][\r]\n

  For a separator, ``ColSpec`` has the form ``SEP:SepStr`` where ``SEP``
  (case insensitive) is a keyword and ``SepStr`` is the literal separator.
  The separator string is taken *as-is*, no escape sequence is interpreted.

  For a data column, ``ColSpec`` has the form ``Type[,AtrLst]:ColName``.
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
  * ``trm`` - Trim leading/trailing spaces from input field value.
  * ``lo``, ``up`` - For ``S`` type. Convert input field to lower/upper case.
  * ``tim`` - For ``I`` or ``IS`` type. Denote that the input field is in
    Apache default timestamp format (e.g., '14/Feb/2009:08:31:30 +0900').
    The field will be converted back to UNIX seconds (e.g., 1234567890).
  * ``n=Len`` - Extract exactly ``Len`` bytes. Use this for a fixed length
    data column. If a data column has a length spec, it can be followed by
    another data column.

  ``ColName`` restrictions:

  * Cannot exceed 31 bytes long.
  * Contain only alphanumeric and '_' characters. The first character
    cannot be a digit.
  * It is case insensitive. However, this spec may change in the future.

  Example:

   ::

    $ logcnv ... -d
        IP:h SEP:' ' S:l SEP:' ' S:u SEP:' [' I,tim:t SEP:'] "'
        S,clf:r SEP:'" ' I:s SEP:' ' I:b ...

  * Process records in the default common log columns.


.. _`-o`:

``[-o[,AtrLst] File] [-c ColName [ColName ...]]``
  Output data rows.
  Optional "``-o[,AtrLst] File``" sets the output attributes and file.
  If ``File`` is a '-' (a single dash), data will be written to stdout.
  Optional ``AtrLst`` is described under `Output File Attributes`_.

  Optional "``-c ColName [ColName ...]``" selects the columns to output.
  Without ``-c``, all columns are selected by default.
  If ``-c`` is specified without a previous ``-o``, output to stdout is
  assumed.

  Multiple sets of "``-o ... -c ...``" can be specified.

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
* ``notitle`` - Suppress the column name label row from the output.
  A label row is normally included by default.

By default, output is in CSV format. Use the ``esc`` and ``noq`` attributes to
set output characteristics as needed.


Apache Format Reference
=======================

The following table shows the corresponding logcnv column spec for some
common format strings:

* %a (Remote IP-address) => IP:Ip
* %A (Local IP-address) => IP:Ip
* %B (Size of response in bytes, excluding HTTP headers) => I:Num
* %b (Like %B, but in CLF format, i.e. a '-' rather than a 0 when no
  bytes are sent) => I:Num
* %{Foobar}C (The contents of cookie Foobar in the request sent to the server.
  Only version 0 cookies are fully supported) => S:Str or S,clf:Str
* %D (The time taken to serve the request, in microseconds) => I:Num
* %{FOOBAR}e (The contents of the environment variable FOOBAR) => S:Str or
  S,clf:Str
* %f (Filename) => S:Str or S,clf:Str
* %h (Remote host if HostnameLookups is set, IP otherwise) => S:Str or IP:ip
* %H (The request protocol) => S:Str
* %{Foobar}i (The contents of Foobar: header line(s) in the request sent to
  the server) => S,clf:Str
* %k (Number of keepalive requests handled on this connection) => I:Num
* %l (Remote logname) => S:Str or S,clf:Str
* %m (The request method) => S:Str
* %{Foobar}n (The contents of note Foobar from another module) => S:Str or
  S,clf:Str
* %{Foobar}o (The contents of Foobar: header line(s) in the reply) => S,clf:Str
* %p (The canonical port of the server serving the request) => I:Num
* %{format}p (The canonical port of the server serving the request or
  the server's actual port or the client's actual port. Valid formats are
  canonical, local, or remote) => I:Num
* %P (The process ID of the child that serviced the request) => I:Num
* %{format}P (The process ID or thread id of the child that serviced
  the request. Valid formats are pid, tid, and hextid) => I:Num
* %q (The query string prepended with a '?' or a blank if there is no
  query) => S:Str
* %r (First line of request) => S,clf:Str or
  broken down as S:Str_method SEP:' ' S,clf:Str_page SEP:' ' S:Str_version
* %R (The handler generating the response) => S:Str
* %s or %>s (Status) => I:Num
* %t (Time the request was received in standard format) => I,tim:Num
* %{format}t => Not supported.
* %T (The time taken to serve the request, in seconds) => I:Num
* %u (Remote user) => S:Str or S,clf:Str
* %U (The URL path requested, not including any query string) => S:Str
* %v (The canonical ServerName of the server serving the request) => S:Str
* %V (The server name according to the UseCanonicalName setting) => S:Str
* %X (Connection status when response is completed - 'X', '+' or '-') => S:Str
* %I (Bytes received, including request and headers) => I:Num
* %O (Bytes sent, including headers) => I:Num

Separator specs must be added to complete the record description.
For example, consider this Common Log Format spec string:

 ::

  %h %l %u %t \"%r\" %>s %b

It can be represented by these column spec:

 ::

  IP:h SEP:' ' S:l SEP:' ' S:u SEP:' [' I,tim:t SEP:'] "'
  S,clf:r SEP:'" ' I:s SEP:' ' I:b

or

 ::

  IP:h SEP:' ' S:l SEP:' ' S:u SEP:' [' I,tim:t SEP:'] "'
  S:r_method SEP:' ' S,clf:r_page SEP:' ' S:r_version SEP:'" ' I:s SEP:' ' I:b


See Also
========

* `jsncnv <jsncnv.html>`_ - JSON log converter
* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udbd <udbd.html>`_ - User (Bucket) Database server
* `aq_udb <aq_udb.html>`_ - Interface to Udb server

