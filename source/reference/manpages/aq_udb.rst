.. |<br>| raw:: html

   <br>

======
aq_udb
======

Udb server interface


Synopsis
========

::

  aq_udb [-h] Global_Opt Mnt_Spec|Order_Spec|Export_Spec

  Global_Opt:
      [-verb] [-stat] [-test]
      [-server AdrSpec [AdrSpec ...]] [-local]

  Mnt_Spec:
      -crt[,AtrLst] DbName |
      -alt[,AtrLst] DbName |
      -clr[,AtrLst] DbName[:TabName] |
      -inf[,AtrLst] DbName [-o[,AtrLst] File] |
      -probe[,AtrLst] DbName

  Order_Spec:
      -ord[,AtrLst] DbName[:TabName] [ColName ...]

  Export_Spec:
      -exp[,AtrLst] DbName[:TabName] |
      -cnt[,AtrLst] DbName[:TabName] |
      -scn[,AtrLst] DbName[:TabName]
      [-seed RandSeed]
      [-var ColName Val]
      [-pp TabName
        [-bvar ColName Val]
        [-eval ColName Expr]
        [-filt FilterSpec]
        [-goto DestSpec]
        [-del_row | -del_key]
      -endpp]
      [-bvar ColName Val]
      [-eval ColName Expr]
      [-filt FilterSpec]
      [-goto DestSpec]
      [-del_row | -del_key]
      [-mod ModSpec [ModSrc]]
      [-sort[,AtrLst] ColName ...]
      [-lim_key Num] [-lim_rec Num] [-key_rec Num] [-top Num]
      [-o[,AtrLst] File] [-c ColName [ColName ...]]


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

Also take a look at some examples of using this command at :doc:`../../usecases/syntaxexamples/aq_udb-option-examples`.


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

    aq_udb: rec=Count


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


.. _`-crt`:

``-crt[,AtrLst] DbName``
  Create a database explicitly. Normally, a database is created automatically
  during an import (see `aq_pp <aq_pp.html>`_).
  However, it is a good idea to perform this create operation anyway in case
  the import is not performed.
  ``DbName`` is the database name (see `Target Database`_).
  Note that it is not an error to create a database that already exists as
  long as the database definition is identical.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).


.. _`-alt`:

``-alt[,AtrLst] DbName``
  Alter the spec of database ``DbName`` (see `Target Database`_).
  The database must already exist (e.g., created via `-crt`_).
  Currently, *only* the Var vector spec can be altered,
  all other tables and vectors must be the same as before.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).

  The values of columns that exist in both the old and new specs are preserved.
  New columns are initialized with 0/blank.


.. _`-clr`:

``-clr[,AtrLst] DbName[:TabName]``
  Clear an entire DB or remove/reset the data of a table/vector.
  ``DbName`` is the database name (see `Target Database`_).
  ``TabName`` is a table/vector name in the database.
  Specific clear actions are:

  * For a table, its records are removed.
  * For a vector, its columns are reset to 0/blank.
  * For the Var vector (i.e., when ``TabName`` is "var"), its columns are reset
    to 0/blank.
  * If ``TabName`` is not given or if it is a "." (a dot), *everything* will be
    cleared - all keys, tables, vectors, the Var vector and the database
    definition will all be removed.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).


.. _`-inf`:

``-inf[,AtrLst] DbName``
  Get the primary key counts and table/vector row counts of database ``DbName``
  (see `Target Database`_). It differs from `-cnt`_ in these ways:

  * All table/vectors row counts are output. The output has this form:

     ::

      "pkey","var","TabName1","TabName2",...,"VecName1","VecName2",...
      num,num,num,num,...,num,num,...

  * Processing rules (e.g., filters) are not supported.
  * Much faster - the counts are cached in memory, no database scan needed.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).
  * ``asis`` - Normally, the results from all the servers are combined to
    produce a single row of counts. With this attribute, the *individual*
    servers' counts are output, producing one row of counts per server.


.. _`-probe`:

``-probe[,AtrLst] DbName``
  Check if the servers associated with database ``DbName``
  (see `Target Database`_) are heathly and that
  the database has been defined on the servers.

  * If all servers responded *successful*, the exit code will be 0.
  * If a connection failed or ``DbName`` is not defined,
    the exit code will be non-zero.
    Usually, an error message will be printed on stderr.
  * Use this with `-verb`_ and/or `-stat`_ to get more info if desired.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).


.. _`-ord`:

``-ord[,AtrLst] DbName[:TabName] [ColName ...]``
  Sort the keys in a DB or sort the records in a table for each key.
  This will alter the data order in the DB.
  This operation is done internally, no output will be generated.
  The default sort order is ascending.
  ``DbName`` is the database name (see `Target Database`_).
  ``TabName`` is the target table to sort.
  ``ColNames`` are the desired sort columns.
  If ``TabName`` or ``ColName`` is not given:

  * ``TabName`` given, ``ColName`` not given -
    ``TabName`` will be sorted by its "TKEY" column
    (see `udb.spec <udb.spec.html>`_).
  * ``TabName`` not given or is a "." (a dot), ``ColName`` not given -
    Every table in ``DbName`` with a "TKEY" will be sorted by its "TKEY".
  * ``TabName`` not given or is a "." (a dot), ``ColName`` given -
    Each ``ColName`` must be a primary key column. This will sort the data
    by their keys on a *per server* basis. If the database is distributed over
    a server pool, the keys are not sorted across servers.`

  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).
  * ``ncas`` - Do case insensitive match (default is case sensitive).
    For ASCII data only.
  * ``dec`` - Sort in descending order (default is ascending).


.. _`-exp`:

``-exp[,AtrLst] DbName[:TabName]``
  Export data.
  ``DbName`` is the database name (see `Target Database`_).
  ``TabName`` is a table/vector name in the database.
  If ``TabName`` is not given or if it is a "." (a dot), the primary keys
  will be exported.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).
  * ``asis`` - This attributes only affects the result of a Var vector
    export. Normally, the results from all the servers are combined to
    produce a single row of Var values. With this attribute, the *individual*
    servers' values are output, producing one row of values per server.
  * ``seg=N1[-N2]/N[:V]`` - Only export a subset of the data by selecting
    segment N1 or segments N1 to N2 (inclusive) out of N segments of
    unique keys based on their hash values.
    For example, ``seg=2-4/10`` will divide the keys into 10 segments and
    export segments 2, 3 and 4; segments 1 and 5-10 are skipped.
    Optional ``V`` is a number that can be used to vary the sample selection.
    It is zero by default.


.. _`-cnt`:

``-cnt[,AtrLst] DbName[:TabName]``
  Count the unique primary keys in database ``DbName`` (see `Target Database`_).
  If ``TabName`` is given, count the rows in the table/vector as well.
  Normally, use this option when the counts are processing rules dependent
  (e.g., filters); otherwise, use `-inf`_ since it is much faster.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).
  * ``asis`` - Normally, the results from all the servers are combined to
    produce a single set of counts. With this attribute, the *individual*
    servers' counts are output, producing one set of counts per server.
  * ``seg=N1[-N2]/N[:V]`` - Only count a subset of the data by selecting
    segment N1 or segments N1 to N2 (inclusive) out of N segments of
    unique keys based on their hash values.
    For example, ``seg=2-4/10`` will divide the keys into 10 segments and
    count segments 2, 3 and 4; segments 1 and 5-10 are skipped.
    Optional ``V`` is a number that can be used to vary the sample selection.
    It is zero by default.


.. _`-scn`:

``-scn[,AtrLst] DbName[:TabName]``
  Scan data only. No output will be produced.
  This option is typically used along with certain data processing rules
  (see `Data Processing Steps`_) and/or a data processing module (see `-mod`_).
  ``DbName`` is the database name (see `Target Database`_).
  ``TabName`` is a table/vector name in the database.
  If ``TabName`` is not given or if it is a "." (a dot), the primary keys
  will be scanned - this is typically used with `-pp`_ rules.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).


.. _`-seed`:

``-seed RandSeed``
  Set the random sequence seed used by the ``$Random``
  `-eval`_ builtin variable.


.. _`-var`:

``-var ColName Val``
  Set the value of the Var vector column ``ColName`` to ``Val``.
  A Var vector must be defined in the Udb spec file and ``ColName``
  must be a column in that table.
  See `udb.spec <udb.spec.html>`_ for details.
  Note that a string ``Val`` must be quoted,
  see `String Constant`_ spec for details.

  * Var columns can also be altered by `-eval`_ and modules (see `-mod`_).
  * Var column values are persistent until they are cleared by a `-clr`_
    operation, at which point the columns are reset to 0/blank.

  Example:

   ::

    $ aq_udb ... -var Var1 0 ...

  * Initialize Var1 in Var vector to 0 before any buctet is processed.


.. _`-bvar`:

``-bvar ColName Val``
  Same as `-var`_ except that the column is set to ``Val`` repeatedly
  as *each* key is processed before other processing rules are executed.
  Note that a string ``Val`` must be quoted,
  see `String Constant`_ spec for details.

  This rule can also be used within a `-pp`_ group. In this case,
  ``ColName`` is set to ``Val`` as each key is processed before other
  pre-processing rules are executed.

  See `Data Processing Steps`_ for details on these usages.

  Example:

   ::

    $ aq_udb ... -pp -bvar Var1 0 ...

  * Initialize Var1 in Var vector to 0 as *each* key is processed.


.. _`-eval`:

``-eval ColName Expr``
  For each row in the table/vector being exported/counted/scanned,
  evaluate expression ``Expr`` and place the result in a column identified
  by ``ColName``. The column can be part of the target table or the Var vector.

  This rule can also be used within a `-pp`_ group. In this case,
  the target table becomes the ``-pp`` table.
  Note that ``-eval`` rules inside `-pp`_ groups are evaluated before those
  for the target table/vector. See `Data Processing Steps`_ for details.

  ``Expr`` is the expression to evaluate.
  Data type of the evaluated result must be compatible with the data type of
  the target column. For example, string result for a string column and
  numeric result for a numeric column (there is no automatic type conversion;
  however, explicit conversion can be done using the ``To*()`` functions
  described below).
  Operands in the expression can be columns from the target table/vector,
  columns from other vectors, columns from the Var vector,
  constants, builtin variables and functions.

  * Column names are case insensitive. Do not quote the name.
    To address columns other than those in the target table/vector, use the
    ``VecName.ColName`` format. For the Var vector, ``VecName`` is optional
    unless ``ColName`` also exists in the target.
  * String constants must be quoted,
    see `String Constant`_ spec for details.
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
  * Operator precedence is *NOT* supported. Use '(' and ')' to group
    operations as appropriate.

  Builtin variables:

  ``$Random``
    A random number (postive integer).
    Its value changes every time the variable is referenced.
    The seed of this random sequence
    can be set using the `-seed`_ option.

  ``$RowNum``
    Represent the per key per table row index (one-based).
    It is generally used during a table scan to identify the current row number.

  ``$CurSec``
    The current time in seconds.
    It is evaluated in realtime when the variable is referenced.

  ``$CurUSec``
    The current time in microseconds.
    It is evaluated in realtime when the variable is referenced.

  Standard functions:

    See `aq-emod <aq-emod.html>`_ for a list of supported functions.

  Example:

   ::

    $ aq_udb -exp mydb:Test
        -eval c_delta 'c1 - c2'

  * Calculate c_delta before exporting.


.. _`-filt`:

``-filt FilterSpec``
  For each row in the table/vector being exported/counted/scanned,
  evaluate ``FilterSpec`` and use the result to determine whether to
  keep the data row.
  The result can also be used in a ``-if/-elif/-endif`` for
  `Rule Execution Controls`_.

  This rule can also be used within a `-pp`_ group. In this case,
  the target table becomes the ``-pp`` table.
  Note that ``-filt`` rules inside `-pp`_ groups are evaluated before those
  for the target table/vector. See `Data Processing Steps`_ for details.

  ``FilterSpec`` is the filter to evaluate.
  It has the basic form ``[!] LHS [<compare> RHS]`` where:

  * The negation operator ``!`` negates the result of the comparison.
    It is recommended that ``!(...)`` be used to clarify the intended
    operation even though it is not required.
  * LHS and RHS can be:

    * A column name (case insensitive). Do not quote the name.
      The column can be part of the target table/vector,
      other vectors, and/or the Var vector.
      To address columns other than those in the target table/vector, use the
      ``VecName.ColName`` format. For the Var vector, ``VecName`` is optional
      unless ``ColName`` also exists in the target.
    * A constant, which can be a string, a number or an IP address.
      A string constant must be quoted,
      see `String Constant`_ spec for details.
    * An expression to evaluate as defined under `-eval`_.

  * If only the LHS is given, its values will be used as a boolean -
    a non blank string or non zero number/IP equals True, False otherwise.
  * Supported comparison operators are:

    * ``==``, ``>``, ``<``, ``>=``, ``<=`` -
      LHS and RHS comparison.
    * ``~==``, ``~>``, ``~<``, ``~>=``, ``~<=`` -
      LHS and RHS case insensitive comparison; string type only.
    * ``!=``, ``!~=`` -
      Negation of the above equal operators.
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

  Example:

   ::

    $ aq_udb -exp mydb:Test
        -filt 't > 123456789'

  * Export only rows of Test with 't > 123456789'.

   ::

    $ aq_udb -exp mydb:Test
        -filt 'Eval($Random % 100) == 0'

  * Randomly select roughly 1/100th of the rows for export.


.. _`-goto`:

``-goto DestSpec``
  Go to ``DestSpec``. This is uaually done conditionally within a
  ``-if/-elif/-endif`` block (see `Rule Execution Controls`_ for details).

  ``DestSpec`` is the destination to go to. It is one of:

  * ``next_key`` - Stop processing the current key and
    start over on the next key.
  * ``next_row`` - Stop processing the current row and
    start over on the next row.

  This rule can also be used within a `-pp`_ group. In this case,
  these additional destinations are supported:

  * ``proc_key`` - Terminate all ``-pp`` processings (i.e.,
    stop the current ``-pp`` group and skip all pending ``-pp`` groups)
    and start the export/count/scan operation for the current key.
  * ``next_pp`` - Stop the current ``-pp`` group and start the next one.


.. _`-del_row`:

``-del_row[,AtrLst]``
  Delete the current row in the database. No more processing on the current
  row will be done.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``post=DestSpec`` - Set the action to take after the delete.
    ``DestSpec`` is one of:

    * ``next_key`` - Stop processing the current key and
      start over on the next key.
    * ``proc_key`` - Skip all pending ``-pp`` groups
      and start the export/count/scan operation for the current key.
    * ``next_row`` - Start processing the next row. This is the default
      behavior.


.. _`-del_key`:

``-del_key[,AtrLst]``
  Delete the current key and its associated data from the database.
  No more processing on the current key will be done.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``post=DestSpec`` - Set the action to take after the delete.
    ``DestSpec`` is one of:

    * ``next_key`` - Start processing the next key. This is the default
      behavior.


.. _`-pp`:

``-pp[,AtrLst] TabName [-bvar ... -eval ... -filt ... -goto ... -del_row ...] -endpp``
  ``-pp`` groups one or more `-bvar`_, `-eval`_, `-filt`_, `-goto`_,
  `-del_row`_ and `-del_key`_ actions together.
  Each group performs pre-processing on a set of key specific data (e.g., a
  table). It is done *before* the main export/count/scan operation.
  See `Data Processing Steps`_ for details.

  ``TabName`` sets the target table/vector for the rules in the ``-pp`` group.
  It may refer to a table/vector or the primary key set.
  To target a table/vector, specify its name.
  To target the primary key set, specify  a "." (a dot).
  "." is a pseudo vector containing the primary key columns.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``post=DestSpec`` - Set the action to take after all the rows in
    the target table has been exhausted.
    ``DestSpec`` is one of:

    * ``next_key`` - Stop processing the current key and
      start over on the next key.
    * ``proc_key`` - Skip all pending ``-pp`` groups
      and start the export/count/scan operation for the current key.
    * ``next_pp`` - Start the next ``-pp`` group. This is the default behavior.

  The `-bvar`_ rules in the group are always executed first.
  Then the list of `-eval`_, `-filt`_, `-goto`_, `-del_row`_ and `-del_key`_
  rules are executed in order.
  Rule executions can also be made conditional by adding "if-else" controls,
  see `Rule Execution Controls`_ for details.

  ``-endpp`` marks the end of a ``-pp`` group.

  Example:

   ::

    $ aq_udb -exp mydb:Test1
        -pp,post=next_key 'Test2'
          -goto proc_key

  * Only export Test1 from keys whose Test2 table is not empty. If Test2 is
    not empty, the ``-goto`` rule will be executed on the first row, causing
    execution to jump to export processing; in this way, the ``post``
    action is not triggered. However, if Test2 is empty, ``-goto``
    is not executed and ``post`` is triggered.

   ::

    $ aq_udb -exp Test
        -pp .
          -filt 'Eval($Random % 100) == 0'
        -endpp
        -filt 't > 123456789'

  * Randomly select roughly 1/100th of the keys for export.
    From this subset, export only rows of Test with 't > 123456789'.
    Note that ``-endpp`` is mandatory here to prevent misinterpretation of the
    2nd ``-filt``.


.. _`-mod`:

``-mod ModSpec [ModSrc]``
  Specify a module to be loaded on the *server side* during an
  export/count/scan operation. A module contains one or more processing
  functions which are called as each key is processed according to the
  `Data Processing Steps`_.
  Only one such module can be specified.

  ``ModSpec`` has the form ``ModName`` or ``ModName(Arg1, Arg2, ...)``
  where ``ModName`` is the module name and ``Arg*`` are module dependent
  arguments. Note that the arguments must be literals -
  `string constants <#string-constant>`_ (quoted), numbers or IP addresses.
  ``ModSrc`` is an optional module source file containing:

  * A module script source file that can be used to build the specified
    module. See the `Udb module script compiler <mcc.umod.html>`_
    documentation for more information.
  * A ready-to-use module object file. It *must* have a ``.so`` extension.

  Without ``ModSrc``, the server will look for a preinstalled module matching
  ``ModName``.


.. _`-sort`:

``-sort[,AtrLst] ColName ...``
  Sort the export result according to the given columns.
  Note that only the result is sorted, data order in the DB is not altered.
  Use this with `-top`_ to get the top ranking results if desired.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``ncas`` - Do case insensitive pattern match (default is case sensitive).
    For ASCII data only.
  * ``dec`` - Sort in descending order (default is ascending).


.. _`-lim_key`:

``-lim_key Num``
  Limit the export *result* to approximately ``Num`` unique keys.
  This option is intended for data sampling only. The actual result count can
  be *less* than expected if the data is distributed over multiple servers.


.. _`-lim_rec`:

``-lim_rec Num``
  Limit the export *result* to approximately ``Num`` records.
  This option is intended for data sampling only. The actual result count can
  be *less* than expected if the data is distributed over multiple servers.
  Use the `-top`_ option if a precise limit is needed.


.. _`-key_rec`:

``-key_rec Num``
  Limit the export *result* to ``Num`` records per unique key.


.. _`-top`:

``-top Num``
  Limit the export *result* to ``Num`` records.


.. _`-o`:

``-o[,AtrLst] File``
  Set the output attributes and file for a `-inf`_, `-exp`_ or `-cnt`_
  operation.
  See the `aq_tool output specifications <aq-output.html>`_ manual for details.
  If this option is not used with those operations, the result will be
  written to stdout.

  Example:

   ::

    $ aq_udb -exp mydb:Test ... -o - -c Col2 Col1

  * Output Col2 and Col1 of Test (in that order) to stdout.


.. _`-c`:

``-c ColName [ColName ...]``
  Select the columns to output during a `-exp`_ operation.

  * For a table/vector export, columns from the target table/vector,
    columns from other vectors and columns from the Var vector can
    be selected.
    Default output includes all target table/vector columns.

  * For a primary key export, columns from the primary key,
    columns from any vectors and columns from the Var vector can
    be selected.
    Default output includes the primary key columns only.

  * For a Var vector export, only columns from the Var vector can
    be selected.
    Default output includes all Var vector columns.

  To address columns other than those in the target table/vector, use the
  ``VecName.ColName`` format. For the Var vector, ``VecName`` (``Var``)
  is optional unless a column of the same name also exists in the target.

  Shorthands can be used to represent groups of columns from a table/vector:

  * Specify ``*`` or ``+`` for all the columns in the target table/vector.
    ``*`` *includes* the primary key columns (if any), while ``+``
    *excludes* them.
  * Specify ``TabName.*`` or ``VecName.*`` or ``TabName.+`` or ``VecName.+``
    for all the columns in any applicable table/vector.
    ``*`` *includes* the primary key columns (if any), while ``+``
    *excludes* them.

  In addition, these special forms can also supported:

  * ``ColName[:NewName][+NumPrintFormat]`` - Add ``ColName`` to the output.
    If ``:NewName`` is given, it will be used as the output label.
    The ``+NumPrintFormat`` spec is for numeric columns. It overrides the
    print format of the column (*be careful with this format - a wrong spec
    can crash the program*).
  * ``^ColName[:NewName][+NumPrintFormat]`` - Same as the above, but with a
    leading ``^`` mark. It is used to *modify* the output label and/or format
    of a previously selected output column called ``ColName``.
    If ``^ColName[...]`` is the first selection after ``-c``, then ``*`` will be
    included automatically first.
  * ``~ColName`` - The leading ``~`` mark is used to *exclude* a previously
    selected output column called ``ColName``. 
    If ``~ColName`` is the first selection after ``-c``, then ``*`` will be
    included automatically first.

  Example:

   ::

    $ aq_udb -exp mydb:Test ... -c Test_Col1 ... Test_ColN Var_Col1 ... Var_ColN
    $ aq_udb -exp mydb:Test ... -c 'Test.*' 'Var.*'
    $ aq_udb -exp mydb:Test ... -c '*' 'Var.*'

  * All examples output Var vector columns along with the columns from Test.
    Even though Test_Col* are normally exported by default, they must be
    listed explicitly in order to include any Var_Col*.


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
* 31 - Udb connect error.
* 32 - Udb communication error.
* 33 - Udb authentication error.
* 34 - Udb request invalid.


String Constant
===============

A string constant must be quoted between double or single quotes.
With *double quotes*, special character sequences can be used to represent
special characters.
With *single quotes*, no special sequence is recognized; in other words,
a single quote cannot occur between single quotes.

Character sequences recognized between *double quotes* are:

* ``\\`` - represents a literal backslash character.
* ``\"`` - represents a literal double quote character.
* ``\b`` - represents a literal backspace character.
* ``\f`` - represents a literal form feed character.
* ``\n`` - represents a literal new line character.
* ``\r`` - represents a literal carriage return character.
* ``\t`` - represents a literal horizontal tab character.
* ``\v`` - represents a literal vertical tab character.
* ``\0`` - represents a NULL character.
* ``\xHH`` - represents a character whose HEX value is ``HH``.
* ``\<newline>`` - represents a line continuation sequence; both the backslash
  and the newline will be removed.

Sequences that are not recognized will be kept as-is.

Two or more quoted strings can be used back to back to form a single string.
For example,

 ::

  'a "b" c'" d 'e' f" => a "b" c d 'e' f


Target Database
===============

``aq_udb`` obtains information about the target database from a spec file.
The spec file contains server IPs (or domain names) and table/vector
definitions. See `udb.spec <udb.spec.html>`_ for details.
``aq_udb`` finds the relevant spec file in several ways:

* The spec file path is taken from the ``spec=UdbSpec`` attribute
  of the main operation option (`-crt`_, `-exp`_, etc.).
* The spec file path is deduced implicitly from the ``DbName`` parameters
  of the main operation option (`-crt`_, `-exp`_, etc.).
  This method sets the spec file to "``.conf/DbName.spec``" in the runtime
  directory of ``aq_udb``.
* If none of the above information is given, the spec file is assumed to be
  "``udb.spec``" in the runtime directory of ``aq_udb``.


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

Sypported ``RuleToCheck`` are `-eval`_ and `-filt`_.
Suppoeted ``RuleToRun`` are `-eval`_, `-filt`_, `-goto`_, `-del_row`_ and
`-del_key`_.

Example:

 ::

  $ aq_udb -exp mydb:Test
      -pp Test
        -bvar v_seq 0
        -if -filt 'flag == "yes"'
          -eval v_seq 'v_seq + 1'
          -eval c3 'v_seq'
        -else
          -eval c3 '0'
        -endif

* Before exporting Test, assign a per key sequence number to column c3 if
  the "flag" column is "yes" or just 0 otherwise.
  Note that `-bvar`_ rules are always executed before the others
  regardless of their placement within a `-pp`_ group.


Data Processing Steps
=====================

For each export/count/scan operation,
data is processed according to the command line options in this way:

* Initialize Var columns according the `-var`_ options.

* Scan the primary keys. For each key in the database:

  * Execute `-pp`_ groups in the order they are specified on the
    command line. For each ``-pp`` group:

    * Initialize Var columns according the `-bvar`_ rules.
    * Scan the ``-pp`` table. For each row in the table:

      * Execute the list of `-eval`_, `-filt`_, `-goto`_, `-del_row`_ and
        `-del_key`_ rules (including any "-if-elif-else-endif" controls)
        in order.

    * When all the rows are exhausted, follow the ``post`` attribute
      setting or start the next group by default.

  * Initialize Var columns according the `-bvar`_ rules.

  * If a module is specified (see `-mod`_) and it has a key-level processing
    function, the fuction is called.
    This function can inspect and/or modify any data associated with the key.
    It can also tell the server to skip the current key so that it will
    not be exported/counted/scanned.

  * Process the target export/count/scan table.
    For each data row in the target table:

    * Execute the list of `-eval`_, `-filt`_, `-goto`_, `-del_row`_ and
      `-del_key`_ rules (including any "-if-elif-else-endif" controls)
      in order.
    * If a module is specified (see `-mod`_) and it has a row processing
      function, the function is called.
      This function can inspect and/or modify the current data row.
      It can also tell the server to skip the current row so that it will
      not be exported/counted/scanned.
    * Export/count, the current data row.


See Also
========

* `aq-output <aq-output.html>`_ - aq_tool output specifications
* `aq-emod <aq-emod.html>`_ - aq_tool eval functions.
* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udb.spec <udb.spec.html>`_ - Udb spec file.
* `udbd <udbd.html>`_ - Udb server
* `mcc.umod <mcc.umod.html>`_ - Udb module script compiler

