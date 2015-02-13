========
udb-size
========

--------------------------------
Udb server storage size estimate
--------------------------------

:Copyright: AuriQ Systems Inc.
:Manual group: Udb
:Manual section: 5
:Date: 2015-01-28
:Version: 1.2.1


Description
===========

An Udb server holds its data in memory. A database can either be held by
a single server or a pool of servers. The number of servers to use must be
determined before populating the database.

A crude estimate is the input data size itself. For example, if the data size
is 100GB (uncompressed size), and each server has 16GB available, 7 servers
are needed.
This is simple, but also very inacurrate.
A better way to estimate the amount memory needed per server is
outlined below. It depends mainly on the database definition
and the characteristics of the data set to be processed.

Database definition related parameters can be obtained from `udb.spec <udb.spec.html>`_.
Data characteristics related parameters can be obtained from the report
produced by `loginf <loginf.html>`_ on the data set (or part of it).


Parameters
==========

Parameters needed for the estimate:

.. _`ptr_z`:

``ptr_z``
  The *pointer size*, an intrinsic software overhead.

   * ptr_z = 4 on a 32 bit platform
   * ptr_z = 8 on a 64 bit platform

.. _`Num_server`:

``Num_server``
   The number of servers in the pool, one or more.

.. _`Num_row`:

``Num_row``
  The overall row count of a table in the data set.
  This is a table specific characteristic.

.. _`Num_string_per_server`:

``Num_string_per_server``
  Strings are hashed so that only the unique ones are stored.
  Strings come from the string columns, excluding the PKEY column.
  ``Num_string_per_server`` is the unique string count per server.
  It is usually less than its overall unique count in a data set,
  but it does not scale linearly with the number of servers.
  In fact, the overall unique count is often a good estimate.

.. _`Avg_string_length`:

``Avg_string_length``
  The average unique string length on a server.
  It should be a per-server estimate;
  however, it is often independent of the number of servers
  so that the overall average can be used.

.. _`Num_bucket`:

``Num_bucket``
  The overall unique PKEY count in the data set.

.. _`Avg_num_pluskey`:

``Avg_num_pluskey``
  The average unique pluskey count per bucket of a table.
  This is a table specific characteristic.
  It should be a per-server estimate;
  however, it is often independent of the number of servers
  so that the overall average can be used.

.. _`Num_vector`:

``Num_vector``
  Number of vectors in the data definition.

.. _`Num_table_with_pluskey`:

``Num_table_with_pluskey``
  Number of tables having a +KEY in the data definition.

.. _`Num_table`:

``Num_table``
  Number of tables in the data definition, excluding vectors and the Var table.

.. _`Num_vector_and_table`:

``Num_vector_and_table``
  Number of vectors and tables in the data definition, excluding the Var table.


Estimation
==========

The amount of memory needed by each server in a pool is the sum of
these constributions:

1) Table rows

   * Per_column_size:

     * I, IS = 4
     * F, L, LS = 8
     * IP = 20
     * S = ptr_z (strings are stored in a hash table, only pointers to the hash
       entries are stored in a row)

   * Total_column_size =

      ::

       Sum_over_columns(Per_column_size)

     excluding PKEY column.

   * Per_row_padding:

     * Up to 8 bytes on a 32 bit platform.
     * Up to 4 bytes on a 64 bit platform.

   * Per_table_size_per_server =

      ::

       Num_row * (Total_column_size + Per_row_padding) / Num_server

   * **Total_row_size_per_server** =

      ::

       Sum_over_tables(Per_table_size_per_server)

2) Strings

   * Hash_size_per_server:

     * (2M * ptr_z) for up to (2M * 12) Num_string_per_server
     * (16M * ptr_z) for up to (16M * 12) Num_string_per_server
     * (128M * ptr_z) max

   * Per_string_size =

      ::

       ptr_z + 6 + Avg_string_length

     rounded up to nearest multiple of ptr_z.

   * **Total_string_size_per_server** =

      ::

       Hash_size_per_server + (Num_string_per_server * Per_string_size)

3) User buckets

   * Num_bucket_per_server =

      ::

       Num_bucket / Num_server

   * Hash_size_per_server:

     * (2M * ptr_z) for up to (2M * 12) Num_bucket_per_server
     * (16M * ptr_z) for up to (16M * 12) Num_bucket_per_server
     * (128M * ptr_z) max

   * Vector_flag_size =

      ::

       Num_vector * 1

     rounded up to nearest multiple of ptr_z.

   * Per_bucket_size =

      ::

       ptr_z + 6 + Avg_pkey_length +
       Vector_flag_size +
       Num_table_with_pluskey * (8 + ptr_z) +
       Num_table * ptr_z +
       Num_vector_and_table * ptr_z

   * **Total_bucket_size_per_server** =

      ::

       Hash_size_per_server + (Num_bucket_per_server * Per_bucket_size)

4) Pluskey (+KEY) overhead

   * Hash_size_per_table (per bucket):

     * 0 for up to (1 * 16) Avg_num_pluskey
     * (8 * ptr_z) for up to (8 * 16) Avg_num_pluskey
     * (8^n * ptr_z) for up to (8^n * 16) Avg_num_pluskey
     * (16M * ptr_z) max

   * Per_pluskey_overhead =

     * 8 on a 32 bit platform
     * 16 on a 64 bit platform

   * Per_pluskey_table_overhead (per bucket) =

      ::

       Hash_size_per_table + (Avg_num_pluskey * Per_pluskey_overhead)

   * **Total_pluskey_overhead_per_server** =

      ::

       Num_bucket_per_server * Sum_over_pluskey_tables(Per_pluskey_table_overhead)

**Total_storage_per_server** =

 ::

  Total_row_size_per_server +
  Total_string_size_per_server +
  Total_bucket_size_per_server +
  Total_pluskey_overhead_per_server


See Also
========

* `udbd <udbd.html>`_ - User (Bucket) Database server
* `udb.spec <udb.spec.html>`_ - Udb spec file.
* `loginf <loginf.html>`_ - Log analyzer

