The AQ Tools
------------

Written in ``C`` to achieve a high level of performance, the AQ tools are able to manipulate and transform raw input
data into a format more easily handled by other AQ or third party tools.  The key programs include:

aq_pp
  The text preprocessor and Extract-Transform-Load workhorse.  It can validate data,
  filter data based on customizable criterion, do string manipulation, perform math, and merge data from other files.
  In a nutshell, it takes raw, dirty data, and outputs clean, formatted data.

udb/aq_udb
  The UDB is a distributed, hash based, in-memory database.  Each compute node in a cluster is a memory bucket for
  UDB, and each node manages a unique set of keys.  ``aq_udb`` is the command line tool used to query the database. We
  will go into more details later, but essentially this enables a map/reduce style analysis of data.


loginf
  This tool reads the contents of a data file to determine number of rows/columns, the type of each column (string,
  float, etc), and also an estimate of the number of unique values in each column.  This tool is particularly handy
  for data exploration, where the format of the data is not known precisely a priori.
