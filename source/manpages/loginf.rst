.. -*- mode: rst -*-

==========================
loginf
==========================
-------------------------------------------------------------
AuriQ text log analyzer
-------------------------------------------------------------
:Author:  myeung@auriq.com
:organization: AuriQ Systems Inc.
:Address: 199 S Los Robles Avenue
          Suite 440
          Pasadena, CA, 91101
:Date: January 28, 2015
:Copyright: AuriQ Systems Inc.
:Manual section: 1
:Manual group: text processing
:Version: 1.2.0

.. raw:: manpage

   .\" disable justification (adjust text to left margin only)
   .ad l

SYNOPSIS
========
|  ``loginf`` [-h] [Global options] [Input options] [Output Options]
|
|  Global_Opt:
|    [-test] [-verb] [-bz ReadBufSiz]
|  Input_Spec:
|    [-f[,AtrLst] File [File ...]] [-lim Num]
|    [-f_raw File [File ...]]
|  Output_Spec:
|    [-o File]
|    [-o_raw File]
|    [-o_pp_col File]
|

DESCRIPTION
============
Process one or more CSV log files and output the analysis as a text
report or raw result file.  Output contains metrics such as column
types, counts, row counts, data uniqueness and so on.


.. comment
  The output pages bear cutmarks and have slightly overlapping
  images for easier assembling.


OPTIONS
=======

-h  display a short usage summary

``-test``
  Test command line arguments and exit

``-verb``
  Verbose, print a marker to stderr for each 10 million lines of text processed.

``-bz``
  Input buffer size (in bytes) and maximum record length. Default is 65536
  (64KB).  If a record exceeds this length, the program will abort.

-f[,tsv]
  Designate the filenames to be processed (or "-" for stdin).  If neither -f
  or -f_raw are used, input is assumed to come from stdin. Files are assumed to
  be CSV (comma separated) or TSV (tab separated) if the ``,tsv`` attribute is
  used.

``-lim``
  Limit the number of records to process. Useful for getting 'good enough'
  results from large files.

``-f_raw``
  Designate the file names to be processed (or "-" for stdin).  Input files
  must be generated from this program.  This option is used to combine results
  from multiple runs, and is particularly useful for estimating uniquess of
  data in a column (see `EXAMPLES`_).

-o
  Output a text report to a file (or stdout if "-").  If neither -o or -o_raw
  is provided, output will default to stdout.

``-o_raw``
  Output the raw result to a file (or stdout if "-") for use in subsequent
  ``loginf`` calls.

``-o_pp_col``
  Output only the column specification based off the data.  If headers are
  present, the column names will use those, otherwise the labels are C1, C2,
  etc.  The format of the specification can be used directly by aq_pp.

EXIT STATUS
===========

Return codes are:

* 0 success (or in the case of the -test option, if all parameters are valid.)
* 1-9  Program initial preparation error.
* 10-19  Input file load error
* 20-29  Result output error


 Files are assumed to be CSV (comma separated) or TSV (tab separated) if the
 ``,tsv`` attribute is used Files are assumed to be CSV (comma separated) or
 TSV (tab separated) if the ``,tsv`` attribute is used.


.. NOTES
   =====

EXAMPLES
============

:loginf -f test.csv -o -:
    Analyze the file "test.csv" and output the results to the stdout.

:cat test.csv | loginf:
    Same as previous example, done via unix pipes.

:loginf -f test.csv -lim 10000 -o_pp_col -:
    Analyze the first ten thousand lines of "test.csv" and estimate the column
    specification.


SEE ALSO
========
`Essentia Home Page <www.auriq.net>`__

