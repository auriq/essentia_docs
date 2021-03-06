:tocdepth: 2

******************
Attributes
******************

-------------------------------------------
UDB attribute flags for tables and vectors
-------------------------------------------

.. _`vec_attr`:

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

--------------------------------------------------------
Substitution strings for the Essentia 'stream' command.
--------------------------------------------------------

=========   =======================
string      provides
=========   =======================
%path       path to file being processed
%file       file without extension
%FILE       file with extension
%cols       Full column spec
%delim      Delimeter
=========   =======================

-------------------------------------------------------------------
Substitution strings for the Essentia 'stream' or 'exec' command.
-------------------------------------------------------------------

============   =======================================
string         provides
============   =======================================
%num_nodes     number of nodes in cluster
%node_id       ID of the node executing the command
%num_threads   number of threads assigned per node
%thread_id     ID of the thread executing the command
============   =======================================




