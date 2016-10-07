.. |<br>| raw:: html

   <br>

======
aq_cat
======

Input multiplexer


Synopsis
========

::

  aq_cat [-h] Global_Opt Input_Spec Output_Spec

  Global_Opt:
      [-verb] [-stat]

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


.. _`-f`:

``-f[,AtrLst] File [File ...]``
  Set the input attributes and files.
  See the `aq_tool input specifications <aq-input.html>`_ manual for details.
  Note that the input sources are typically *streams*, as described under
  `Description`_.

  Example:

   ::

    $ aq_cat ... -f,+1l stream_1 stream_2 ...

  * Skip the first line from each stream before loading.


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

    $ aq_cat ... -d s:Col1 s,lo:Col2 i,trm:Col3 ...

  * Col1 is a string. Col2 is also a string, but the input value will be
    converted to lower case. Col3 is an unsigned integer, the ``trm``
    attribute removes blanks around the value before it is converted to
    an internal number.


.. _`-o`:

``[-o[,AtrLst] File] [-c ColName [ColName ...]]``
  Output data rows.
  Optional "``-o[,AtrLst] File``" sets the output attributes and file.
  See the `aq_tool output specifications <aq-output.html>`_ manual for details.

  Optional "``-c ColName [ColName ...]``" selects the columns to output.
  ``ColName`` refers to a column defined under `-d`_.
  A ``ColName`` can be preceeded with a ``~`` (or ``!``) negation mark.
  This means that the column is to be excluded.
  If no `-d`_ is given, the desired column numbers or number ranges
  (one-based) can specified instead (e.g "... -c 5-3 1 2 ...").
  Negation does not work on column number spec.
  Without ``-c``, all columns are selected by default.
  If ``-c`` is specified without a previous ``-o``, output will got to stdout.

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

