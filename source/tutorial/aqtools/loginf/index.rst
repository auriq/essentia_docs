*************
File Analyzer
*************

It is not uncommon for data scientists to spend a significant amount of time determining properties about a data set.
``loginf`` was developed to assist in the process.  It scans a file and determines:
* column names
* type of each column (string, int, etc)
* number of records
* estimate of the number of unique values in the column

``loginf`` uses an O(N) algorithm to determine these properties.  In particular the uniqueness estimate is based on an
algorithm which results in an answer that is accurate to within a few percent.

Usage
=====

We will look at a simple 3 column file (:download:`donations.csv`) that record the last name, city, and amount donated
to a fictional charity.  In the rawest form, one can execute the following to get the full output::

  loginf -f donations_1.csv

  Sources = 1
  Process Time = 0.000
  Original Bytes = 228
  Analyzed Bytes = 228 (100.00% Original)
  Original Lines = 11
  Analyzed Lines = 11 (100.00% Original)
  Rows = 11
  Row Length Min|Max|Avg = 15|31|20.7273
  Columns Min|Max = 3|3
  Column.1
    Value Bytes = 72 (31.58% Analyzed)
    Count = 11 (100.00% Rows)
    Value Length Min|Max|Avg = 4|9|6.54545
    Unique Estimate = 11
    Type.String
      Occurrence = 11 (100.00% Count)
      Sample.1 = [8]lastname
      Sample.2 = [9]Henderson
      Sample.3 = [4]Long
      Sample.4 = [9]Alexander
  Column.2
    Value Bytes = 95 (41.67% Analyzed)
    Count = 11 (100.00% Rows)
    Value Length Min|Max|Avg = 4|18|8.63636
    Unique Estimate = 11
    Type.String
      Occurrence = 11 (100.00% Count)
      Sample.1 = [4]city
      Sample.2 = [4]Ngou
      Sample.3 = [15]Lendangara Satu
      Sample.4 = [9]Carazinho
      Sample.Has binary = [18]Oborniki Śląskie
  Column.3
    Value Bytes = 28 (12.28% Analyzed)
    Count = 11 (100.00% Rows)
    Value Length Min|Max|Avg = 2|8|2.54545
    Unique Estimate = 10
    Type.String
      Occurrence = 1 (9.09% Count)
      Sample.1 = [8]donation
    Type.Integer
      Occurrence = 10 (90.91% Count)
      Numeric Min|Max = 25|50
      Sample.1 = [2]26
      Sample.2 = [2]27
      Sample.3 = [2]31
      Sample.4 = [2]35

``logcnv`` breaks down each column.  Note column three which is the numerical column.  Since at first ``logcnv`` does
not know if there is a header line, it identifies that 1/11 entries are strings, while the other 10/11 are integers.

This is used for determining the column specification used in other AQ commands::

  loginf -f donations_1.csv -o_pp_col -

  S:lastname
  S:city
  I:donation

It is extremely helpful when integrating new datasets with the AQ tools.

Other Notes
===========

This utility also has the ability to store the output in a raw form that can be used to merge results from several
files.  This is most useful when an estimate of uniqueness is needed from a column in a set of log files that span a
length of time.  Refer to the ``loginf`` manual for the full syntax.
