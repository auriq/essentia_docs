======
objcnv
======

XML/JSON Field Extractor


Synopsis
========

::

  objcnv [-h] Global_Opt Input_Spec Output_Spec

  Global_Opt:
      [-test] [-verb] [-stat] [-bz ReadBufSiz]
      -jsn|-xml

  Input_Spec:
      [-f[,AtrLst] File [File ...]] [-base BasSpec] [-d ColSpec [ColSpec ...]]

  Output_Spec:
      [-o[,AtrLst] File] [-c ColName [ColName ...]]


Description
===========

``objcnv`` is a stream-based data object field extractor.
It processes input log files with a given object structure and
outputs the selected data fields in CSV or binary format.

* Supported input formats are JSON and XML.
* The input should contain one or more records of the given type.

  * JSON records can optionally be separated by blanks/newlines and/or commas.
  * XML records *must* be separated by one or more blanks/newlines.

* Which fields to extract are defined by the *object field spec* from the
  command line options.
  There is no need to specify all the fields in the object, only the ones
  of interest.
  See the `-d`_ option specification for details.
* Extracted fields are presented as data columns on the output.
  Fields that are not found in an object set to blank/zero.
* Each object may result in one or more rows of outputs. For example,
  an array in a JSON object can result in multiple output rows per object.

With its stream-based design, ``objcnv`` can process an unlimited amount of
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


.. _`-stat`:

``-stat``
  Print a record count summary line to stderr at the end of processing.
  The line has the form:

   ::

    objcnv: rec=Count err=Count out=Count


.. _`-bz`:

``-bz ReadBufSiz``
  Set input buffer length.
  It must be large enough to hold *all* the extracted field values in
  string form from any one record in the input.
  If the extracted data exceed this length, the program may abort or
  simply skip the offending record depending on the
  `Input File Attributes`_.
  Default length is 64KB. Use this option if more data is expected.
  ``ReadBufSiz`` is a number in bytes.


.. _`-jsn`:

.. _`-xml`:

``-jsn|-xml``
  Set the input data format. This is a *required* option.

  * ``-jsn`` selects JSON format.
  * ``-xml`` selects XML format.


.. _`-f`:

``-f[,AtrLst] File [File ...]``
  Set the input attributes and files.
  If the data come from stdin, set ``File`` to '-' (a single dash).
  Optional ``AtrLst`` is described under `Input File Attributes`_.
  If no `-f`_ option is specified, stdin is assumed.

  Example:

   ::

    $ objcnv ... -f,+1l,eok file1 -f file2 ...

  * File1 and file2 can have different attributes.


.. _`-base`:

``-base BasSpec``
  Set an optional *base* for the ``ObjSpec`` in the column spec.
  It must be specified *before* `-d`_.

  ``BasSpec`` is a list of dot separated elements as in
  ``Element.Element....``. Each ``Element`` has the form:

  * ``KeyName`` denotes the value of an object member named ``KeyName``
    (case insensitive).
  * ``[*]`` denotes all values in an array.
  * ``KeyName[*]`` denotes all values in the array belonging to an object
    member named ``KeyName`` (case insensitive).

  See `Extraction Spec Examples`_ for usage examples.


.. _`-d`:

``-d ColSpec [ColSpec ...]``
  Define the data columns and their corresponding *object field spec*
  of the input records from all `-f`_ specs.
  ``ColSpec`` has the form ``Type[,AtrLst]:ColName:ObjSpec``.
  Up to 2048 ``ColSpec`` can be defined.
  Supported ``Types`` are:

  * ``S`` - String.
  * ``F`` - Double precision floating point.
  * ``L`` - 64-bit unsigned integer.
  * ``LS`` - 64-bit signed integer.
  * ``I`` - 32-bit unsigned integer.
  * ``IS`` - 32-bit signed integer.
  * ``IP`` - v4/v6 address.

  Note that the type selected do not necessarily need to match that of
  the corresponding field being extracted. For example, a JSON string
  can be extracted into a numeric column or vice versa as long as the
  conversion is valid.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``hex`` - For numeric type. Denote that the input field is in hexdecimal
    notation. Starting ``0x`` is optional. For example, ``100`` is
    converted to 256 instead of 100.
  * ``trm`` - Trim leading/trailing spaces from input field value.
  * ``lo``, ``up`` - For ``S`` type. Convert input field to lower/upper case.

  ``ColName`` is case insensitive. It can have up to 31 alphanumeric and '_'
  characters. The first character must not be a digit.

  ``ObjSpec`` specifies which data field to extract for the column.
  It is a list of dot separated elements as in
  ``Element.Element....``. Each ``Element`` has the form:

  * ``KeyName`` denotes the value of an object member named ``KeyName``
    (case insensitive).
  * ``[*]`` denotes all values in an array.
  * ``KeyName[*]`` denotes all values in the array belonging to an object
    member named ``KeyName`` (case insensitive).

  If `-base`_ is given, ``BasSpec`` will be prepended to each ``ObjSpec``.
  See `Extraction Spec Examples`_ for usage examples.


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

    $ objcnv ... -d S:Col1:key1 I:Col2:key2.ary[*]
        -o OutAll.csv
        -o Out2.csv -c Col2

  * Output Col1 and Col2 to OutAll.csv (this is the default when no ``-c``
    is given with the ``-o``) and output only Col2 to Out2.csv.


Extraction Spec Examples
========================

These are some examples that illustrate the use of the `-base`_ and
`-d`_ options on various source data sets.
Recall that
JSON records can optionally be separated by blanks/newlines and/or commas
while XML records *must* be separated by one or more blanks/newlines.
Note the `Extraction Limitation`_ described in the next section.

 ::

  {
    "Key1" : "Val1",
    "Key2" : { "Ary" : [ 0, 1, 2 ] }
  }

  $ objcnv -jsn ... -d S:Col1:key1 I:Col2:key2.ary[*] ...

* Extract 2 columns from the example JSON data - one from "key1",
  the other from all values of "key2.ary". The result will be "Val1,0",
  "Val1,1" and "Val1,2".

 ::

  <root>
    <Key1>Val1</Key1>
    <Key2>
      <Ary>0</Ary>
      <Ary>1</Ary>
      <Ary>2</Ary>
    </Key2>
  </root>

  $ objcnv -xml ... -d S:Col1:root.key1 I:Col2:root.key2.ary[*] ...

* Extract 2 columns from the example XML data - one from "key1",
  the other from all values of "key2.ary". The result will be "Val1,0",
  "Val1,1" and "Val1,2".

 ::

  { "k1" : { "k2" : { "k3" : { "k4" : "14", "k5" : "15" } } } }
  { "k1" : { "k2" : { "k3" : { "k4" : "24", "k5" : "25" } } } }
  { "k1" : { "k2" : { "k3" : { "k4" : "34", "k5" : "35" } } } }

  $ objcnv -jsn ... -d I:Col1:k1.k2.k3.k4 I:Col2:k1.k2.k3.k5 ...
  $ objcnv -jsn ... -base k1.k2.k3 -d I:Col1:k4 I:Col2:k5 ...

* Extract 2 columns from the example JSON data. The two commands are
  equivalent, extracting 3 rows of output - "14,15", "24,25" and "34,35".

 ::

  <k1><k2><k3><k4>14</k4><k5>15</k5></k3></k2></k1>
  <k1><k2><k3><k4>24</k4><k5>25</k5></k3></k2></k1>
  <k1><k2><k3><k4>34</k4><k5>35</k5></k3></k2></k1>

  $ objcnv -xml ... -d I:Col1:k1.k2.k3.k4 I:Col2:k1.k2.k3.k5 ...
  $ objcnv -xml ... -base k1.k2.k3 -d I:Col1:k4 I:Col2:k5 ...

* Extract 2 columns from the example XML data. The two commands are
  equivalent, extracting 3 rows of output - "14,15", "24,25" and "34,35".

 ::

  [
    { "k1" : { "k2" : { "k3" : { "k4" : "14", "k5" : "15" } } } },
    { "k1" : { "k2" : { "k3" : { "k4" : "24", "k5" : "25" } } } },
    { "k1" : { "k2" : { "k3" : { "k4" : "34", "k5" : "35" } } } }
  ]

  $ objcnv -jsn ... -base [*].k1.k2.k3 -d I:Col1:k4 I:Col2:k5 ...

* Extract 2 columns from the example JSON data. Produces ths same
  result as the previous example. Note the use of "``[*]``" in ``-base``
  to address all the objects in the top array.

 ::

  <k0>
  <k1><k2><k3><k4>14</k4><k5>15</k5></k3></k2></k1>
  <k1><k2><k3><k4>24</k4><k5>25</k5></k3></k2></k1>
  <k1><k2><k3><k4>34</k4><k5>35</k5></k3></k2></k1>
  </k0>

  $ objcnv -xml ... -base k0.k1[*].k2.k3 -d I:Col1:k4 I:Col2:k5 ...

* Extract 2 columns from the example XML data. Produces ths same
  result as the previous example. Note the use of "``[*]``" in ``-base``
  to address all the "k1" entries.

 ::

  { "k1" : { "k2" : { "k3" : [ { "k4" : "14", "k5" : "15" },
                               { "k4" : "24", "k5" : "25" } ] } } },
  { "k1" : { "k2" : { "k3" : [ { "k4" : "34", "k5" : "35" } ] } } }

  $ objcnv -jsn ... -base k1.k2.k3[*] -d I:Col1:k4 I:Col2:k5 ...

* Extract 2 columns from the example JSON data. Produces ths same
  result as the previous example. Note the use of "``[*]``" in ``-base``
  to address all the objects in the "k3" array.

 ::

  <k1><k2><k3><k4>14</k4><k5>15</k5></k3>
          <k3><k4>24</k4><k5>25</k5></k3></k2></k1>
  <k1><k2><k3><k4>34</k4><k5>35</k5></k3></k2></k1>

  $ objcnv -xml ... -base k1.k2.k3[*] -d I:Col1:k4 I:Col2:k5 ...

* Extract 2 columns from the example XML data. Produces ths same
  result as the previous example. Note the use of "``[*]``" in ``-base``
  to address all the objects in the "k3" elements.

 ::

  [
    { "k1" : { "k2" : { "k3" : [ { "k4" : "14", "k5" : "15" },
                                 { "k4" : "24", "k5" : "25" } ] } } },
    { "k1" : { "k2" : { "k3" : [ { "k4" : "34", "k5" : "35" } ] } } }
  ]

  $ objcnv -jsn ... -base [*].k1.k2.k3[*] -d I:Col1:k4 I:Col2:k5 ...

* Extract 2 columns from the example JSON data. Produces ths same
  result as the previous example. Note the use of two "``[*]``" in ``-base``
  to address all the objects in the top array and
  all the objects in the "k3" array.

 ::

  <k0>
  <k1><k2><k3><k4>14</k4><k5>15</k5></k3>
          <k3><k4>24</k4><k5>25</k5></k3></k2></k1>
  <k1><k2><k3><k4>34</k4><k5>35</k5></k3></k2></k1>
  </k0>

  $ objcnv -xml ... -base k0.k1[*].k2.k3[*] -d I:Col1:k4 I:Col2:k5 ...

* Extract 2 columns from the example XML data. Produces ths same
  result as the previous example. Note the use of two "``[*]``" in ``-base``
  to address all the "k1" entries and
  all the "k3" entries.

 ::

  [ 1,2 ]
  [ 3,4 ]

  $ objcnv -jsn ... -base [*] -d I:Col1: ...

  [ [ 1,2 ], [ 3,4 ] ]

  $ objcnv -jsn ... -base [*].[*] -d I:Col1: ...

  { "k1" : [ 1,2 ] }
  { "k1" : [ 3,4 ] }

  $ objcnv -jsn ... -base k1[*] -d I:Col1: ...

  <k1>1</k1>
  <k1>2</k1>
  <k1>3</k1>
  <k1>4</k1>

  $ objcnv -xml ... -base k1 -d I:Col1: ...

* The ``JsnSpec`` in a ``ColSpec`` can be blank if appropriate.


Extraction Limitation
=====================

There is one limitation regarding array extraction. The ``[*]`` specification
denotes that all elements of an array is to be extracted.
While this is true, it may not be possible to extract some other desired fields
when processing an array. This condition depends on the arrangement of the
source data. The order of the columns specified under `-d`_ does not affect
the result.

Consider an example from the last section:

 ::

  {
    "Key1" : "Val1",
    "Key2" : { "Ary" : [ 0, 1, 2 ] }
  }

  $ objcnv -jsn ... -d S:Col1:key1 I:Col2:key2.ary[*] ...

Extracting "key1" and "key2.ary" gives the expected result of "Val1,0",
"Val1,1" and "Val1,2". However, if the source data is arranged differently,
as in:

 ::

  {
    "Key2" : { "Ary" : [ 0, 1, 2 ] },
    "Key1" : "Val1"
  }

  $ objcnv -jsn ... -d S:Col1:key1 I:Col2:key2.ary[*] ...

The same command gives only ",0", ",1" and ",2" - i.e., the value of "key1" is
missing. This has to do with the *stream based* design of the tool -
it outputs one record for each value of *inner most* array "key2.ary".
However, "key1" is not known when "key2.ary" is processed, so it is given
an empty string value.
To illustrate further, consider:

 ::

  {
    "Key2" : { "Ary" : [ 0, 1, 2 ] },
    "Key1" : "Val1",
    "Key3" : { "Ary" : [ 10, 11, 12 ] }
  }

  $ objcnv -jsn ... -d S:Col1:key1 I:Col2:key2.ary[*] I:Col3:key3.ary[*] ...

The result will be ",0,0", ",1,0", ",2,0", "Val1,0,10", "Val1,0,11" and
"Val1,0,12". There are two inner most arrays of interest in this case.
The first 3 result rows come from "key2.ary", where "key1" and "key3.ary"
are not known.
The other result rows come from "key3.ary", where "key1" is known but
"key2.ary" is no longer in context.


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

Each input file can have these comma separated attributes:

* ``eok`` - Make error non-fatal. If there is an input error, program will
  try to skip over bad/broken records. If there is a record processing error,
  program will just discard the record.
* ``qui`` - Quiet; i.e., do not print any input/processing error message.
* ``+Num[b|r|l]`` - Specifies the number of bytes (``b`` suffix), records (``r``
  suffix) or lines (no suffix or ``l`` suffix) to skip before processing.


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

