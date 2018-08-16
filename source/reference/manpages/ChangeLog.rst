.. |<br>| raw:: html

   <br>

===================
Change Log - V2.0.0
===================

:Replaces: V1.2.4
:Revision: V1.2.5-0 2016-12-07
:Revision: V1.2.5-1 2017-04-13
:Revision: V1.2.5-2 2017-11-02
:Revision: V1.2.5-3 2018-12-29
:Revision: V1.2.5-4 2018-02-12
:Revision: V2.0.0-0 2018-05-04
:Revision: V2.0.0-1 2018-06-18
:Revision: V2.0.0-2 2018-08-01


Introduction
============

The following sections list the category/command specific changes.
There are 4 kind of changes:

* [New] |<br>|
  Describe a new feature.

* [Warn] |<br>|
  An existing feature has changed. The old usage is still supported; however,
  applications should switch to the new usage as soon as possible.
  The old usage will be discontinued in the next release.

* [Critical] |<br>|
  An existing feature has changed in a non backward compatible manner.
  Applications must be ported to the new usage in order to use the new
  version.

* [Bug] |<br>|
  A bug was discovered and fixed.


Summary
=======

Incompatible changes:

* ``aq_ord`` no longer supports the *raw sort* mode. This mode was designed to
  the sort input data by column numbers without a column spec.
  However, its use cases were very limited, so the support was removed.
* To exclude a column in the ``-c`` column spec, only ``~ColName`` is accepted
  now, ``!ColName`` is no longer supported.
* The ``-rownum`` option of ``aq_pp`` is no longer supported.

New features:

* Support the *Perl Compatible Regular Expressions* (PCRE) engine in addition
  to the POSIX one. PCRE uses a syntax like POSIX's *extended* regex -
  i.e., it uses ``()`` without any backslashes for sub-expressions.
* Enhanced ``DateToTime()`` to handle sub-seconds.
* A new ``RxRep()`` function that works like ``RxReplace()`` but returns the
  result directly.
* More math functions - ``Sqrt()``, ``Cbrt()``, ``Log()``, ``Log10()``,
  ``Exp()``, ``Exp10()``, ``Pow()``.
* New substring comparison functions - ``BegCmp()`` ``EndCmp()``, ``SubCmp()``,
  ``SubCmpAll()``, ``MixedCmp()`` ``MixedCmpAll()``, ``Contain()``,
  ``ContainAll()``.
* New string obfuscation function ``MaskStr()``.
* New built-in evaluation variables ``$CurSec`` and ``$CurUSec`` for the
  current time.
* ``aq_pp`` can output to a target defined by a variable using
  ``-o,fvar VarName``. In other words, the output target can be dynamic.
* ``aq_pp`` supports a ``-cmb,mrg,...`` *merge* mode for
  combine data that is too large to fit into memory.
* ``aq_pp``, ``aq_ord`` and ``aq_cat`` can have multiple outputs with the same
  destination. This was allowed before but the result was not well defined.
* ``aq_udb -chk ...`` can be used to do spec file syntax check.
* ``aq_udb`` can sort output even when a sort column is not in the output.
* ``aq_udb`` ``-exp``, ``-cnt`` and ``-inf`` can have an ``asis`` attribute
  to output the individual results from all servers.
* New ``aq_udb`` ``-alt`` option to alter the definition of the Var vector
  after a database has been created.
* New ``aq_udb`` ``-inf`` option to output a database's key count and
  tables/vectors row counts.
* New ``aq_udb`` ``-key_rec`` option to limit the number of resulting rows
  per key.
* ``aq_udb`` ``-top`` can be used to limit the number of resulting rows
  without ``-sort``.
* ``aq_udb`` ``-exp`` and ``-cnt`` support the ``seg=N1[-N2]/N[:V]`` attribute
  for data sampling (like the same attribute for import).
* The ``-c`` output column spec of ``aq_pp``, ``aq_ord`` and ``aq_udb`` accepts
  a ``*`` to represent the default output column set.
* ``aq_ord`` supports case insensitive sorting with ``-sort,ncas,...``.
* ``aq_ord`` supports a block sort mode with ``-blk NumRec FilPrefix``.
  Use this mode when there is not enough memory for the entire data set.
* ``aq_ord`` supports a merge mode with ``-sort,mrg,...``. This will merge
  already sorted input files.
* Output columns specified under ``-c`` can have an output column name override
  as in ``-d ... i:c1 ... -c c1:c1_out_name+0x%x``. The format spec, if any,
  must be given after the name override.
* Most tools now support inputting from and outputting to named pipes and
  network sockets.
* Improved JSON parser EOK handling to save more records.
* Udb supports case insensitive ordering and sorting with ``-ord,ncas,...`` and
  ``-sort,ncas,...``.
* Udb handles out-of-descriptor condition gracefully. When this happens,
  ``aq_pp`` and ``aq_udb`` will show an "out of FD, connection failed" message.
* Udb server files (e.g., logs) will be created with the same permission as the
  server's runtime directory. In other words, these files will have a global
  read/write permission in a default installation.
* Udb server start/stop script (``udbd``) can handle ``<defunc>`` processes.
* Udb server supports an import memory allocation margin via environment
  ``UDBD_MEM_MARGIN``. An import will be aborted when the system's free memory
  drops below this limit.
* ``mcc.*`` enhancements.
* ``aq_cnt`` can output extended statistics (sum, average, standard deviation,
  minimum and maximum) in ``-kX`` reports.
  The ``-kX`` output can also be used as the input of a merge operation.
* ``loginf`` can handle input data in aq_tool's internal binary format either
  explicitly or automatically.

Changes to be enforced in a future release:

* ``aq_pp``:

  * ``-udb ... -imp ...`` --> ``-imp[,AtrLst] ...`` (``-udb`` not needed)
  * ``-ddef ... -imp ...`` --> ``-imp,ddef ...``
  * ``-map``, ``-mapf`` and ``-mapc`` --> ``RxMap()`` function
  * ``-kenc`` and ``-kdec`` --> ``KeyEnc()`` and ``KeyDec()`` functions
  * ``-alias`` will be removed.

* ``aq_udb``:

  * ``-pp ... -end_of_scan DestSpec ...`` --> ``-pp,post=DestSpec ...``
  * ``-lim_usr`` --> ``-lim_key``
  * ``next_bucket`` and ``proc_bucket`` --> ``next_key`` and ``proc_key``

* Evaluation functions:

  * ``KDec()`` --> ``KeyDec()``
  * ``QryParmExt()`` --> ``QryDec()``


Common
======
Cf: `aq_cat <aq_cat.html>`_, `aq_cnt <aq_cnt.html>`_, `aq_ord <aq_ord.html>`_, `aq_pp <aq_pp.html>`_, `aq_udb <aq_udb.html>`_, etc.

* [Bug] 1.2.5-2: |<br>|
  There was a bug in the "-filt" expression parser. It affects aq_pp and Udb
  when the negation group ``!()`` is used in these ways:

  * ``!( anything )`` - e.g., ``!(col==5)``
  * ``(!( anything ))`` - e.g., ``(!(col==5))``
  * ``(!( anything )) operator anything`` - e.g., ``(!(col==5))&&1``
  * ``anything operator (!( anything ))`` - e.g,, ``1&&(!(col==5))``

  These constructions can be used to circumvent the problem if necessary:

  * ``!( anything ) operator anything`` - e.g, ``!(col==5)&&1``, ``!(col==5)||0``
  * ``anything operator !( anything )`` - e.g, ``1&&!(col==5)``, ``0||!(col==5)``

* [Critical] 1.2.5-2: |<br>|
  To exclude a column in the ``-c`` column spec, only ``~ColName`` is accepted.
  ``!ColName`` is no longer supported. Having an alternate form (``!``) is not
  necessary. It is better to reserve the ``!`` mark for another use in the
  future.

* [New] 1.2.5-1/3: |<br>|
  The mapping options of ``aq_pp`` and regular expression related evaluation
  functions now support the *Perl Compatible Regular Expressions* (PCRE)
  engine in addition to the POSIX one. POSIX is still the default.
  PCRE can be selected at runtime in these ways:

  * Add a ``pcre`` to the mapping option's attribute (e.g., ``-map,pcre ...``).
  * Add a ``pcre`` to the evaluation function's attribute parameter.
  * Set the default regular expression processing attributes via the new
    ``-rx DefRgxAtr`` option of ``aq_pp`` and ``aq_udb (e.g., ``-rx pcre``).

* [New] 1.2.5-1/2/3/4: |<br>|
  Updated/new evaluation functions:

  * ``DateToTime()`` and ``GmDateToTime()`` can output deci-seconds to
    nano-seconds from decimal seconds with the ``%S1`` to ``%S9`` format spec.
  * ``RxRep()`` is similar to ``RxReplace()``, except that it returns the
    result directly.
  * ``AgentToUId()`` converts an agent string to an RTmetrics user ID.
  * ``UNameHash()`` converts a string (usually an user name) to an RTmetrics
    name hash.
  * ``Sqrt()``, ``Cbrt()``, ``Log()``, ``Log10()``, ``Exp()``, ``Exp10()`` and
    ``Pow()`` for square root, cube root, natural logarithm, base 10 logarithm,
    ``e`` (natural logarithm) base power, base 10 power and  abitrary power.

* [New] 2.0.0-0: |<br>|
  Updated/new evaluation functions:

  * ``IConv()`` can choose the best conversion to return. In this way, ``eok``
    can output a blank. A ``FromCode`` of ``-`` (a dash) can explicitly output
    a blank as fallback.
  * ``BegCmp()`` ``EndCmp()``, ``SubCmp()``, ``SubCmpAll()``,
    ``MixedCmp()`` ``MixedCmpAll()``, ``Contain()`` and ``ContainAll()``
    for substring comparisons.
  * ``MaskStr()`` irreversibly obfuscates a string with a high degree of
    uniqueness.

* [New] 2.0.0-0: |<br>|
  New built-in evaluation variables:

  * ``$CurSec`` and ``$CurUSec`` represent the current time in seconds and
    microseconds respectively.

* [New] 1.2.5-2: |<br>|
  ``aq_pp``, ``aq_ord`` and ``aq_cat`` can have multiple outputs with the same
  destination. For example, ``aq_pp ... -o outfile ... -o outfile ...`` will
  output each row to ``outfile`` twice, giving
  ``title,title,row1,row1,...,rowN,rowN,...``. Older versions also allow this
  kind of specs, but the result was not well defined.

* [New] 1.2.5-2: |<br>|
  Most tools now support inputting from and outputting to named pipes and
  network sockets.

  * Named pipes are used to connect the input/output of processes 
    running on the same machine. Example usages are
    ``aq_pp -f fifo@PipeName ...`` and ``aq_pp ... -o fifo@PipeName``
    where ``PipeName`` is the desired name of the input or output named pipe.
  * Sockets are used to connect the input/output of processes
    running on separated machines that are connected via a network.
    Example usages are
    ``aq_pp -f socket@IP:Port ...`` and ``aq_pp ... -o socket@IP:Port``
    where ``IP:Port`` is the IP address and port of the input or output socket.

* [New] 1.2.5-4: |<br>|
  Most tools now support inputting from worker nodes listed under a Udb spec's
  ``@server`` section. For example, ``aq_cat -f servers@DbName:port ...``.
  This is an experimental feature, so it is not documented yet.

* [New] 2.0.0-1: |<br>|
  ``aq_pp`` and ``aq_ord`` support the ``*`` column spec in ``-c`` - each ``*``
  represents the entire set of relevant default output columns.

* [New] 2.0.0-2: |<br>|
  Improved JSON parser EOK handling. More records can be saved if the JSON
  records are line-based.


aq_pp
=====
Cf: `aq_pp <aq_pp.html>`_

* See also `common`_ changes.

* [Bug] 1.2.5-2: |<br>|
  If a ``-cmb`` or ``-kdec`` action is executed conditionally
  (i.e., it is inside a ``-if`` block), columns derived from the action
  are not set if the action is not taken. In most cases, those column would
  retain the last values when the action was executed.
  With the bug fix, those columns will be initialized to 0 or blank if the
  action is not taken.

* [New] 1.2.5-2: |<br>|
  Support setting an output file using the value of a variable using
  ``-o,fvar VarName``. In this way, the output can be changed dynamically
  by changing the variable. When the value of the variable changes,
  the old output (based on the previous value of the variable) will be closed
  and the new one (based on the new value of the variable) will be opened.
  This is designed for infrequent switching only. Changing the value of the
  variable frequently is very inefficient.

* [New] 1.2.5-2: |<br>|
  Support ``-cmb,mrg,...`` *merge* mode. Records in the main data set and in
  the combine set must already be *sorted* in the same order.
  Default order is ascending. Use ``-cmb,mrg,dec`` if all the data are in
  descending order.
  This is designed to handle combine data that is too large to fit into memory.


aq_ord
======
Cf: `aq_ord <aq_ord.html>`_

* See also `common`_ changes.

* [New] 1.2.5-2: |<br>|
  Support case insensitive sorting with ``-sort,ncas,...``.

* [New] 1.2.5-2: |<br>|
  ``aq_ord`` supports a block sort mode with ``-blk NumRec FilPrefix`` or
  ``-blk_only NumRec FilPrefix``. In this mode,``aq_ord`` will load, sort and
  output ``NumRec`` at a time to ``FilPrefix-BlkNo.bin``. ``BlkNo`` is the
  output file number, it starts from 1 and increments for each ``NumRec``
  records until the entire input is consumed. Use this mode when the data set
  is too large to fit into memory all at once.

  * ``-blk`` performs the block sort and then loads and merges the results
    into a single output.
  * ``-blk_only`` performs the block sort onlt.
  
* [New] 1.2.5-2: |<br>|
  ``aq_ord`` supports a merge mode with ``-sort,mrg,...``. This will merge
  the inputs into a single sorted output. All the inputs must already
  be sorted in the same order as desired for the output. This option can be
  used to merge the output blocks from ``-blk`` and ``-blk_only``.


aq_cnt
======
Cf: `aq_cnt <aq_cnt.html>`_

* See also `common`_ changes.

* [New] 1.2.5-4: |<br>|
  Can output extended statistics (sum, average, standard deviation, minimum and
  maximum) of any associated numerical columns in ``-kX`` reports.
  The ``-kX`` output can also be used as the input of a merge operation
  that outputs the combined statistics.


aq_udb/udb server
=================
Cf: `aq_udb <aq_udb.html>`_, `udbd <udbd.html>`_

* See also `common`_ changes.

* [Bug] 1.2.5-1: |<br>|
  Under certain environment (e.g., ``docker``), the OS may leave zombie
  (aka, ``<defunc>``) processes behind. ``udbd`` (script) was not designed
  to handle this condition, So it would detect/report server status
  (running or not) incorrectly. This problem has been fixed.

* [New] 1.2.5-2: |<br>|
  Support case insensitive ordering and sorting with ``-ord,ncas,...`` and
  ``-sort,ncas,...`` of ``aq_udb``.

* [New] 1.2.5-2: |<br>|
  Support output sorting even when a sort column is not in the output.
  This condition was not allowed before.

* [New] 1.2.5-2: |<br>|
  Support shorthand column specs in ``-c`` that represent groups of columns in
  a table/vector - ``-c ... TabName.* ...`` includes all columns from a table
  of the given name, ``-c ... TabName.+ ...`` includes all columns except for
  the primary keys in the table, and similarly for vectors.

* [New] 1.2.5-3: |<br>|
  Udb handles out-of-descriptor condition gracefully. Previously, this error
  was silently ignored by the server and the condition could not be detected
  from the client side. Now, this error is logged in the server log as well as
  passed back to the client. When this happens,
  ``aq_pp`` and ``aq_udb`` will show an "out of FD, connection failed" message.

* [New] 2.0.0-0: |<br>|
  Udb server supports an import memory allocation margin via environment
  ``UDBD_MEM_MARGIN`` (Kb). A default margin of 500000K is applied if the
  environment is not set. If the system's free memory drops below this limit
  during an import, ``aq_pp`` will get an``out of memory`` server error.

* [New] 2.0.0-1: |<br>|
  ``aq_udb`` supports an ``asis`` attribute for Var export
  (i.e., ``aq_udb -exp,asis DbName:Var ...``), ``-cnt`` and ``-inf``.
  This will output the *individual* results from all the servers rather than
  a single set of combined result from them.

* [New] 2.0.0-2: |<br>|
  The ``-alt`` option can be used to alter the definition of the Var vector
  after a database has been created.

* [New] 2.0.0-2: |<br>|
  The ``-inf`` option can be used to to output a database's key count and
  tables/vectors row counts. Filters are not supported, but it is much faster
  than ``-cnt``.

* [New] 2.0.0-2: |<br>|
  The ``-key_rec`` option can be used to limit the number of resulting rows
  per key in an export operation.

* [New] 2.0.0-2: |<br>|
  The ``-top`` option can be used to limit the number of resulting rows
  in an export operation without ``-sort``.

* [New] 2.0.0-2: |<br>|
  ``aq_udb`` ``-exp`` and ``-cnt`` support the ``seg=N1[-N2]/N[:V]`` attribute
  for data sampling (like the same attribute for import). The sampling is
  repeatable since it is done based the keys' hash values.


loginf
======
Cf: `loginf <loginf.html>`_

* See also `common`_ changes.

* [New] 1.2.5-4: |<br>|
  Accept ``bin`` and ``aq`` input attribute to handle data in aq_tool's
  internal binary format. Can also detect this data format automatically with
  the ``auto`` input attribute.

