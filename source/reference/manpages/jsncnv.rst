======
jsncnv
======


Synopsis
========

::

  jsncnv [-h] Global_Opt Input_Spec Output_Spec

  Global_Opt:
      [-test] [-verb] [-bz ReadBufSiz]

  Input_Spec:
      [-f[,AtrLst] File [File ...]] [-d ColSpec [ColSpec ...]]

  Output_Spec:
      [-o[,AtrLst] File] [-c ColName [ColName ...]]


Description
===========

*Deprecated in Essentia version 3.1.0.1. Use* :doc:`objcnv` *instead*.

``jsncnv`` is a stream-based log format converter.
It processes input log files with a given JSON field spec and
outputs the same data in CSV or binary format.

* The input must be a list of JSON records. Each record must be a
  JSON *object* (enclosed in "``{}``") or *array* (enclosed in "``[]``").
  Records can optionally be separated by blanks and/or a single comma.
* The JSON field spec defines which fields to extract from the records.
  It does not need to cover the entire input JSON object/array.
  Only the ones of interested are needed.
  See the `-d`_ option specification for details.
* Extracted fields from each record are presented as data columns on the
  output. Fields that are not found in a record are set to blank/zero.

With its stream-based design, ``jsncnv`` can process an unlimited amount of
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
  It must be large enough to hold *all* the extracted field values in
  string form from any one record in the input.
  If the extracted data exceed this length, the program may abort or
  simply skip the offending record depending on the
  `Input File Attributes`_.
  Default length is 64KB. Use this option if more data is expected.
  ``ReadBufSiz`` is a number in bytes.


.. _`-f`:

``-f[,AtrLst] File [File ...]``
  Set the input attributes and files.
  If the data come from stdin, set ``File`` to '-' (a single dash).
  Optional ``AtrLst`` is described under `Input File Attributes`_.
  If no `-f`_ option is specified, stdin is assumed.

  Example:

   ::

    $ jsncnv ... -f,+1l,eok file1 -f file2 ...

  * File1 and file2 can have different attributes.


.. _`-d`:

``-d ColSpec [ColSpec ...]``
  Define the data columns and their corresponding JSON field spec
  of the input records from all `-f`_ specs.
  ``ColSpec`` has the form ``Type[,AtrLst]:ColName:JsnSpec``.
  Up to 256 ``ColSpec`` can be defined.
  Supported ``Types`` are:

  * ``S`` - String.
  * ``F`` - Double precision floating point.
  * ``L`` - 64-bit unsigned integer.
  * ``LS`` - 64-bit signed integer.
  * ``I`` - 32-bit unsigned integer.
  * ``IS`` - 32-bit signed integer.
  * ``IP`` - v4/v6 address.

  Note that the type selected do not necessarily need to match that of
  the corresponding JSON field being extracted. For example, a JSON string
  can be extracted into a numeric column or vice versa as long as the
  conversion is valid.
  Optional ``AtrLst`` is a comma separated list containing:

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

  ``JsnSpec`` has the form ``KeyName[Index].KeyName[Index]....`` if each
  input record is an object or
  ``[Index].KeyName[Index].KeyName[Index]....`` if each
  input record is an array.
  Each ``KeyName`` (case insensitive) corresponds to an object key.
  The ``[Index]`` spec (the "[]" is part of the spec) is only needed when
  a key's value is an array;
  in this case, an index must be specified to select an element from the
  array (0 means the first element).

  Example:

   ::

    $ jsncnv ... -d S:Col1:Key1 I:Col2:Key2.Ary2[2] ...

  * This extracts 2 columns from an input JSON object containing at least
    these elements (line breaks, indentations and spaces are included for
    clarity):

   ::

    {
      "Key1" : "Val1",
      "Key2" : {
        "Ary2" : [
          Num1, Num2, Num3 ...
        ]
      }
    }


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

    $ jsncnv ... -d S:Col1:Key1 I:Col2:Key2.Ary2[2]
        -o OutAll.csv
        -o Out2.csv -c Col2

  * Output Col1 and Col2 to OutAll.csv (this is the default when no ``-c``
    is given with the ``-o``) and output only Col2 to Out2.csv.


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


See Also
========

* `logcnv <logcnv.html>`_ - CLF log converter
* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udbd <udbd.html>`_ - User (Bucket) Database server
* `aq_udb <aq_udb.html>`_ - Interface to Udb server

