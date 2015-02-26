:tocdepth: 2

******************
Reference Material
******************

This section provides additional tutorials, tables, and a copy of the man pages for the Essentia toolkit.

Manuals
=======
.. toctree::
   :maxdepth: 1

   manpages/index
   essentia-ref

Additional guides
=================
.. toctree::
   :maxdepth: 1

   loginf
   logcnv

Tables
======

**Table 1 :** Substitution strings for the Essentia 'stream' or 'exec' command.

============   =======================================
string         provides
============   =======================================
%num_nodes     number of nodes in cluster
%node_id       ID of the node executing the command
%num_threads   number of threads assigned per node
%thread_id     ID of the thread executing the command
============   =======================================

**Table 2:** Substitution strings for the Essentia 'stream' command.

=========   =======================
string      provides
=========   =======================
%path       path to file being processed
%file       file without extension
%FILE       file with extension
%tz         Timezone
%cols       Full column spec
%delim      Delimeter
%date_col   name of the date column
%date_fmt   format of date
=========   =======================

**Table 3:** UDB attribute flags for tables and vectors

=========  =============================================
attribute  use
=========  =============================================
pkey       primary hash key, must be string type
tkey       integer sorting key
+key       string key to merge on
+first     Use the first imported value when merging
+last      Use the last imported values when merging
+add       Sum values across rows for each unique value
+bor       Bitwise-OR numeric values
+min       Take the smallest value
+max       Take the largest value
+nozero    Ignore values of 0 or an empty string
=========  =============================================


