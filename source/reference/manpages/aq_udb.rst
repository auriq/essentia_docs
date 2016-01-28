======
aq_udb
======


Synopsis
========

::

  aq_udb [-h] Global_Opt Export_Spec|Order_Spec|Mnt_Spec

  Global_Opt:
      [-test] [-verb] [-stat]
      [-spec UdbSpec | -db DbName]
      [-server AdrSpec [AdrSpec ...]]
      [-local]

  Export_Spec:
      -exp [DbName:]TabName | -cnt [DbName:]TabName | -scn [DbName:]TabName
      [-seed RandSeed]
      [-lim_usr Num] [-lim_rec Num]
      [-var ColName Val]
      [-bvar ColName Val]
      [-eval ColName Expr]
      [-filt FilterSpec]
      [-goto DestSpec]
      [-mod ModSpec]
      [-pp TabName
        [-bvar ColName Val]
        [-eval ColName Expr]
        [-filt FilterSpec]
        [-goto DestSpec]
        [-end_of_scan DestSpec]
      -endpp]
      [-sort[,AtrLst] [ColName ...] [-top Num]]
      [-o[,AtrLst] File] [-c ColName [ColName ...]]

  Order_Spec:
      -ord[,AtrLst] [DbName:]TabName [ColName ...]

  Mnt_Spec:
      -clr [DbName:]TabName | -probe


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
  Export data from ``TabName``.
  ``TabName`` refers to a table/vector defined in the Udb spec file
  (see `udb.spec <udb.spec.html>`_).
  To export the "PKEY" (bucket key) only, specify  a "." (a dot) as ``TabName``.
  Optional ``DbName`` sets the Udb spec file as in the `-db`_ option.


.. _`-cnt`:

``-cnt [DbName:]TabName``
  Retrieve the unique "PKEY" count and row count for ``TabName``.
  ``TabName`` refers to a table/vector defined in the Udb spec file
  (see `udb.spec <udb.spec.html>`_).
  To do a "PKEY" (bucket key) count only, specify  a "." (a dot) as ``TabName``.
  Optional ``DbName`` defines UdbSpec indirectly as in the `-db`_ option.


.. _`-scn`:

``-scn [DbName:]TabName``
  Scan data in ``TabName``.
  ``TabName`` refers to a table/vector defined in the Udb spec file
  (see `udb.spec <udb.spec.html>`_).
  To scan the user buckets only, specify  a "." (a dot) as ``TabName``.
  Optional ``DbName`` sets the Udb spec file as in the `-db`_ option.

  There is no default output.
  However, if used with a module (see `-mod`_),
  the module can optionally output custom data.
  This option is typically used with certain data inspection/modification
  rules/module.


.. _`-seed`:

``-seed RandSeed``
  Set the seed of random sequence used by the ``$Random``
  `-eval`_ builtin variable.


.. _`-lim_usr`:

``-lim_usr Num``
  Limit export output to the given Num users. Default is 0, meaning no limit.


.. _`-lim_rec`:

``-lim_rec Num``
  Limit export output to the given Num records. Default is 0, meaning no limit.


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
    Represent the per bucket per table row index.
    Index of the first row is 1.
    It is generally used during a table scan to identify the current row number.

  Builtin functions:

  ``ToIP(Val)``
    Returns the IP address value of ``Val``.
    ``Val`` can be a string/IP column's name, a `string constant`_,
    or an expression that evaluates to a string/IP.

  ``ToF(Val)``
    Returns the floating point value of ``Val``.
    ``Val`` can be a string/numeric column's name, a string/numeric constant,
    or an expression that evaluates to a string/number.

  ``ToI(Val)``
    Returns the integral value of ``Val``.
    ``Val`` can be a string/numeric column's name, a string/numeric constant,
    or an expression that evaluates to a string/number.

  ``ToS(Val)``
    Returns the string representation of ``Val``.
    ``Val`` can be a numeric column's name, a string/numeric/IP constant,
    or an expression that evaluates to a string/number/IP.

  ``Min(Val1, Val2 [, Val3 ...])``
    Returns the smallest among ``Val1``, ``Val2`` and so on.
    Values can be numeric column names, numbers,
    or expressions that evaluates to a number.

  ``Max(Val1, Val2 [, Val3 ...])``
    Returns the greatest among ``Val1``, ``Val2`` and so on.
    Values can be numeric column names, numbers,
    or expressions that evaluates to a number.

  ``PatCmp(Val, Pattern [, AtrLst])``
    Perform a pattern comparison between string value and a pattern.
    Returns 1 (True) if successful or 0 (False) otherwise.
    ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
    ``Pattern`` is a `string constant`_ specifying
    the pattern to match.
    ``AtrLst`` is a comma separated string list containing:

    * ``ncas`` - Do case insensitive pattern match (default is case sensitive).
      This has the same effect as the case insensitive operators below.
    * ``rx`` - Do Regular Expression matching.
    * ``rx_extended`` - Do Regular Expression matching.
      In addition, enable POSIX Extended Regular Expression syntax.
    * ``rx_newline`` - Do Regular Expression matching.
      In addition, apply certain newline matching restrictions.

    Without any of the Regular Expression related attributes,
    ``Pattern`` must be a simple wildcard pattern containing just '*'
    (matches any number of bytes) and '?' (matches any 1 byte) only;
    literal '*', '?' and '\\' in the pattern must be '\\' escaped.

    If any of the Regular Expression related attributes is enabled, then
    the pattern must be a GNU RegEx.

  ``SHash(Val)``
    Returns the numeric hash value of a string.
    ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.

  ``SLeng(Val)``
    Returns the length of a string.
    ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.

  ``KDec(Key, DecSpec)``
    Decode a key previously encoded via ``-kenc`` of `aq_pp <aq_pp.html>`_
    and place the results in columns.
    Returns the number of components in ``Key``. If the return value is not
    needed, invoke function using ``-eval - KDec(...)``.
    ``Key`` is the previously encoded value.
    It can be a string column's name, a `string constant`_
    or an expression that evaluates to a string.
    ``DecSpec`` is a `string constant`_ specifying
    how to decode ``Key``. It has the form:

     ::

      ColName;ColName[;ColName...]

    Each ``ColName`` specifies a decode-to column.
    Note that the decode-to column types must match those used in the
    original ``-kenc`` spec.
    If a decode-to value is not needed, specify ``ColType:`` (including
    the ":") in place of ``ColName``.

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

  ``FilterSpec`` is the filter to evaluate.
  It is evaluated on each data row in the target table according to the
  `Data Processing Steps`_.
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
  * ``+Num`` - Jump over Num `-eval`_, `-filt`_ and `-goto`_ rules.
    ``Num=0`` means the next rule, ``Num=1`` means skip over one rule, and so.

  This rule can also be used within a `-pp`_ group. In this case,
  these additional destinations are supported:

  * ``proc_bucket`` - Terminate all ``-pp`` processings (i.e.,
    stop the current ``-pp`` group and skip all pending ``-pp`` groups)
    and start the export/count/scan operation in the current user bucket.
  * ``next_pp`` - Stop the current ``-pp`` group and start the next one.


.. _`-mod`:

``-mod ModSpec``
  Specify a module to load on the *server side* during an export/count/scan
  operation.
  Only one such module can be specified.
  ``ModSpec`` has the form ``ModName[:argument]`` where ``ModName``
  is the logical module name and ``argument`` is a module specific
  parameter string. Udb server will try to load "umod/``ModName``.so"
  in the directory where ``udbd`` is installed.
  Module functions are called in each user bucket according to the
  `Data Processing Steps`_.

  Standard modules:

  ``roi``
    Module for ROI counting. ROI spec is given in the module argument:

     ::

      VecName.Count_Col:TabName.Page_Col:Page_1[,AtrLst]:Page_2[,AtrLst]:...

    * ``VecName.Count_Col`` - Column to save matched count to.
      It must have type ``I``.
    * ``TabName.Page_Col`` - Column to get the match value from.
      It must have type ``S``. Rows in the table must already be in the
      desired ROI matching order (usually ascending time order).
    * Page_N[,AtrLst] - One or more ``Pages`` to match against the
      ``TabName.Page_Col`` value.
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
.. _`-end_of_scan`:

``-pp TabName [-bvar ... -eval ... -filt ... -goto ... -end_of_scan ...] -endpp``
  ``-pp`` groups one or more `-bvar`_, `-eval`_, `-filt`_ and/or `-goto`_
  actions together.
  Each group performs pre-processing at the user bucket level before
  data in the bucket is exported/counted/scanned.

  ``TabName`` sets the target table/vector for the rules in the ``-pp`` group.
  It may refer to a table/vector or the user bucket itself.
  To target a table/vector, specify its name.
  To target the "PKEY" (bucket key), specify  a "." (a dot).
  "." is a pseudo vector containing a single read only "PKEY" column.

  The list of `-eval`_, `-filt`_ and `-goto`_ rules are generally
  executed in order. See `Data Processing Steps`_ for details.
  Rule executions can also be made conditional by adding "if-else" controls.
  See `Rule Execution Controls`_ for details.

  ``-end_of_scan DestSpec`` - a special rule that defines the
  action to take after all the rows in the target table has been exhausted.
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

  ``-endpp`` marks the end of a ``-pp`` group.

  Example:

   ::

    $ aq_udb -exp Test1
        -pp 'Test2'
          -goto proc_bucket
          -end_of_scan next_bucket

  * Only export Test1 from buckets whose Test2 table is not empty. If Test2 is
    not empty, the ``-goto`` rule will be executed on the first row, causing
    execution to jump to export processing; in this way, the end-of-scan
    condition is not triggered. However, if Test2 is empty, ``-goto``
    is not executed and end-of-scan is triggered.

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


.. _`-sort`:

``-sort[,AtrLst] [ColName ...] [-top Num]``
  `-exp`_ output post processing option.

  When exporting a table/vector,
  use ``ColName`` to set the desired sort columns.
  If no ``ColName`` is given, the "PKEY" column is assumed.
  The sort columns must be in the output columns.

  When exporting the "PKEY" (bucket key) only, no ``ColName`` is needed.
  Sort is always done by the "PKEY".

  Optional ``AtrLst`` is a comma separated list containing:

  * ``dec`` - Sort in descending order. Default order is ascending.

  ``-top`` limits the output to the top ``Num`` records in the result.

  **Note**: Sort should *not* be used if the output contains columns
  other than those from the target table/vector (e.g. other vector columns).


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

  * When exporting an user table/vector, columns from the target table/vector,
    columns from other user vectors, and/or columns from the Var vector can
    be selected.
    Default output includes all target table/vector columns.

  * When exporting the "PKEY" (bucket key), the "PKEY" column,
    columns from any user vectors, and/or columns from the Var vector can
    be selected.
    Default output includes the "PKEY" column only.

  * When exporting the Var vector, only columns from the Var vector can
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


.. _`-ord`:

``-ord[,AtrLst] [DbName:]TabName [ColName ...]``
  Sort records in table ``TabName`` within each bucket.
  Optional ``DbName`` sets the Udb spec file as in the `-db`_ option.
  ``ColName`` sets the desired sort columns.
  If no ``ColName`` is given, the "TKEY" column is assumed
  (see `udb.spec <udb.spec.html>`_).
  Optional ``AtrLst`` is a comma separated list containing:

  * ``dec`` - Sort in descending order. Default order is ascending.

  If ``TabName`` is a "." (a dot), all tables with a "TKEY" will be sorted.
  No ``ColName`` is needed in this case.


.. _`-clr`:

``-clr [DbName:]TabName``
  Remove/reset ``TabName`` data in the database.
  Optional ``DbName`` sets the Udb spec file as in the `-db`_ option.

  * For a table, the records are removed.
  * For a vector, the columns are reset to 0/blank.
  * For the Var vector (i.e., when ``TabName`` is "var"), the columns are reset
    to 0/blank.

  If ``TabName`` is a "." (a dot), all user buckets will be removed,
  along with all tables/vectors in the buckets.
  The Var vector will be reset as well.


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
* 1 - Memory allocation error.
* 2 - Command option spec error.
* 3 - Initialization error.
* 11 - Input open error.
* 13 - Input processing error.
* 21 - Output open error.
* 22 - Output write error.
* 31 - Udb connect error.
* 32 - Udb communication error.


Output File Attributes
======================

Some output file can have these comma separated attributes:

* ``app`` - Append to file; otherwise, file is overwritten by default.
* ``bin`` - Input in binary format (default is CSV).
* ``esc`` - Use '\\' to escape ',', '"' and '\\' (CSV).
* ``noq`` - Do not quote string fields (CSV).
* ``fmt_g`` - Use "%g" as print format for ``F`` type columns. Only use this
  to aid data inspection (e.g., during integrity check or debugging).
* ``notitle`` - Suppress the column name label row from the output.
  A label row is normally included by default.

By default, output is in CSV format. Use the ``esc`` and ``noq`` attributes to
set output characteristics as needed.


String Constant
===============

A string constant must be quoted between double or single quotes.
With *double* quotes, special character sequences can be used to represent
special characters.
With *single* quotes, no special sequence is recognized; in other words,
a single quote cannot occur between single quotes.

Character sequences recognized between *double* quotes are:

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

Beyond these, other special sequences may be recognized depending on where
the string is used. For example, in a simple wildcard pattern
(see ``PatCmp()``), ``\?`` and ``\*`` represent literal ``?`` and ``*``
respectively.
Sequences that are not recognized will be kept as-is. For example, in ``\a``,
the backslash will not be removed.

Two or more quoted strings can be used back to back to form a single string.
For example,

 ::

  'a "b" c'" d 'e' f" => a "b" c d 'e' f


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
Suppoeted ``RuleToRun`` are `-eval`_, `-filt`_ and `-goto`_.

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

      * Execute the list of `-eval`_, `-filt`_ and `-goto`_ rules
        (including any "-if-elif-else-endif" controls) in order.

    * When all the rows are exhausted, execute the `-end_of_scan`_ rule.

  * Initialize Var columns according the `-bvar`_ rules for the target table.

  * If a module is specified (see `-mod`_), call its user bucket processing
    function (if any).
    This function can inspect and/or modify arbitrary data in the bucket.
    It can also tell the server to skip the current bucket so that it will
    not be exported/counted/scanned.

  * Process the target export/count/scan table.
    For each data row in the target table:

    * Execute the list of `-eval`_, `-filt`_ and `-goto`_ rules
      (including any "-if-elif-else-endif" controls) in order.
    * If a module is specified (see `-mod`_), call its row processing
      function (if any).
      This function can inspect and/or modify the current data row.
      It can also tell the server to skip the current row so that it will
      not be exported/counted/scanned.
    * Export/count, the current data row.


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udb.spec <udb.spec.html>`_ - Udb spec file.
* `udbd <udbd.html>`_ - User (Bucket) Database server
* :doc:`../../usecases/syntaxexamples/aq_udb-option-examples` - Further examples of aq_udb options.

