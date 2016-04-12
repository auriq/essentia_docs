.. |<br>| raw:: html

   <br>

=======
aq_sess
=======

Session count


Synopsis
========

::

  aq_sess [-h] Global_Opt Input_Spec Sess_Spec Output_Spec

  Global_Opt:
      [-verb] [-stat] [-bz ReadBufSiz]

  Input_Spec:
      [-f[,AtrLst] File [File ...]] -d ColSpec [ColSpec ...]

  Sess_Spec:
      -t ColName
      -k ColName [ColName ...]
      -tout SessEpxr
      [-ttol Tolerance]
      [-trim]

  Output_Spec:
      [-o[,AtrLst] File]


Description
===========

``aq_sess`` counts and reports sessions in a set of *events*.
The events must satisfy these requirements:

* Contain one or more columns for use as the identification *key*
  (e.g., an user ID).
* Contain one numeric column for use as the event *time*
  (e.g., time in UNIX seconds).
* Events must be in ascending *time* order.

During processing, sessions are compiled and reported.
Reported information for each session includes:

* Values of the columns forming the *key*.
* Session start time obtained from the first event in the session.
* Session end time obtained from the last event in the session.
* Session length.
* Number of events in the session.

Even though the input events are in time order, the output session records
will not be in any particular order.

This program only stores unfinished sessions in memory.
Completed ones are flushed (output) and cleared from memory periodically.
With this design, the amount of memory needed is determined by the number of
concurrent sessions per unit time and not the data size. In other words,
the program can process an unlimited amount of data using a constant
amount of memory.


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

    aq_sess: rec=Count err=Count out=Count


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

    $ aq_sess ... -f,+1l,eok file1 -f file2 ...

  * File1 and file2 can have different attributes.


.. _`-d`:

``-d ColSpec [ColSpec ...]`` or |<br>| ``-d [SepSpec] ColSpec [[SepSpec] ColSpec ...]``
  Define the columns in the input records from all the `-f`_ specs.
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

  Optional ``AtrLst`` is used in conjunction with the `input file attributes`_
  to determine how column data are to be extracted from the input.
  It is a comma separated list containing:

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
  or more bytes. A ``SepSpec`` is generally needed between two adjacent
  ``ColSpec`` unless the former column has a length spec.

  Example:

   ::

    $ aq_sess ... -d s:Col1 s,lo:Col2 i,trm:Col3 ...

  * Col1 is a string. Col2 is also a string, but the input value will be
    converted to lower case. Col3 is an unsigned integer, the ``trm``
    attribute removes blanks around the value before it is converted to
    an internal number.

   ::

    $ aq_sess ... -d sep:' [' s:time_s sep:'] "' s,clf:url sep:'"' ...

  * This parses data of the form: [01/Apr/2016:01:02:03 +0900] "/index.html".


.. _`-t`:

``-t ColName``
  Mandatory.
  Define the name of the *time* column. It must be of type ``I``.


.. _`-k`:

``-k ColName [ColName ...]``
  Mandatory.
  Define one or more columns that form the *key*.


.. _`-tout`:

``-tout SessExpr``
  Mandatory.
  Set the session inactivity timeout.
  It must be in the same unit as the *time* column (from `-t`_).
  Sessions inactive for a period *longer* than this time will be closed.
  An output session record is generated when a session is closed.

  Example:

   ::

    $ aq_sess ... -d i:Time s:Col2 ip:Col3 ...
        -t Time -k Col2 Col3 -tout 1800 ...

  * Set the *time* column to Time, *key* columns (composite) to Col2 and Col3,
    and session expiration to half an hour.


.. _`-ttol`:

``-ttol Tolerance``
  Set optional out-of-order time tolerance.
  It must be in the same unit as the *time* column (from `-t`_).
  With this, the *time* column can be out of ascending order by up to
  ``Tolerance`` amount.
  If a record is out-of-order within this limit, its *time* value
  will be set to the last in-order time.
  If a record exceeds this out-of-order limit, the program will **stop**.
  The default limit is 0, meaning that the record must be in order.


.. _`-trim`:

``-trim``
  Discard possible partial sessions at the beginning and end of the imput.
  This is because session start cannot be accurately determined before
  ``SessExpr`` (see `-tout`_) after the beginning of input.
  Similarly, session end cannot be accurately determined after
  ``SessExpr`` (see `-tout`_) before the end of input.


``-o[,AtrLst] File``
  Set the output attributes and file for the session records.
  Session records have the form:

   ::

    "ColName","ColName",...,"TBeg","TEnd","DT","PV"
    ColVal,ColVal,...,Num,Num,Num,Num
    ...

  where

  * "ColNames" are the columns from `-k`_.
  * "TBeg" is the session start time.
  * "TEnd" is the session end time.
  * "DT" is the session length (TEnd - TBeg).
  * "PV" is the number of events in the session.

  If ``File`` is a '-' (a single dash), data will be written to stdout.
  Optional ``AtrLst`` is described under `Output File Attributes`_.

  If this option is not given, data is written to stdout.

  Example:

   ::

    $ aq_sess ... -o,esc,noq -

  * Output to stdout in a format suitable for Amazon Cloud.


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

Each input option can have a list of comma separated attributes that control
input processing.

Positioning the start of input:

* ``+Num[b|r|l]`` - Specifies the number of bytes (``b`` suffix), records (``r``
  suffix) or lines (``l`` suffix) to skip before processing.
  Line is the default.

Error handling:

* ``eok`` - Make input error non-fatal. If there is an input parse error,
  program will try to skip over bad/broken record. If there is an input data
  processing error, program will just discard the record.
* ``qui`` - Quiet; i.e., do not print any input error message.

Input formats  - these attributes are mutually exclusive except for
``sep=c`` and ``csv`` that can be used together:

* ``sep=c`` or ``sep=\xHH`` - Input is in 'c' (single byte) separated value
  format. '\\xHH' is a way to specify 'c' via its HEX value ``HH``.
* ``csv`` - Input is in CSV format. This is the only format that supports
  quoted data fields. Although CSV implies *comma separated*,
  ``sep=c`` can be used to override this.
* ``fix`` - Input columns are all fixed width *without* any separator.
  Individual column widths are set in the ``n=Len``
  `column spec attribute <-d_>`_.
* ``tab`` - Input is in HTML table format. Columns must be enclosed in
  "``<td>data</td>``" or "``<td ...>data</td>``" and rows must be terminated
  by a "``</tr>``".
* ``bin`` - Input is in aq_tool's internal binary format.

These are used in conjunction with the `column spec attributes <-d_>`_:

* ``esc`` - '\\' is an escape character in input fields.
* ``noq`` - No quotes around fields in ``csv`` format.

If no input format attribute is given, ``csv`` is assumed.


Output File Attributes
======================

Each output option can have a list of comma separated attributes:

* ``notitle`` - Suppress the column name label row from the output.
  A label row is normally included by default.
* ``app`` - When outputting to a file, append to it instead of overwriting.
* ``sep=c`` or ``sep=\xHH`` - Output in 'c' (single byte) separated value
  format. '\\xHH' is a way to specify 'c' via its HEX value ``HH``.
* ``csv`` - Output in CSV format. Strings will be quoted. The default
  separator is comma, but ``sep=c`` can be used to override this.
* ``bin`` - Output in aq_tool's internal binary format.
* ``esc`` - Use '\\' to escape the field separator, '"' and '\\' (non binary).
* ``noq`` - Do not quote string fields in ``csv`` format.
* ``fmt_g`` - Use "%g" as print format for ``F`` type columns. Only use this
  to aid data inspection (e.g., during integrity check or debugging).

If no output format attribute is given, ``csv`` is assumed.


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udbd <udbd.html>`_ - Udb server
* `aq_udb <aq_udb.html>`_ - Udb server interface

