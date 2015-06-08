======
prtrng
======


Synopsis
========

::

  prtrng [-h] Global_Opt Input_Spec Range_Spec

  Global_Opt:
      [-nolabel]

  Input_Spec:
      [-f File]

  Range_Spec:
      -b RngSpec [RngSpec ...] | -l RngSpec [RngSpec ...]


Description
===========

``prtrng`` reads an input file or stream and output selected ranges of data
from the input.
It is used to augment data processing program that output messages containing
byte or line ranges of certain data of interest but not the data themselves.
By passing the same input data and selected byte/line ranges to this program,
the data of interest can be inspected/sampled.

The program accepts either byte or line ranges (but not both).
Byte range is perferred if available as it is more efficient.
Output goes to stdout.


Options
=======

.. _`-nolabel`:

``-nolabel``
  Do not output data range label line.
  By default, a label line is printed before each block of selected data.
  See `Output Format`_ for details.


.. _`-f`:

``-f File``
  Set the input file.
  If the data come from stdin, set ``File`` to '-' (a single dash).
  If this option is not given, stdin is assumed.


.. _`-b`:

``-b RngSpec [RngSpec ...]``
  Specify the byte ranges of data to print.
  ``RngSpec`` specify a range in one of these forms:

  ``Pos``
    Select a single byte at ``Pos``.

  ``BegPos-EndPos``
    Select a range from ``BegPos`` to ``EndPos`` bytes, inclusive.

  ``BegPos+Num``
    Select ``Num`` bytes starting at ``BegPos`` (inclusive).

  Note that position starts at 1; that is, the first byte is 1.
  Although the program accepts any ``RngSpecs``, it is best to follow
  these rules:

  * They should be given in ascending order. If not, the program will
    silently reorder them automatically.
  * They should not overlap. If not, the program will emit a warning and
    try to eliminate the overlap automatically.
  * They should not be continuous. If not, the program will silently join
    consecutive ranges.

  Example:

   ::

    $ prtrng ... -f file1 -b 100+20 1000+10 ...

  * Print bytes 100 to 119 and 1000 to 1009 (inclusive) of file1.


.. _`-l`:

``-l RngSpec [RngSpec ...]``
  Same as `-b`_ except that lines are selected instead of bytes.


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


Output Format
=============

Output from the program appears this way:

 ::

  FileName: byte=BegByte+NumByte<newline>
  <selected data><newline>

or

 ::

  FileName: line=BegLine+NumLine<newline>
  <selected data><newline>

The first line is a *label* line. FileName comes from `-f`_.
A byte range is shown if `-b`_ was used
and a line range is shown if `-l`_ was used.

* The range shown is the *intended* range. It may differ from the range of
  data that follows. For example, if the input ends before the
  desired range is satisfied, the amount of data printed will be less.
* The label line can be suppressed with `-nolabel`_.

The subsequent block contains the selected data.

* The ending <newline> is added by the program when an entire range is
  satisfied. It is not printed if the input ends before a range is satisfied.
* If the selected data also ends with a <newline>, the added <newline> will
  appear as a blank line. It is not an error.
* If the selected data does not end with a <newline>, the added <newline>
  will cause a line break, making the output more readable. Although the
  output looks normal in this case, one should note that the data is not
  <newline> terminated.


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udbd <udbd.html>`_ - User (Bucket) Database server
* `aq_udb <aq_udb.html>`_ - Interface to Udb server

