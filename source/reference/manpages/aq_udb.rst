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
      [-server AdrSpec [AdrSpec ...]]
      [-local]

  Mnt_Spec:
      -crt[,AtrLst] DbName |
      -clr[,AtrLst] DbName:TabName |
      -probe[,AtrLst] DbName

  Order_Spec:
      -ord[,AtrLst] DbName:TabName [ColName ...]

  Export_Spec:
      -exp[,AtrLst] DbName:TabName |
      -cnt[,AtrLst] DbName:TabName |
      -scn[,AtrLst] DbName:TabName
      [-seed RandSeed]
      [-var ColName Val]
      [-pp TabName
        [-bvar ColName Val]
        [-eval ColName Expr]
        [-filt FilterSpec]
        [-goto DestSpec]
        [-del_row | -del_usr]
      -endpp]
      [-bvar ColName Val]
      [-eval ColName Expr]
      [-filt FilterSpec]
      [-goto DestSpec]
      [-del_row | -del_usr]
      [-mod ModSpec [ModSrc]]
      [-lim_usr Num] [-lim_rec Num]
      [-sort[,AtrLst] [ColName ...] [-top Num]]
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
  ``DbName`` is the database name (see `Target Database`_).
  Note that it is not an error to create a database that already exists as
  long as the database definition is identical.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).


.. _`-clr`:

``-clr[,AtrLst] DbName:TabName``
  Remove/reset the data of a table/vector.
  ``DbName`` is the database name (see `Target Database`_).
  ``TabName`` is a table/vector name in the database.
  Specific clear actions are:

  * For a table, its records are removed.
  * For a vector, its columns are reset to 0/blank.
  * For the Var vector (i.e., when ``TabName`` is "var"), its columns are reset
    to 0/blank.
  * If ``TabName`` is a "." (a dot), *everything* will be cleared -
    tables, vectors, the "var" vector, user buckets and the database
    definition are all be removed,

  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).


.. _`-probe`:

``-probe[,AtrLst] DbName``
  Check if the servers associated with ``DbName`` are heathly and that
  ``DbName`` has been defined on the servers.

  * If all servers responded *successful*, the exit code will be 0.
  * If a connection failed or ``DbName`` is not defined,
    the exit code will be non-zero.
    Usually, an error message will be printed on stderr.
  * Use this with `-verb`_ and/or `-stat`_ to get more info if desired.

  ``DbName`` is the database name (see `Target Database`_).
  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).


.. _`-ord`:

``-ord[,AtrLst] DbName:TabName [ColName ...]``
  Sort records in a table within each bucket. The default sort order is
  ascending. The records are sorted internally; not output will be generated.
  ``DbName`` is the database name (see `Target Database`_).
  ``TabName`` is a table name in the database.
  ``ColName`` sets the desired sort columns.
  If no ``ColName`` is given, the "TKEY" column is assumed
  (see `udb.spec <udb.spec.html>`_).
  If ``TabName`` is a "." (a dot), all tables with a "TKEY" will be sorted.
  No ``ColName`` is needed in this case.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).
  * ``dec`` - Sort in descending order. Default is ascending.


.. _`-exp`:

``-exp[,AtrLst] DbName:TabName``
  Export data.
  ``DbName`` is the database name (see `Target Database`_).
  ``TabName`` is a table/vector name in the database.
  To export the "PKEY" (bucket key) only, specify  a "." (a dot) as ``TabName``.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).


.. _`-cnt`:

``-cnt[,AtrLst] DbName:TabName``
  Count unique "PKEY" and rows.
  ``DbName`` is the database name (see `Target Database`_).
  ``TabName`` is a table/vector name in the database.
  To count "PKEY" (bucket key) only, specify  a "." (a dot) as ``TabName``.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).


.. _`-scn`:

``-scn[,AtrLst] DbName:TabName``
  Scan data only.
  This option is typically used along with certain data processing rules
  (see `Data Processing Steps`_) and/or a data processing module (see `-mod`_).
  There is no default output. However, if a module is used, it can output
  custom data.

  ``DbName`` is the database name (see `Target Database`_).
  ``TabName`` is a table/vector name in the database.
  To scan the user buckets only, specify  a "." (a dot) as ``TabName``.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Database`_).


.. _`-seed`:

``-seed RandSeed``
  Set the seed of random sequence used by the ``$Random``
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
    operation, at which point the columns are reset to 0 or blank.

  Example:

   ::

    $ aq_udb ... -var Var1 0 ...

  * Initialize Var1 in Var vector to 0 before any buctet is processed.


.. _`-bvar`:

``-bvar ColName Val``
  Same as `-var`_ except that the column is set to ``Val`` repeatedly
  in *each* bucket before other processing rules are executed.
  Note that a string ``Val`` must be quoted,
  see `String Constant`_ spec for details.

  This rule can also be used within a `-pp`_ group. In this case,
  ``ColName`` is set to ``Val`` in each bucket before other pre-processing
  rules are executed.

  See `Data Processing Steps`_ for details on these usages.

  Example:

   ::

    $ aq_udb ... -pp -bvar Var1 0 ...

  * Initialize Var1 in Var vector to 0 when *each* bucket is processed.


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
  columns from other user vectors, columns from the Var vector,
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
  * Operator precedency is *NOT* supported. Use '(' and ')' to group
    operations as appropriate.

  Builtin variables:

  ``$Random``
    A random number (postive integer).
    Its value changes every time the variable is referenced.
    The seed of this random sequence
    can be set using the `-seed`_ option.

  ``$RowNum``
    Represent the per bucket per table row index (one-based).
    It is generally used during a table scan to identify the current row number.

  Standard functions:

    See `aq-emod <aq-emod.html>`_ for a list of supported functions.

  Example:

   ::

    $ aq_udb -exp Test
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
      other user vectors, and/or the Var vector.
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

    $ aq_udb -exp Test
        -filt 't > 123456789'

  * Export only rows of Test with 't > 123456789'.

   ::

    $ aq_udb -exp Test
        -filt 'Eval($Random % 100) == 0'

  * Randomly select roughly 1/100th of the rows for export.


.. _`-goto`:

``-goto DestSpec``
  Go to ``DestSpec``. This is uaually done conditionally within a
  ``-if/-elif/-endif`` block (see `Rule Execution Controls`_ for details).

  ``DestSpec`` is the destination to go to. It is one of:

  * ``next_bucket`` - Skip the current user bucket entirely.cw
    The export/count/scan processing on this bucket will also be skipped.
  * ``next_row`` - Skip the current data row and start over on the next row.

  This rule can also be used within a `-pp`_ group. In this case,
  these additional destinations are supported:

  * ``proc_bucket`` - Terminate all ``-pp`` processings (i.e.,
    stop the current ``-pp`` group and skip all pending ``-pp`` groups)
    and start the export/count/scan operation in the current user bucket.
  * ``next_pp`` - Stop the current ``-pp`` group and start the next one.


.. _`-del_row`:

``-del_row[,AtrLst]``
  Delete the current row in the database. No more processing on the current
  row will be done.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``post=DestSpec`` - Set the action to take after the delete.
    ``DestSpec`` is one of:

    * ``next_bucket`` - Stop processing the current user bucket.
      Any export/count/scan processing on the remaining rows of this bucket
      will be skipped.
    * ``proc_bucket`` - Skip all pending ``-pp`` groups
      and start the export/count/scan operation in the current user bucket.
    * ``next_row`` - Start processing the next row. This is the default
      behavior.


.. _`-del_usr`:

``-del_usr[,AtrLst]``
  Delete the current user bucket in the database. No more processing on the
  current bucket will be done.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``post=DestSpec`` - Set the action to take after the delete.
    ``DestSpec`` is one of:

    * ``next_bucket`` - Start processing the next bucket. This is the default
      behavior.


.. _`-mod`:

``-mod ModSpec [ModSrc]``
  Specify a module to be loaded on the *server side* during an
  export/count/scan operation. A module contains one or more processing
  functions which are called in each user bucket according to the
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
  ``ModName``. Standard modules:

  ``roi("VecName.Count_Col", "TabName.Page_Col", "Page1[,AtrLst]", ...)``
    Module for ROI counting. ROI spec is given in the module arguments.
    There are 3 or more arguments:

    * ``VecName.Count_Col`` - Column to save matched count to.
      It must have type ``I``.
    * ``TabName.Page_Col`` - Column to get the match value from.
      It must have type ``S``. Rows in the table must already be in the
      desired ROI matching order (usually ascending time order).
    * ``PageN[,AtrLst]`` - One or more pages to match against the
      ``TabName.Page_Col`` value. Each page is given as a separate
      module argument.
      Optional ``AtrLst`` is a comma separated list containing:

      * ``ncas`` - Do case insensitive match.
      * ``seq`` - Require that the page match occur *immediately* after the
        previous match (i.e., no unmatch page in between).
        Applicable on the second page and up only.

    Either exact or wildcard match can be done. Exact match will either match
    the entire ``TabName.Page_Col`` value or up to (but not including) a
    '?' or '#' character.
    Wildcard match is done if ``Page`` contains '*' (matches any number of
    bytes) and/or '?' (matches any 1 byte).
    Literal ',', ':', '*', '?' and '\\' in ``Page`` must be '\\' escaped.


.. _`-pp`:

``-pp[,AtrLst] TabName [-bvar ... -eval ... -filt ... -goto ... -del_row ...] -endpp``
  ``-pp`` groups one or more `-bvar`_, `-eval`_, `-filt`_, `-goto`_,
  `-del_row`_ and `-del_usr`_ actions together.
  Each group performs pre-processing at the user bucket level *before*
  data in the bucket is exported/counted/scanned.
  See `Data Processing Steps`_ for details.

  ``TabName`` sets the target table/vector for the rules in the ``-pp`` group.
  It may refer to a table/vector or the user bucket itself.
  To target a table/vector, specify its name.
  To target the user bucket itself, specify  a "." (a dot).
  "." is a pseudo vector containing the "PKEY" columns.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``post=DestSpec`` - Set the action to take after all the rows in
    the target table has been exhausted.
    ``DestSpec`` is one of:

    * ``next_bucket`` - Skip the current user bucket entirely.
      The export/count/scan processing on this bucket will also be skipped.
    * ``proc_bucket`` - Skip all pending ``-pp`` groups
      and start the export/count/scan operation in the current user bucket.
    * ``next_pp`` - Start the next ``-pp`` group. This is the default behavior.

  The `-bvar`_ rules in the group are always executed first.
  Then the list of `-eval`_, `-filt`_, `-goto`_, `-del_row`_ and `-del_usr`_
  rules are executed in order.
  Rule executions can also be made conditional by adding "if-else" controls,
  see `Rule Execution Controls`_ for details.

  ``-endpp`` marks the end of a ``-pp`` group.

  Example:

   ::

    $ aq_udb -exp Test1
        -pp,post=next_bucket 'Test2'
          -goto proc_bucket

  * Only export Test1 from buckets whose Test2 table is not empty. If Test2 is
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

  * Randomly select roughly 1/100th of the buckets for export.
    From this subset, export only rows of Test with 't > 123456789'.
    Note that ``-endpp`` is mandatory here to prevent misinterpretation of the
    2nd ``-filt``.


.. _`-lim_usr`:

``-lim_usr Num``
  Limit export output to the given Num users. Default is 0, meaning no limit.

  **Note**: If the data is distributed over multiple servers, the result
  exported can be less than expected if ``Num`` is close to
  ``Total_Num_Users / Num_Servers``.


.. _`-lim_rec`:

``-lim_rec Num``
  Limit export output to the given Num records. Default is 0, meaning no limit.

  **Note**: If the data is distributed over multiple servers, the result
  exported can be less than expected if ``Num`` is close to
  ``Total_Num_Records / Num_Servers``.


.. _`-sort`:

``-sort[,AtrLst] ColName ... [-top Num]``
  `-exp`_ export output post processing option.
  This sets the output sort columns.
  Note that the sort columns must be in the output columns.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``dec`` - Sort in descending order. Default order is ascending.

  ``-top`` limits the output to the top ``Num`` records in the result.

  **Note**: Sort should *not* be used if the output contains columns
  other than those from the target table/vector (e.g. other vector columns).


.. _`-o`:

``-o[,AtrLst] File``
  Export output option.
  Set the output attributes and file.
  See the `aq_tool output specifications <aq-output.html>`_ manual for details.
  If this option is not used with an export, data is written to stdout.

  Example:

   ::

    $ aq_udb -exp Test ... -o,esc,noq -

  * Output to stdout in a format suitable for Amazon Cloud.


.. _`-c`:

``-c ColName [ColName ...]``
  Select columns to output during an export.

  * For a table/vector export, columns from the target table/vector,
    columns from other user vectors, and/or columns from the Var vector can
    be selected.
    Default output includes all target table/vector columns.

  * For a "PKEY" (bucket key) export, the "PKEY" columns,
    columns from any user vectors, and/or columns from the Var vector can
    be selected.
    Default output includes the "PKEY" columns only.

  * For a Var vector export, only columns from the Var vector can
    be selected.
    Default output includes all Var vector columns.

  To address columns other than those in the target table/vector, use the
  ``VecName.ColName`` format. For the Var vector, ``VecName`` is optional
  unless ``ColName`` also exists in the target.

  Example:

   ::

    $ aq_udb -exp Test ... -c Test_Col1 ... Test_ColN Var_Col1 ... Var_ColN

  * Output Var vector columns along with columns from Test.
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
* 11 - Input open error.
* 12 - Input read error.
* 13 - Input processing error.
* 21 - Output open error.
* 22 - Output write error.
* 31 - Udb connect error.
* 32 - Udb communication error.


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

* The spec file path can be given explicitly via the ``spec=UdbSpec`` attribute
  of the `-crt`_, `-ord`_, `-exp`_, `-cnt`_, `-scn`_, `-clr`_ or `-probe`_
  option.
* The spec file path can be deduced implicitly from the ``DbName`` parameters
  of the `-crt`_, `-ord`_, `-exp`_, `-cnt`_, `-scn`_, `-clr`_ or `-probe`_
  option.
  This method sets the spec file to "``.conf/DbName.spec``" in the current
  work directory of ``aq_udb``.
* If none of the above information is given, the spec file is assumed to be
  "``udb.spec``" in the current work directory of ``aq_udb``.


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
`-del_usr`_.

Example:

 ::

  $ aq_udb -exp Test
      -pp Test
        -bvar v_seq 0
        -if -filt 'flag == "yes"'
          -eval v_seq 'v_seq + 1'
          -eval c3 'v_seq'
        -else
          -eval c3 '0'
        -endif

* Before exporting Test, assign a per bucket sequence number to column c3 if
  the "flag" column is "yes" or just 0 otherwise.
  Note that `-bvar`_ rules are always executed before the others
  regardless of their placement within a `-pp`_ group.


Data Processing Steps
=====================

For each export/count/scan operation,
data is processed according to the commandline options in this way:

* Initialize Var columns according the `-var`_ options.

* Scan user buctets. For each user bucket in the database:

  * Execute `-pp`_ groups in the order they are specified on the
    commandline. For each ``-pp`` group:

    * Initialize Var columns according the `-bvar`_ rules.
    * Scan the ``-pp`` table. For each row in the table:

      * Execute the list of `-eval`_, `-filt`_, `-goto`_, `-del_row`_ and
        `-del_usr`_ rules (including any "-if-elif-else-endif" controls)
        in order.

    * When all the rows are exhausted, follow the ``post`` attribute
      setting or start the next group by default.

  * Initialize Var columns according the `-bvar`_ rules.

  * If a module is specified (see `-mod`_) and it has a user bucket processing
    function, the fuction is called.
    This function can inspect and/or modify arbitrary data in the bucket.
    It can also tell the server to skip the current bucket so that it will
    not be exported/counted/scanned.

  * Process the target export/count/scan table.
    For each data row in the target table:

    * Execute the list of `-eval`_, `-filt`_, `-goto`_, `-del_row`_ and 
      `-del_usr`_ rules (including any "-if-elif-else-endif" controls)
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
* `Example aq_udb Commands <../../usecases/syntaxexamples/aq_udb-option-examples.html>`_ - Additional examples of aq_udb options.

