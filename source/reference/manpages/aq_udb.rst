======
aq_udb
======


Synopsis
========

::

  aq_udb [-h] Global_Opt Export_Spec|Order_Spec|Mnt_Spec

  Global_Opt:
      [-test] [-verb] [-stat] [-tag TagLab]
      [-spec UdbSpec | -db DbName]
      [-server AdrSpec [AdrSpec ...]]
      [-local]

  Export_Spec:
      -exp [DbName:]TabName | -cnt [DbName:]TabName | -scn [DbName:]TabName
        | -exp_usr | -cnt_usr | -scn_usr
      [-seed RandSeed]
      [-lim_usr Num] [-lim_rec Num]
      [-var ColName Val]
      [-filt FilterSpec]
      [-mod ModSpec]
      [-pp TabName
        [-pp_var ColName Val]
        [-pp_evlc ColName Expr]
        [-pp_filt FilterSpec]
        [-pp_goto DestSpec]
        [-pp_end_of_scan DestSpec]
      ]
      [-o[,AtrLst] File] [-c ColName [ColName ...]] [-notitle]
      [-sort [ColName ...] [-dec] [-top Num]]

  Order_Spec:
      -ord [DbName:]TabName [ColName ...] | -ord_all [-dec]

  Mnt_Spec:
      -clr [DbName:]TabName | -clr_all | -probe


Description
===========

``aq_udb`` is a client of the Udb server.
It is used to send command to the server (or a pool of servers)
to manipulate and/or export the data held by the server.
It can also instruct the server to clear a portion or all of the held
data.

Data manipulation can be done using builtin options or through a custom
*module* that is dynamically loaded on the server side.

**Note**: Data import to the Udb server is done by `aq_pp <aq_pp.html>`_.


Options
=======

.. _`-test`:

``-test``
  Test command line arguments and exit.
  If specified twice (``-test -test``), a more throughout test will be
  attempted. For example, the program will try to
  connect to Udb in test mode.

  * If all specs are good, the exit code will be 0.
  * If there is an error, the exit code will be non-zero. Usually, an error
    message will also be printed to stderr.
    connect to remote servers, and so on.


.. _`-verb`:

``-verb``
  Verbose - print program progress to stderr while processing.
  Usually, a marker is printed for each 10,000,000 records processed.


.. _`-stat`:

``-stat``
  Print a record count summary line to stderr at the end of processing.
  The line has the form:

   ::

    aq_udb:TagLab rec=Count


.. _`-tag`:

``-tag TagLab``
  Set label used to tag output messages. Default is blank.
  Currently, it is only used in:

  * The `-stat`_ summary line.
  * Final error message before program aborts.


.. _`-db`:

``-spec UdbSpec`` | ``-db DbName``
  Set the Udb spec file to ``UdbSpec``.
  Alternatively, "``-db DbName``" indirectly sets the spec file to
  to ".conf/``DbName``.spec" in the current work directory.
  If neither option is given,  ``DbName`` can be given in a later
  `-exp`_, `-cnt`_, `-scn`_, `-ord`_  or `-clr`_ option.
  If no spec file is given at all, "udb.spec" in the current work directory
  is assumed.

  The spec file contains server IPs (or domain names) and table/vector
  definitions.
  See `udb.spec <udb.spec.html>`_ for details.


.. _`-server`:

``-server AdrSpec [AdrSpec ...]``
  Set the target servers.
  If given, server spec in the Udb spec file will be ignored.
  ``AdrSpec`` has the form ``IP_or_Domain[|IP_or_Domain_Alt][:Port]``.
  See `udb.spec <udb.spec.html>`_ for details.


.. _`-local`:

``-local``
  Tell the program to connect to the *local* servers only.
  Local servers are those in the server spec (from the Udb spec file or
  `-server`_ option) whose IP matches the the local
  IP of the machine the program is running on.


.. _`-exp`:

``-exp [DbName:]TabName``
  Export the table rows from ``TabName``.
  ``TabName`` refers to a table/vector defined in the Udb spec file.
  ``TabName`` is case insensitive. It must not exceed 31 bytes long.
  Optional ``DbName`` sets the Udb spec file as in the `-db`_ option.


.. _`-cnt`:

``-cnt [DbName:]TabName``
  Retrieve the unique user count and row count for ``TabName``.
  ``TabName`` refers to a table/vector defined in the Udb spec file.
  ``TabName`` is case insensitive. It must not exceed 31 bytes long.
  Optional ``DbName`` defines UdbSpec indirectly as in the `-db`_ option.


.. _`-scn`:

``-scn [DbName:]TabName``
  Scan the table rows of ``TabName``.
  There is no default output.
  However, if used with a module (see `-mod`_),
  the module can optionally output custom data.
  ``TabName`` refers to a table/vector defined in the Udb spec file.
  ``TabName`` is case insensitive. It must not exceed 31 bytes long.
  Optional ``DbName`` sets the Udb spec file as in the `-db`_ option.

  This option should be used with a module (see `-mod`_) that operates on the
  table being scanned. Otherwise, use `-scn_usr`_ instead. `-pp`_ rules can
  also be used besides the module.


.. _`-exp_usr`:

``-exp_usr``
  Export the user keys (the common "PKEY" column).


.. _`-cnt_usr`:

``-cnt_usr``
  Retrieve the user count.


.. _`-scn_usr`:

``-scn_usr``
  Scan the user buckets.
  There is no default output.
  However, if used with a module (see `-mod`_),
  the module can optionally output custom data.

  This option should be used with `-pp`_ rules and/or a module (see `-mod`_)
  to operate on the data in each bucket.


.. _`-seed`:

``-seed RandSeed``
  Set the seed of random sequence used by the ``$Random``
  `-pp_evlc`_ builtin variable.


.. _`-lim_usr`:

``-lim_usr Num``
  Limit export output to the given Num users. Default is 0, meaning no limit.


.. _`-lim_rec`:

``-lim_rec Num``
  Limit export output to the given Num records. Default is 0, meaning no limit.


.. _`-var`:

``-var ColName Val``
  Set the value of Var vector column ``ColName`` to ``Val``.
  A Var vector must be defined in the Udb spec file and ``ColName``
  must be a column in that table.
  See `udb.spec <udb.spec.html>`_ for details.
  ``Val`` is the literal value to initialize the column to
  (``Val`` is not an expression, there is no need to enclose
  a string value in double quotes).

  * Var columns can also be altered by `-pp_var`_, `-pp_evlc`_ and
    modules (see `-mod`_).
  * Var column values are persistent until a `-clr`_ ``var`` or `-clr_all`_
    operation, at which point Var columns are reset to 0 or blank.

  Example:

   ::

    $ aq_udb ... -var Var1 0 ...

  * Initialize Var1 in Var vector to 0 before any buctet is processed.


.. _`-filt`:

``-filt FilterSpec``
  For each row in the table being exported/counted/scanned,
  evaluate ``FilterSpec`` and use the result to determine whether to
  keep the data row. 
  The result can also be used in a ``-if/-elif/-endif`` for
  `Rule Execution Controls`_.

  ``FilterSpec`` is the filter to evaluate.
  It is evaluated on each data row in the target table according to the
  `Data Processing Steps`_.
  It has the basic form ``LHS <compare> RHS``.
  LHS can be a column name or an expression to evaluate:

  * The column can be part of the target table or the Var vector.
    The name is case insensitive.
  * Evaluation has the form ``Eval(Expr)`` where ``Expr`` is the expression
    to evaluate as in `-pp_evlc`_.

  RHS can be a column name or a constant:

  * The column can be part of the target table or the Var vector.
    The name is case insensitive.
  * A constant can be a string, a number or an IP address.
    A string constant must be quoted with double quotes.

  Supported comparison operators are:

  * ``==``, ``>``, ``<``, ``>=``, ``<=`` -
    LHS and RHS comparison.
  * ``~==``, ``~>``, ``~<``, ``~>=``, ``~<=`` -
    LHS and RHS case insensitive comparison; string type only.
  * ``!=``, ``!~=`` -
    Negation of the above equal operators.
  * ``~~`` -
    LHS value matches RHS pattern. LHS must be a string column and
    RHS must be a literal pattern spec containing '*' (any number of bytes)
    and '?' (any 1 byte).
  * ``~~~`` -
    Same as ``~~`` but does case insensitive match.
  * ``!~``, ``!~~`` -
    Negation of the above.
  * ``##`` -
    LHS value matches RHS regex. LHS must be a string column and
    RHS must be a literal GNU RegEx.
  * ``~##`` -
    Same as ``##`` but does case insensitive match.
  * ``!#``, ``!~#`` -
    Negation of the above.
  * ``&=`` -
    Perform a "(LHS & RHS) == RHS" check; numeric types only.
  * ``!&=`` -
    Negation of the above.
  * ``&`` -
    Perform a "(LHS & RHS) != 0" check; numeric types only.
  * ``!&`` -
    Negation of the above.

  More complex expression can be constructed by using ``(...)`` (grouping),
  ``!`` (negation), ``||`` (or) and ``&&`` (and).
  For example:

   ::

    LHS_1 == RHS_1 && !(LHS_2 == RHS_2 || LHS_3 == RHS_3)

  In a quoted string literal, '\\' and double quotes must be '\\' escaped.
  In addition, if the RHS is a pattern (``~~`` and ``!~`` operators)
  literal '*' and '?' in the pattern must also be '\\' escaped.

  Example:

   ::

    $ aq_udb -exp Test
        -filt 't > 123456789'

  * Export only rows of Test with 't > 123456789'.

   ::

    $ aq_udb -exp Test
        -filt 'Eval($Random % 100) == 0'

  * Randomly select roughly 1/100th of the rows for export.


.. _`-mod`:

``-mod ModSpec``
  Specify a module to load on the server side during an export/count/scan
  operation.
  ``ModSpec`` has the form ``ModName[:argument]`` where ``ModName``
  is the logical module name and ``argument`` is a module specific
  parameter string. Udb server will try to load "mod/``ModName``.so"
  in the server directory.
  Module functions are called in each user bucket according to the
  `Data Processing Steps`_.

  Only one such module can be specified.


.. _`-pp`:

``-pp TabName [-pp_var ... -pp_evlc ... -pp_filt ... -pp_goto ... -pp_end_of_scan ...]``
  ``-pp`` groups one or more `-pp_var`_, `-pp_evlc`_ and/or `-pp_filt`_
  actions together.
  Each group performs pre-processing at the user bucket level before
  data in the bucket is exported/counted/scanned. Pre-processing applies to the
  user bucket itself or table data in the bucket.

  ``TabName`` is the table whose data is to be processed by the
  `-pp_evlc`_ and `-pp_filt`_ actions in the group.
  To target the user bucket itself, set ``TabName`` to "bucket".
  The only column in this pseudo table is "name" (the "PKEY").

  The list of `-pp_evlc`_, `-pp_filt`_ and `-pp_goto`_ rules are generally
  executed in order. See `Data Processing Steps`_ for details.
  Rule executions can also be made conditional by adding "if-else" controls.
  See `Rule Execution Controls`_ for details.


.. _`-pp_var`:

``-pp_var ColName Val``
  Part of a `-pp`_ group.
  Same as `-var`_, but the assignment is done at the beginning of a `-pp`_
  group in each user bucket.

  Example:

   ::

    $ aq_udb ... -pp -pp_var Var1 0 ...

  * Initialize Var1 in Var vector to 0 before *each* bucket is processed.


.. _`-pp_evlc`:

``-pp_evlc ColName Expr``
  Part of a `-pp`_ group.
  For each row in the ``-pp`` table,
  evaluate expression ``Expr`` and place the result in a column identified
  by ``ColName``. The column can be part of the ``-pp`` table or the Var vector.

  ``Expr`` is the expression to evaluate.
  Data type of the evaluated result must be compatible with the data type of
  the target column. For example, string result for a string column and
  numeric result for a numeric column.
  Operands in the expression can be columns in the ``-pp`` table, columns in
  the Var vector, constants, builtin variables and functions.

  * Use '(' and ')' to group operations as appropriate.
  * For a numeric type evaluation, supported operators are
    '*', '/', '%', '+', '-', '&', '|' and '^'.
  * Depending on the operand type, evaluation may use 64-bit floating point
    arithmetic or 64-bit signed integral arithmetic. For example, "1 + 1" is
    evaluated using integral arithmetic while "1 + 1.0" is evaluated using
    floating point arithmetic. Similarly, "Col1 + 1" may use either arithmetic
    depending on Col1's type while "Col1 + 1.0" always uses floating point.
  * For a string type evaluation, the only supported operator is
    '+' for concatenation.
  * Certain types can be converted to one another using the builtin functions
    ``ToIP()``, ``ToF()``, ``ToI()`` and ``ToS()``.
  * Operator precedency is *NOT* supported. Use '(' and ')' to group
    operations as appropriate.

  Builtin variables:

  ``$Random``
    A random number (postive integer).
    Its value changes every time the variable is referenced.
    The seed of this random sequence
    can be set using the `-seed`_ option.

  ``$RowNum``
    Represent the per bucket per table row index.
    Index of the first row is 1.
    It is generally used during a table scan to identify the current row number.

  Builtin functions:

  ``ToIP(Val)``
    Returns the IP address value of ``Val``.
    ``Val`` can be a string/IP column's name, a literal string,
    or an expression that evaluates to a string/IP.

  ``ToF(Val)``
    Returns the floating point value of ``Val``.
    ``Val`` can be a string/numeric column's name, a literal string/number,
    or an expression that evaluates to a string/number.

  ``ToI(Val)``
    Returns the integral value of ``Val``.
    ``Val`` can be a string/numeric column's name, a literal string/number,
    or an expression that evaluates to a string/number.

  ``ToS(Val)``
    Returns the string representation of ``Val``.
    ``Val`` can be a numeric column's name, a literal string/number/IP,
    or an expression that evaluates to a string/number/IP.

  ``Min(Val1, Val2)``
    Returns the lesser of ``Val1`` and ``Val2``.
    ``Val1`` and ``Val2`` can be a numeric column's name, a literal number,
    or an expression that evaluates to a number.

  ``Max(Val1, Val2)``
    Returns the greater of ``Val1`` and ``Val2``.
    ``Val1`` and ``Val2`` can be a numeric column's name, a literal number,
    or an expression that evaluates to a number.

  ``SHash(Val)``
    Returns the numeric hash value of a string.
    ``Val`` can be a string column's name, a literal string,
    or an expression that evaluates to a string.

  ``SLeng(Val)``
    Returns the length of a string.
    ``Val`` can be a string column's name, a literal string,
    or an expression that evaluates to a string.

  Example:

   ::

    $ aq_udb -exp Test
        -pp Test
          -pp_var Var1 0
          -pp_evlc Var1 'Var1 + 1'
          -pp_evlc c3 'Var1'

  * Assign a per bucket sequence number to column c3 of table Test before
    exporting it. Var1 must be a (numeric) column defined in the Var vector in
    the Udb spec file. Note that it is set to 0 at the beginning of each user
    bucket before Test is scanned.


.. _`-pp_filt`:

``-pp_filt FilterSpec``
  Part of a `-pp`_ group.
  Like `-filt`_, but the filter is applied to ``-pp`` table.

  Example:

   ::

    $ aq_udb -exp Test
        -pp bucket
          -pp_filt 'Eval(SHash(name) % 100) == 0'

  * This is a way to select a subset of users. Assuming that the user name hash
    is uniformly distributed, this example selects 1/100th of the user pool.


.. _`-pp_goto`:

``-pp_goto DestSpec``
  Part of a `-pp`_ group.
  Go to ``DestSpec``. This is uaually done conditionally within a
  ``-if/-elif/-endif`` block (see `Rule Execution Controls`_ for details).

  ``DestSpec`` is the destination to go to. It is one of:

  * ``next_bucket`` - Skip the current user bucket entirely.cw
    The export/count/scan processing on this bucket will also be skipped.
  * ``next_row`` - Skip the current data row and start over on the next row.
  * ``proc_bucket`` - Terminate all ``-pp`` processings (i.e.,
    stop the current ``-pp`` group and skip all pending ``-pp`` groups)
    and start the export/count/scan operation in the current user bucket.
  * ``next_pp`` - Stop the current ``-pp`` group and start the next one.
  * ``+Num`` - Jump over Num `-pp_evlc`_, `-pp_filt`_ and `-pp_goto`_ rules.
    ``Num=0`` means the next rule, ``Num=1`` means skip over one rule, and so.


.. _`-pp_end_of_scan`:

``-pp_end_of_scan DestSpec``
  Part of a `-pp`_ group.
  This is a special rule that defines the
  action to take after all the rows in the ``-pp`` table has been exhausted.
  The default action is to start the next ``-pp`` group.
  Use ``DestSpec`` to control the exact behavior:

  * ``next_bucket`` - Skip the current user bucket entirely.
    The export/count/scan processing on this bucket will also be skipped.
  * ``proc_bucket`` - Skip all pending ``-pp`` groups
    and start the export/count/scan operation in the current user bucket.
  * ``next_pp`` - Start the next ``-pp`` group. This is the default behavior
    at the end of a ``-pp`` table scan.
  * ``+Num`` - Jump over Num ``-pp`` groups. ``Num=0`` is equivalent to
    ``next_pp``,
    ``Num=1`` means skip over the next ``-pp`` group as well, and so.

  This option is not position dependent - it can be specified anywhere
  within a ``-pp`` group.

  Example:

   ::

    $ aq_udb -exp Test1
        -pp 'Test2'
          -pp_goto proc_bucket
          -pp_end_of_scan next_bucket

  * Only export Test1 from buckets whose Test2 table is not empty. If Test2 is
    not empty, the ``-goto`` rule will be executed on the first row, causing
    execution to jump to export processing; in this way, the end-of-scan
    condition is not triggered. However, if Test2 is empty, ``-goto``
    is not executed and end-of-scan is triggered.


.. _`-o`:

``-o[,AtrLst] File``
  Export output option.
  Set the output attributes and file.
  If ``File`` is a '-' (a single dash), data will be written to stdout.
  Optional ``AtrLst`` is described under `Output File Attributes`_.

  If this option is not used with an export, data is written to stdout.

  Example:

   ::

    $ aq_udb -exp Test ... -o,esc,noq -

  * Output to stdout in a format suitable for Amazon Cloud.


.. _`-c`:

``-c ColName [ColName ...]``
  Select columns to output during an export.
  Available selections are columns from the table/vector being exported and/or
  columns from the Var vector.
  Default output includes all columns in the table/vector being exported.

  Example:

   ::

    $ aq_udb -exp Test ... -c Test_Col1 ... Test_ColN Var_Col1 ... Var_ColN

  * Output Var vector columns along with columns from Test.
    Even though Test_Col* are normally exported by default, they must be
    listed explicitly in order to include any Var_Col*.


.. _`-notitle`:

``-notitle``
  Export output option.
  Suppress the column name label row from the output.
  A label row is normally included by default.


.. _`-sort`:

``-sort [ColName ...] [-dec] [-top Num]``
  `-exp`_ and `-exp_usr`_ output post processing option.

  For `-exp`_, use ``ColName`` to set the desired sort columns.
  If no ``ColName`` is given, the "PKEY" column is assumed.
  The sort columns must be in the output columns.

  For `-exp_usr`_, no ``ColName`` is needed. Sort is always done by the "PKEY".

  Records are normally sorted in ascending order (i.e., smallest value first).
  Use ``-dec`` to sort in descending order.
  ``-top`` limits the output to the top Num records in the result.

  **Note**: Sort should not be used if the output contains Var vector columns.


.. _`-ord`:

``-ord [DbName:]TabName [ColName ...] [-dec]``
  Sort records in table ``TabName`` within each bucket.
  Optional ``DbName`` sets the Udb spec file as in the `-db`_ option.
  Use ``ColName`` to set the desired sort columns.
  If no ``ColName`` is given, the "TKEY" column is assumed.
  Note that the "PKEY" column cannot be used here.
  Records are normally sorted in ascending order (i.e., smallest value first).
  Use ``-dec`` to sort in descending order.


.. _`-ord_all`:

``-ord_all [-dec]``
  Sort records within each bucket.
  All tables with a "TKEY" will be sorted.
  Records are normally sorted in ascending order (i.e., smallest value first).
  Use ``-dec`` to sort in descending order.


.. _`-clr`:

``-clr [DbName:]TabName``
  Remove/reset ``TabName`` records in the database.
  Optional ``DbName`` sets the Udb spec file as in the `-db`_ option.

  * For a table, the records are removed.
  * For a vector, the columns are reset to 0/blank.
  * For the Var vector (i.e., when ``TabName`` is "var"), the columns are reset
    to 0/blank.


.. _`-clr_all`:

``-clr_all``
  Remove/reset data from all tables/vectors in the database.
  All user buckets will be removed as well.

  * For a table, the records are removed.
  * For a vector, the columns are reset to 0/blank.
  * For the Var vector (i.e., when ``TabName`` is "var"), the columns are reset
    to 0/blank.


.. _`-probe`:

``-probe``
  Probe the servers and exit.

  * If all servers responded *successful*, the exit code will be 0.
  * If a connection failed or a server responded *failure*,
    the exit code will be non-zero.
    Usually, an error message will also be printed to stderr.
  * Use this with `-verb`_ to get more info.


Exit Status
===========

If successful, the program exits with status 0. Otherwise, the program exits
with a non-zero status code along error messages printed to stderr.
Applicable exit codes are:

* 0 - Successful.
* 1-9 - Program initial preparation error.
* 10-19 - Input file load error.
* 20-29 - Result output error.
* 30-39 - Udb server connection/communication error.


Output File Attributes
======================
Some output file can have these comma separated attributes:

* ``app`` - Append to file; otherwise, file is overwritten by default.
* ``bin`` - Input in binary format (default is CSV).
* ``esc`` - Use '\\' to escape ',', '"' and '\\' (CSV).
* ``noq`` - Do not quote string fields (CSV).
* ``fmt_g`` - Use "%g" as print format for ``F`` type columns. Only use this
  to aid data inspection (e.g., during integrity check or debugging).

By default, output is in CSV format. Use the ``esc`` and ``noq`` attributes to
set output characteristics as needed.


Rule Execution Controls
=======================

`-pp`_ also supports conditional actions using the
``-if[not]``, ``-elif[not]``, ``-else`` and ``-endif`` construction:

 ::

  -if[not] RuleToCheck
    RuleToRun
    ...
  -elif[not] RuleToCheck
    RuleToRun
    ...
  -else
    RuleToRun
    ...
  -endif

Sypported ``RuleToCheck`` are `-pp_evlc`_ and `-pp_filt`_.
Suppoeted ``RuleToRun`` are `-pp_evlc`_, `-pp_filt`_ and `-pp_goto`_.

Example:

 ::

  $ aq_udb -exp Test
      -pp Test
        -pp_var v_seq 0
        -if -pp_filt 'flag == "yes"'
          -pp_evlc v_seq 'v_seq + 1'
          -pp_evlc c3 'v_seq'
        -else
          -pp_evlc c3 '0'
        -endif

* Before exporting Test, assign a per bucket sequence number to column c3 if
  the "flag" column is "yes" or just 0 otherwise.
  Note that `-pp_var`_ can be specified anywhere within a `-pp`_ group.
  These rules are always executed at the beginning of the group.


Data Processing Steps
=====================

For each export/count/scan operation,
data is processed according to the commandline options in this way:

* Var columns are initialized according the `-var`_ options.

* Then the user buctets are scanned. For each user bucket in the database:

  * The `-pp`_ groups are executed in the order they are specified on the
    commandline. For each ``-pp`` group:

    * Var columns are initialized according the `-pp_var`_ rules.
    * Then the ``-pp`` table is scanned. For each row in the table:

      * The list of `-pp_evlc`_, `-pp_filt`_ and `-pp_goto`_ rules
        (including any "-if-elif-else-endif" controls) are executed in order.

    * When all the rows are exhausted, the `-pp_end_of_scan`_ rule is executed.

  * Then, if a module is specified (see `-mod`_), its user bucket processing
    function (if any) is called.
    This function can inspect and/or modify arbitrary data in the bucket.
    It can also tell the server to skip the current bucket so that it will
    not be exported/counted/scanned.

  * Then export/count/scan processing on the target table begins. For each
    data row in the target table:

    * The ``-filt`` rule is processed.
    * Then, if a module is specified (see `-mod`_), its row processing
      function (if any) is called.
      This function can inspect and/or modify the current data row.
      It can also tell the server to skip the current row so that it will
      not be exported/counted/scanned.
    * Finally, the data row is exported/counted.


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udb.spec <udb.spec.html>`_ - Udb spec file.
* `udbd <udbd.html>`_ - User (Bucket) Database server

