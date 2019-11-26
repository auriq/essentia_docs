.. |<br>| raw:: html

   <br>

=====
aq_pp
=====

Record preprocessor

Interactive examples of using this command and/or its options are available at `aq_pp - Essentia playground <https://essentia-playground.auriq.com/notebooks/README.ipynb>`_


Synopsis
========

::

  aq_pp [-h] Global_Opt Input_Spec Prep_Spec Process_Spec Output_Spec

  Global_Opt:
      [-verb] [-stat] [-test]

  Input_Spec:
      [-f[,AtrLst] File [File ...]] [-d ColSpec [ColSpec ...]] |
      [-exp[,AtrLst]|-cnt[,AtrLst] DbName[:TabName] [ExpOpts ...] --]
      [-cat[,AtrLst] File [File ...] ColSpec [ColSpec ...]]

  Prep_Spec:
      [-seed RandSeed]
      [-var ColSpec Val]
      [-alias ColName AltName]
      [-renam ColName NewName]

  Process_Spec:
      [-eval ColSpec|ColName Expr]
      [-mapf[,AtrLst] ColName MapFrom] [-mapc ColSpec|ColName MapTo]
      [-kenc ColSpec|ColName ColName [ColName ...]]
      [-kdec ColName ColSpec|ColName[+] [ColSpec|ColName[+] ...]]
      [-filt FilterSpec]
      [-map[,AtrLst] ColName MapFrom MapTo]
      [-sub[,AtrLst] ColName File [File ...] [ColSPec ...]]
      [-grep[,AtrLst] ColName File [File ...] [ColSPec ...]]
      [-cmb[,AtrLst] File [File ...] ColSpec [ColSpec ...]]
      [-pmod ModSpec [ModSrc]]

  Output_Spec:
      [-o[,AtrLst] File] [-c ColName [ColName ...]]
      [-ovar[,AtrLst] File [-c ColName [ColName ...]]]
      [-imp[,AtrLst] DbName[:TabName] [-server AdrSpec [AdrSpec ...]] [-local]
        [-mod ModSpec [ModSrc]]


Description
===========

``aq_pp`` is a *stream-based* record processing tool.
It loads and processes records on at a time through these simple steps:

* First, it reads data from the input in various formats (e.g., CSV)
  according to the input spec.
* Then it converts the input into an internal data row
  according to the column spec.
* The row is then passed through a *processing chain*
  according to the processing spec.
* The data row, or any of its columns, can be output at any point in the chain.
  A row can also be output multiple times with varying values,
  or it needs not be output at all.

Other characteristics of the tool include:

* Columns are typed - numbers, string and IP. Column operations are also
  type specific.
* Besides the input columns, new columns can be added dynamically
  through the processing chain.
* *Variables* can also be added dynamically. They differ from columns
  in that their values persist across input rows, while column values are
  updated at each row. For example, a variable can be used to calculate the
  sum of a column over all rows in a data set.
* A variety of processing options are supported to populate and modify
  column values. An example is `-eval`_ which sets a column's value
  according to the evaluated result of an expression.
* A variety of processing options are supported to select (or filter) data
  rows. An example is `-filt`_ which filters-in records
  according to the logical result of an expression.
* Custom *modules* can be used to augment processing.
  One module type supplies custom processing functions for use in
  evaluation expressions.
  Another module type operates on the data row directly.
* `Conditional processing groups`_ can be used to control execution within
  the chain.  For example, a `-filt`_ can control whether to
  perform a `-eval`. Even the outputs can be controlled this way.
* Result can go to files, stdout and/or another processing layer called Udb.

With its stream-based design, ``aq_pp`` can process an unlimited amount of
data using a constant amount of memory.
For this reason, it is well suited for the *pre-processing* of large amount of
raw data, where the extracted and transformed result is used to generate
higher level analytics.


Options
=======

.. _`-test`:

``-test``
  Test command line arguments and exit.
  If specified twice (``-test -test``), a more throughout test will be
  attempted. For example, the program will try to load lookup files and
  connect to Udb in test mode.

  * If all specs are good, the exit code will be 0.
  * If there is an error, the exit code will be non-zero. Usually, an error
    message will also be printed to stderr.


.. _`-verb`:

``-verb``
  Verbose - print program progress to stderr while processing.
  Usually, a marker is printed for each 10,000,000 records processed.


.. _`-stat`:

``-stat``
  Print a record count summary line to stderr at the end of processing.
  The line has the form:

   ::

    aq_pp: rec=Count err=Count out=Count


.. _`-f`:

``-f[,AtrLst] File [File ...]``
  Set the input attributes and files.
  See the `aq_tool input specifications <aq-input.html>`_ manual for details.

  Example:

   ::

    $ aq_pp ... -f,+1l file1 file2 ...

  * Skip the first line from both files before loading.


.. _`-d`:

``-d ColSpec [ColSpec ...]``
  Define the input data columns.
  See the `aq_tool input specifications <aq-input.html>`_ manual for details.
  In general, ``ColSpec`` has the form ``Type[,AtrLst]:ColName``.
  Supported ``Types`` are:

  * ``S`` - String.
  * ``F`` - Double precision floating point.
  * ``L`` - 64-bit unsigned integer.
  * ``LS`` - 64-bit signed integer.
  * ``I`` - 32-bit unsigned integer.
  * ``IS`` - 32-bit signed integer.
  * ``IP`` - v4/v6 address.

  Optional ``AtrLst`` is a comma separated list of column specific attributes.
  ``ColName`` is the column name (case insensitive). It can contain up to
  31 alphanumeric and '_' characters. Its first character cannot be a digit.

  Example:

   ::

    $ aq_pp ... -d s:Col1 s,lo:Col2 i,trm:Col3 ...

  * Col1 is a string. Col2 is also a string, but the input value will be
    converted to lower case. Col3 is an unsigned integer, the ``trm``
    attribute removes blanks around the value before it is converted to
    an internal number.


.. _`-exp`:

``-exp[,AtrLst]|-cnt[,AtrLst] DbName[:TabName] [ExpOpts ...] --``
  Get the input data from an Udb export or count operation.
  This will set the data source as well as the column definitions,
  so -f`_ and `-d`_ are *not* needed.
  ``DbName`` is the database name (see `Target Udb Database`_).
  ``TabName`` is a table/vector name in the database to export.
  If ``TabName`` is not given or if it is a "." (a dot), the primary keys
  will be exported/counted.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Udb Database`_).

  ``ExpOpts`` are the ``-exp`` or ``-cnt`` related options as decribed in
  `aq_udb <aq_udb.html>`_ (except ``-o`` which is not applicable here).
  A ``--`` must be specified following the last ``ExpOpts``. Options given
  after ``--`` will be interpreted as ``aq_pp`` options.

  Example:

   ::

    $ aq_pp ... -exp mydb:Test -filt 'Col3 > 123456789' -- ...
    $ aq_pp ... -exp mydb:Test -- -filt 'Col3 > 123456789' ...

  * Use Test's data as the input. The two examples produce the same result.
    However, the first form is more efficient because the filter is done
    inside Udb so that less data is processed by ``aq_pp``.


.. _`-cat`:

``-cat[,AtrLst] File [File ...] ColSpec [ColSpec ...]``
  Add rows from ``Files`` to the `-f`_ data set.
  The file and column specifications are the same as in the `-f`_ and `-d`_
  options.
  See the `aq_tool input specifications <aq-input.html>`_ manual for details.

  Note that the columns need not be the same as those from `-d`_ (by name).
  If they differ, a super set is constructed.
  Multiple ``-cat`` can be used such that the final data set will contain
  unique columns from `-d`_ and all `-cat`_.
  Columns that do not exist in a data set will be set to zero or blank
  when that data set is loaded.

  Example:

   ::

    $ aq_pp ... -d s:Col1 s:Col2 i:Col3 s:Col4 ...
        -cat more.csv i:Col3 s:Col1 s:Col5 s:Col6
        ...

  * Add data from "``more.csv``". Column Col3 and Col1 are common,
    so the resulting data set will have Col1, Col2, Col3, Col4, Col5 and Col6.
    Since the main data set does not have Col5 and Col6, they are set to
    blank when it is loaded.
    Similarly, since "``more.csv``" does not have Col2 and Col4,
    they are set to blank when it is loaded.


.. _`-seed`:

``-seed RandSeed``
  Set the random sequence seed of the ``$Random`` evaluation builtin variable.
  Default seed is 1.


.. _`-var`:

``-var ColSpec Val``
  Define a new variable and initialize its value to Val.
  A variable stores a value that persists between rows over the entire run.
  Recall that normal column values change from row to row.
  ``ColSpec`` is the variable's spec in the form ``Type:ColName`` where Type
  is the data type and ColName is the variable's name, see `-d`_ for details.
  Note that a string ``Val`` must be quoted,
  see `String Constant`_ spec for details.

  A variable can also be used in conjunction with ``-o,fvar VarName`` to
  specify a dynamic output target (the variable must be a string in this case).
  See the ``fvar`` description under `-o`_ for details.

  Example:

   ::

    $ aq_pp ... -d i:Col1 ...
        -var 'i:Sum' 0 ...
        -eval 'Sum' 'Sum + Col1' ...

  * Initialize variable Sum to 0, then update the rolling sum for each row.


.. _`-alias`:

``-alias ColName AltName``
  Set a column alias.
  `` ColName`` refers to a previously defined column/variable/alias.
  ``AltName`` is the desired alias. An alias allow the same column to be
  addressed using multiple names.
  If the original column is no longer needed, use `-renam`_ instead.


.. _`-renam`:

``-renam ColName NewName``
  Rename a column or an alias.
  `` ColName`` refers to a previously defined column/variable/alias.
  ``NewName`` is the new name of the column/variable/alias.
  addressed using multiple names.


.. _`-eval`:
   
``-eval ColSpec|ColName Expr``
  Examples are also available in `aq_pp -eval - Essentia Playground <https://essentia-playground.auriq.com/notebooks/aq_pp%20-eval.ipynb>`_.

  Evaluate ``Expr`` and save the result to a column. The column can be a new
  column, an existing column/variable or null as explained below.

  * If a ``-`` is given, the result will not be saved anywhere. This is
    useful when calling a function that puts its result in destinated columns
    by itself.
  * If ``ColSpec`` is given, a new column will be created using the spec.
    See `-d`_ for details. Note that the new column cannot participate in
    ``Expr``.
  * If `` ColName`` is given, it must refer to a previously defined
    column/variable.

  ``Expr`` is the expression to evaluate.
  Data type of the evaluated result must be compatible with the data type of
  the target column. For example, string result for a string column and
  numeric result for a numeric column (there is no automatic type conversion;
  however, explicit conversion can be done using the ``To*()`` functions
  described below).
  Operands in the expression can be the names of previously defined columns or
  variables, constants, builtin variables and functions.

  * Column names are case insensitive. Do not quote the name.
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



  .. _`builtin variables`:

  Builtin variables:

  ``$Random``
    A random number (postive integer).
    Its value changes every time the variable is referenced.
    The seed of this random sequence can be set using the `-seed`_ option.

  ``$RowNum``
    The input row index (one-based).

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

    $ aq_pp ... -d i:Col1 ... -eval l:Col_evl 'Col1 * 10' ...

  * Set new column Col_evl to 10 times the value of Col1.

   ::

    $ aq_pp ... -d s:Col1 s:Col2 ...
        -eval is:Dt 'DateToTime(Col2, "Y.m.d.H.M.S.p") - DateToTime(Col1, "Y.m.d.H.M.S.p")'
        ...

  * Col1 and Col2 are date strings of the form "Year/Month/day Hour:Min:Sec AM".
    Dt will contain the time difference in seconds.




.. _`-mapf`:

``-mapf[,AtrLst] ColName MapFrom``
  Examples are also available on aq_pp -map - `Essentia Playground <https://essentia-playground.auriq.com/notebooks/aq_pp%20-map.ipynb>`_.

  Extract data from a string column. This option should be used in
  conjunction with `-mapc`_.
  ``ColName`` is a previously defined column/variable to extract data from.
  ``MapFrom`` defines the extraction rule.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``ncas`` - Do case insensitive match (default is case sensitive).
    For ASCII data only.
  * One or more `regular expression attributes <aq-emod.html#regex-attributes>`_.

  If any of the regular expression related attributes are enabled, then
  ``MapFrom`` must use the `RegEx MapFrom Syntax`_.
  Otherwise, it must use the `RT MapFrom Syntax`_.


.. _`-mapc`:

``-mapc ColSpec|ColName MapTo``
  Render data extracted via previous `-mapf`_ into a new
  column or into an existing column/variable.
  The column must be of string type.

  * If ``ColSpec`` is given, a new column will be created using the spec.
    See `-d`_ for details.
  * If ``ColName`` is given, it must refer to a previously defined
    column/variable.

  ``MapTo`` is the rendering spec. See `MapTo Syntax`_ for details.

  Example:

   ::

    $ aq_pp ... -d s:Col1 s:Col2 s:Col3 ...
        -mapf Col1 '%%v1_beg%%.%%v1_end%%'
        -mapf,rx Col2 '\(.*\)-\(.*\)'
        -mapf,rx Col3 '\(.*\)_\(.*\)'
        -mapc s:Col_beg '%%v1_beg%%,%%1%%,%%4%%'
        -mapc s:Col_end '%%v1_end%%,%%2%%,%%5%%'
        ...

  * Extract data from Col1, Col2 and Col3. Then put "parts" of these columns
    in two new columns.
    Note that the RegEx based ``MapFrom`` expressions do not have named
    placeholders for the extracted data. Placeholders are interpreted
    implicitly from the the expressions in this way.
  * ``%%0%%`` - Represent the entire match in the first ``-mapf,rx``
    (not used in example).
  * ``%%1%%`` - Represent the 1st subpattern match in the first ``-mapf,rx``.
  * ``%%2%%`` - Represent the 2nd subpattern match in the first ``-mapf,rx``.
  * ``%%3%%`` - Represent the entire match in the second ``-mapf,rx``
    (not used in example).
  * ``%%4%%`` - Represent the 1st subpattern match in the second ``-mapf,rx``.
  * ``%%5%%`` - Represent the 2nd subpattern match in the second ``-mapf,rx``.

  * In


.. _`-kenc`:

``-kenc ColSpec|ColName ColName [ColName ...]``
  Encode a *key* column from the given ``ColNames``.
  The *key* column must be of string type.
  The *encoded* value it stores constains binary data.

  * If ``ColSpec`` is given, a new column will be created using the spec.
    See `-d`_ for details.
  * If ``ColName`` is given, it must refer to a previously defined
    column/variable.

  The source ``ColNames`` must be previously defined.
  They can have any data type.

  Example:

   ::

    $ aq_pp ... -d s:Col1 i:Col2 ip:Col3 ...
        -kenc s:Key1 Col1 Col2 Col3
        ...

  * Compose a new "composite" column Key1 from Col1, Col2 and Col3.


.. _`-kdec`:

``-kdec ColName ColSpec|ColName[+] [ColSpec|ColName[+] ...]``
  Decode a *key* column given by ``ColName`` into one or more columns
  given by ``ColSpec`` (new column) or ``ColName`` (existing column/variable).
  The *key* ``ColName`` must be an existing string column/variable.
  For the decode-to columns, possible specs are:

  ``Type:ColName[+]``
    Extract column value into the newly defined column.
    With an optional '+', the extracted value will also be encoded back into
    the key.

  ``ColName[+]``
    Extract column value into an existing column or variable.
    With an optional '+', the extracted value will also be encoded back into
    the key.

  ``Type:[+]``
    Like specifying a new column, but with a blank column name.
    This means that the extracted value will not be saved in another column.
    With an optional '+', the extracted value will be encoded back into
    the key.

  Note that the decode-to column types must match those used in the original
  `-kenc`_ spec.

  Example:

   ::

    $ aq_pp ... -d s:Key1 ...
        -kdec Key1 s:Col1 i:Col2 ip:Col3
        ...

  * Extract Col1, Col2 and Col3 from Key1.

   ::

    $ aq_pp ... -d s:Key1 ...
        -kdec Key1 s: i:Col2 ip:
        ...

  * Extract only Col2 from Key1. Since there is no '+' in the extract-to spec,
    the value of Key1 is NOT altered.

   ::

    $ aq_pp ... -d s:Key1 ...
        -kdec Key1 s: i:Col2+ ip:+
        -kdec Key1 i: ip:Col3
        ...

  * In the first rule, Col2 is extracted from Key1. At the same time,
    the 2nd and 3rd fields are encoded back into Key1.
    In the second rule. Col3 is extracted from the new value of Key1.


.. _`-filt`:

``-filt FilterSpec``
  Examples for this option are also available on `aq_pp -filt - Essentia Playground <https://essentia-playground.auriq.com/notebooks/aq_pp%20-filt.ipynb>`_.

  Filter (or select) records based on ``FilterSpec``.
  ``FilterSpec`` is a logical expression that evaluates to either true or false
  for each record - if true, the record is selected; otherwise, it is
  discarded.
  It has the basic form ``[!] LHS [<compare> RHS]`` where:

  * The negation operator ``!`` negates the result of the comparison.
    It is recommended that ``!(...)`` be used to clarify the intended
    operation even though it is not required.
  * LHS and RHS can be:

    * A column/variable name (case insensitive). Do not quote the name.
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

    $ aq_pp ... -d s:Col1 s:Col2 i:Col3 s:Col4 ...
        -filt 'Col1 === Col4 && Col2 != "" && Col3 >= 100'
        ...

  * Only keep records whose Col1 and Col4 are the same (case insensitive) and
    Col2 is not blank and Col3's value is greater than or equal to 100.


.. _`-map`:

``-map[,AtrLst] ColName MapFrom MapTo``
  Remap (a.k.a., rewrite) a string column's value.
  ``ColName`` is a previously defined column/variable.
  ``MapFrom`` defines the extraction rule.
  ``MapTo`` is the rendering spec. See `MapTo Syntax`_ for details.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``ncas`` - Do case insensitive match (default is case sensitive).
    For ASCII data only.
  * One or more `regular expression attributes <aq-emod.html#regex-attributes>`_.

  If any of the regular expression related attributes are enabled, then
  ``MapFrom`` must use the `RegEx MapFrom Syntax`_.
  Otherwise, it must use the `RT MapFrom Syntax`_.

  Example:

   ::

    $ aq_pp ... -d s:Col1 ...
        -map Col1 '%%v1_beg%%-%*' 'beg=%%v1_beg%%'
        ...
    $ aq_pp ... -d s:Col1 ...
        -map,rx Col1 '\(.*\)-*' 'beg=%%1%%'
        ...

  * Both commands rewrite Col1 in the same way.


.. _`-sub`:

``-sub[,AtrLst] ColName File [File ...] [ColSpec ...]``
  Replace the values of ``ColName``, a string column in the current data set,
  with values from a lookup table loaded from ``Files``.
  Optional ``AtrLst`` is a comma separated list containing:

  * Standard `input attributes <aq-input.html#input-file-option>`_ described
    in the `aq_tool input specifications <aq-input.html>`_ manual.
  * ``ncas`` - Do case insensitive match (default is case sensitive).
    For ASCII data only.
  * ``pat`` - Support '?' and '*' wild cards in the "From" value. Literal '?',
    '*' and '\\' must be escaped by a '\\'. Without this attribute,
    "From" value is assumed constant and no escape is necessary.
  * ``req`` - Discard records not matching any entry in the lookup table.
    Normally, column value will remain unchanged if there is no match.
  * ``all`` - Use all matches. Normally, only the first match is used.
    With this attribute, one row is produced for each match.

  ``ColSpecs`` define the `input columns <aq-input.html#column-spec>`_ as
  described in the `aq_tool input specifications <aq-input.html>`_ manual.
  The spec is optional, default is "``S:from S:to``" (or just "``from to``").
  If a spec is defined, it must include these 2 columns (by name):

  * ``from`` - Marks the column used to match the value of ``ColName``.
    It must have a string type.
  * ``to`` - Marks the column used as the new value of ``ColName``.
    It must have a string type.

  The *from* values are generally literals. Patterns can be used if
  the ``pat`` attribute description above is set.
  The *to* values are always literals.
  Matches are carried out according to the order of the match value in the
  files. Match stops when the first match is found. If the files contain both
  exact value and pattern, then:

  * Exact values are matched first, skipping over any interleaving patterns.
  * Patterns are matched next, skipping over any interleaving fixed values.

  Example:

   ::

    $ aq_pp ... -d s:Col1 ... -sub Col1 lookup.csv TO X FROM ...

  * Substitute Col1 according to lookup table. The data in the lookup table
    is not in the default "``from to``" format, so the column spec must be
    given. The ``X`` in the spec marks an unneeded column.


.. _`-grep`:

``-grep[,AtrLst] ColName File [File ...] [ColSpec ...]``
  Filter by matching the value of ``ColName``, a string column in the current
  data set, against the values loaded from ``Files``.
  Optional ``AtrLst`` is a comma separated list containing:

  * Standard `input attributes <aq-input.html#input-file-option>`_ described
    in the `aq_tool input specifications <aq-input.html>`_ manual.
  * ``ncas`` - Do case insensitive match (default is case sensitive).
    For ASCII data only.
  * ``pat`` - Support '?' and '*' wild cards in the "From" value. Literal '?',
    '*' and '\\' must be escaped by a '\\'. Without this attribute,
    match value is assumed constant and no escape is necessary.
  * rev - Reverse logic, select records that do not match.

  ``ColSpecs`` define the `input columns <aq-input.html#column-spec>`_ as
  described in the `aq_tool input specifications <aq-input.html>`_ manual.
  The spec is optional, default is "``S:from``" (or just "``from``").
  If a spec is defined, it must include 1 column (by name):

  * ``from`` - Marks the column used to match the value of ``ColName``.
    It must have a string type.

  The *from* values are generally literals. Patterns can be used if
  the ``pat`` attribute description above is set.
  Matches are carried out according to the order of the match value in the
  files. Match stops when the first match is found. If the files contain both
  exact value and pattern, then:

  * Exact values are matched first, skipping over any interleaving patterns.
  * Patterns are matched next, skipping over any interleaving fixed values.

  Example:

   ::

    $ aq_pp ... -d s:Col1 ... -grep,rev Col1 lookup.csv X X FROM ...

  * Select (or retain) only records whose Col1 values are not in lookup table.
    The data in the lookup table is not in the default format, so the column
    spec must be given. The ``X``'s in the spec mark the unneeded columns.


.. _`-cmb`:

``-cmb[,AtrLst] File [File ...] ColSpec [ColSpec ...]``
  Examples for this option are available on aq_pp -cmb - `Essentia Playground <https://essentia-playground.auriq.com/notebooks/aq_pp%20-cmb.ipynb>`_.

  Combine data from ``Files`` into the current data set by joining rows
  from both data sets. The new data set will contain unique columns from
  both sets. Common columns are automatically used as the join keys
  (see ``ColSpec`` description on how to customize join keys).
  Optional ``AtrLst`` is a comma separated list containing:

  * Standard `input attributes <aq-input.html#input-file-option>`_ described
    in the `aq_tool input specifications <aq-input.html>`_ manual.
  * ``ncas`` - Do case insensitive match (default is case sensitive).
    For ASCII data only.
  * ``req`` - Discard unmatched records.
  * ``all`` - Use all matches. Normally, only the first match is used.
    With this attribute, one row is produced for each match.
  * ``mrg`` - Use *merge* mode. Records in the current data set and in
    in the combine files must already be *sorted* according to the combine keys
    in the same order (default is ascending unless ``dec`` is given).
    Use this approach if the combine data is too large to fit into memory.
  * ``dec`` - Same as ``mrg`` except that all the data are sorted in descending
    order.

  ``ColSpecs`` define the `input columns <aq-input.html#column-spec>`_ as
  described in the `aq_tool input specifications <aq-input.html>`_ manual.
  with these column attribute extensions:

  * ``key`` - Marks a column as being a join key. It must be a common column.
    This is the default for a common column.
  * ``cmb`` - Marks a column to be combined into the current data set.
    This is the default for a non-common column.
    It is typically used to mark a common column as *not* a join key.

  Example:

   ::

    $ aq_pp ... -d s:Col1 s:Col2 i:Col3 s:Col4 ...
        -cmb lookup.csv i:Col3 s:Col1 s:Col5 s:Col6
        ...

  * Combine lookup.csv into the data set according to composite key
    <Col3, Col1>.
    The resulting data set will have columns Col1, Col2, Col3, Col4, Col5 and
    Col6.

   ::

    $ aq_pp ... -d s:Col1 s:Col2 i:Col3 s:Col4 ...
        -cmb lookup.csv i:Col3 s:Col1 s:Col5 s:Col6 s,cmb:Col2
        ...
    $ aq_pp ... -d s:Col1 s:Col2 i:Col3 s:Col4 ...
        -cmb lookup.csv i,key:Col3 s,key:Col1 s,cmb:Col5 s,cmb:Col6 s,cmb:Col2
        ...

  * Both are the same as the previous example, except that Col2 is explicitly
    set as a combine column. That is, its value will originally come from the
    current data set, then it will be overwritten if there is a match from the
    lookup table.


.. _`-pmod`:

``-pmod ModSpec [ModSrc]``
  Use the processing function in the given module to process the current record.
  The function is typically used to implement custom logics.

  * Retrieve and/or modify one or more columns in the current data row.
  * Filter out the current data row.
  * Generate multiple output rows from the current row.
  * Stop processing.

  ``ModSpec`` has the form ``ModName`` or ``ModName("Arg1", "Arg2", ...)``
  where ``ModName`` is the module name and ``Arg*`` are module dependent
  arguments. Note that the arguments must be string constants;
  for this reason, they must be quoted according to the
  `string constant`_ spec.

  ``ModSrc`` is an optional module source file. It can be:

  * A module script source file that can be used to build the specified
    module. See the `aq_pp module script compiler <mcc.pmod.html>`_
    documentation for more information.
  * A ready-to-use module object file. It *must* have a ``.so`` extension.

  Without ``ModSrc``, ``aq_pp`` will look for a preinstalled module matching
  ``ModName``. Standard modules:

  ``unwrap_strv("From_Col", "From_Sep", "To_Col" [, "AtrLst"])``
    Unwrap a delimiter separated string column into none or more values.
    The row will be replicated for each of the unwrapped values.
    This module requires 3 or 4 arguments:

    * ``From_Col`` - Column containing the string value to unwrap.
      It must have type ``S``.
    * ``From_Sep`` - The single byte delimiter that separate individual
      values. The delimiter must be given as-is, no escape is recognized.
    * ``To_Col`` - Column to save each unwrapped value to.
      It must have type ``S``. The ``To_Col`` can be the same as the
      ``From_Col`` - the module will remember the original ``From_Col``
      value.
    * ``AtrLst`` - Optional. A comma separated attribute list containing:

      * ``relax`` - No trailing delimiter. One is expected by default.
      * ``noblank`` - Skip blank values. Blanks are kept by default.


.. _`-o`:

``[-o[,AtrLst] File] [-c ColName [ColName ...]]``
  Examples for output specs are available on aq-output - `Essentia Playground <https://essentia-playground.auriq.com/notebooks/aq_output.ipynb>`_ .

  Output data rows. Multiple sets of "``-o ... -c ...``" can be specified.

  Optional "``-o[,AtrLst] File``" sets the output attributes and file.
  See the `aq_tool output specifications <aq-output.html>`_ manual for details.
  In addition, the following attribute is supported:

  * ``fvar`` - Output to a dynamically defined target. ``File`` is the name of
    a previously defined string `variable <#var>`_. The actual target
    file is obtained from the value of the variable.
    The initial value of the variable sets the initial file. Subsequently,
    when the value of the variable changes, the old output will be closed
    and the new one will be opened.

  Optional "``-c ColName [ColName ...]``" selects the columns to output.
  Normally, each selection is the name of a previously defined column/variable.
  In addition, these special forms are supported:

  * ``*`` - An asterisk adds all columns (except variables) to the output.
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

  If ``-o`` is given without a ``-c``, then ``*`` is assumed.
  If ``-c`` is given without a prior ``-o``, the selected columns will
  be output to stdout.

  Example:

   ::

    $ aq_pp ... -d s:Col1 s:Col2 s:Col3 ... -o - -c Col2 Col1

  * Output Col2 and Col1 (in that order) to stdout.

   ::

    $ aq_pp ... -d s:Col1 s:Col2 s:Col3 ... -c ^Col1:ColX ~Col3

  * First, select ``*`` (Col1, Col2 and Col3) implicitly.
    Then change Col1's label to ColX. Then exclude Col3. The final output
    columns are ColX and Col2.

   ::

    $ aq_pp ... -d s:Col1 s:Col2 s:Col3 ... -var i:Col4 0 -c '*' Col4

  * First, select ``*`` (Col1, Col2 and Col3) explicitly.
    Then add the variable Col4.

   ::

    $ aq_pp ... -var s:out1 '"first.csv"' ...
        -if -filt '...' -eval out1 '...' -endif ...  -o,fvar out1 ...

  * Define the output target as the value of variable ``out1``.
  * Change the variable's value conditionally via a
    `-if ... -endif <#conditional-processing-groups>`_ group.
    The conditional group and/or the `-eval`_ statement can be replaced by
    other means of changing ``out1`` as well.
  * Sometimes, the initial value of ``out1`` is not known until run time.
    If so, set its value to ``/dev/null`` in the ``-var`` statement.


.. _`-ovar`:

``-ovar[,AtrLst] File [-c ColName [ColName ...]]``
  Output the *final* values of all variables defined via the `-var`_ option.
  Multiple sets of "``-ovar ... -c ...``" can be specified.
  Only a single data row is output from each spec.

  "``-ovar[,AtrLst] File``" sets the output attributes and file.
  See the `aq_tool output specifications <aq-output.html>`_ manual for details.
  In addition, the following attribute is supported:

  * ``fvar`` - Output to a dynamically defined target. ``File`` is the name of
    a previously defined string `variable <#var>`_. The actual target
    file is obtained from the value of the variable.
    The initial value of the variable sets the initial file. Subsequently,
    when the value of the variable changes, the old output will be closed
    and the new one will be opened.

  Optional "``-c ColName [ColName ...]``" selects the variables to output.
  Normally, each selection is the name of a previously defined variable.
  In addition, these special forms are supported:

  * ``*`` - An asterisk adds all variables to the output.
  * ``ColName[:NewName][+NumPrintFormat]`` - Add ``ColName`` to the output.
    If ``:NewName`` is given, it will be used as the output label.
    The ``+NumPrintFormat`` spec is for numeric variables. It overrides the
    print format of the variable (*be careful with this format - a wrong spec
    can crash the program*).
  * ``^ColName[:NewName][+NumPrintFormat]`` - Same as the above, but with a
    leading ``^`` mark. It is used to *modify* the output label and/or format
    of a previously selected output variable called ``ColName``.
    If ``^ColName[...]`` is the first selection after ``-c``, then ``*`` will be
    included automatically first.
  * ``~ColName`` - The leading ``~`` mark is used to *exclude* a previously
    selected output variable called ``ColName``.
    If ``~ColName`` is the first selection after ``-c``, then ``*`` will be
    included automatically first.

  If ``-o`` is given without a ``-c``, then ``*`` is assumed.

  Example:

   ::

    $ aq_pp ... -d i:Col1 i:Col2 ... -var i:Sum1 0 -var i:Sum2 0 ...
        -eval Sum1 'Sum1 + Col1' -eval Sum2 'Sum2 + (Col2 * Col2)' ...
        -ovar - -c Sum1 Sum2

  * Calculate sums and output their values at the end of processing.


.. _`-imp`:

``-imp[,AtrLst] DbName[:TabName] [-server AdrSpec [AdrSpec ...]] [-local] [-mod ModSpec [ModSrc]]``
  Output data to Udb (i.e., perform an Udb import). (Examples for udb is available at `aq_udb <https://essentia-playground.auriq.com/notebooks/aq_udb.ipynb>`_).

  ``DbName`` is the database name (see `Target Udb Database`_).
  ``TabName`` is a table/vector name in the database.
  If ``TabName`` is not given or if it is a "." (a dot), a primary key-only
  import will be performed.
  Columns (including `variables <#var>`_) from the current data set matching
  the column names of ``TabName`` are automatically selected for import.
  In case certain desired columns in the current data set are named
  differently from tbe columns of ``TabName``, use `-alias`_ or `-renam`_
  to remap their names manually.

  Optional ``AtrLst`` is a comma separated list containing:

  * ``spec=UdbSpec`` - Set the spec file directly (see `Target Udb Database`_).
  * ``ddef`` - Allow missing target columns. Normally, it is an error when
    a target column is missing from the current data set. With this attribute,
    0 or blank will be used as the missing columns' value.
  * ``nodelay`` - Send records to Udb servers as soon as possible.
    Otherwise, up to 16KB of data may be buffered before an output occurs.
  * ``seg=N1[-N2]/N[:V]`` - Only import a subset of the input data by selecting
    segment N1 or segments N1 to N2 (inclusive) out of N segments of
    unique keys based on their hash values.
    For example, ``seg=2-4/10`` will divide the keys into 10 segments and
    import segments 2, 3 and 4; segments 1 and 5-10 are skipped.
    Optional ``V`` is a number that can be used to vary the sample selection.
    It is zero by default.
  * ``nobnk`` - Exclude records with a blank key from the import.
    This only applies with the primary key is made up of a single string column.
  * ``nonew`` - Tell the server not to create any new key during the
    import. In other words, records belonging to keys *not yet* in the DB are
    discarded.
  * ``noold`` - The opposite of ``nonew``.

  Optional "``-server AdrSpec [AdrSpec ...]``" sets the target servers.
  If given, server spec in the Udb spec file will be ignored.
  ``AdrSpec`` has the form ``IP_or_Domain[|IP_or_Domain_Alt][:Port]``.
  See `Target Udb Database`_ for details.

  Optional "``-local``" tells the program to connect to the *local* servers
  only. Local servers are those in the server spec (from the Udb spec file or
  ``-server`` option) whose IP matches the the local
  IP of the machine the program is running on.

  Optional "``-mod ModSpec [ModSrc]``" specifies a module to be
  loaded on the *server side*.
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

  Multiple sets of Udb import options can be specified.

  Example:

   ::

    $ aq_pp ... -d s:Col1 s:Col2 i:Col3 s:Col4 ... -imp mydb:Test

  * Import data set into Test.


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


RT MapFrom Syntax
=================

RT style MapFrom is used in both `-mapf`_ and `-map`_ options. The MapFrom
spec is used to match and/or extract data from a string column's value.
It has this general syntax:

* A literal - In other words, compare input data to a constant.
* A literal and wild cards -
  ``literal_1%*literal_2%?literal_3`` -
  ``%*`` matches any number of bytes and ``%?`` matches any 1 byte.
  This is like a pattern comparison.
* A variable -
  ``%%my_var%%`` -
  Extract the value into a variable named ``my_var``. ``my_var`` can later be
  used in the MapTo spec.
* Literals and variables -
  ``literal_1%%my_var_1%%literal_2%%my_var_2%%`` -
  A common way to extract specific data portions.
* Case sensitive or insensitive toggling -
  ``literal_1%=literal_2%=literal_3`` -
  ``%=`` is used to toggle case sensitive/insensitive match. In the above case,
  if `-mapf`_ or `-map`_ does not have the ``ncas`` attribute, then
  ``literal_1``'s match will be case sensitive, but ``literal_2``'s will be
  case insensitive, and ``literal_3``'s will be case sensitive again.
* '\\' escape -
  ``\%\%not_var\%\%%%my_var%%a_backslash\\others`` -
  If a '%' is used in such a way that resembles an unintended MapFrom spec,
  the '%' must be escaped. Literal '\\' must also be escaped.
  In summary, the following escape sequences are recognized:

  * ``\%`` - represents a literal percent character.
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

Each ``%%var%%`` variable can have additional attributes. The general form of
a variable spec is:

 ::

  %%VarName[:@class][:[chars]][:min[-max]][,brks]%%

where

* ``VarName`` is the variable name which can be used in MapTo. VarName can be a
  '*'; in this case, the extracted data is not stored, but the extraction
  attributes are still honored.
  Note: Do not use numbers as a RT mapping variable name.
* ``:@class`` restricts the exctracted data to belong to a class of characters.
  ``class`` is a code with these values and meanings:

  * ``n`` - Characters 0-9.
  * ``a`` - Characters a-z.
  * ``b`` - Characters A-Z.
  * ``c`` - All printable ASCII characters.
  * ``x`` - The opposite of ``c`` above.
  * ``s`` - All whitespaces.
  * ``g`` - Characters in ``{}[]()``.
  * ``q`` - Single/double/back quotes.

  Multiple classes can be used; e.g., ``%%my_var:@nab%%`` for all alphanumerics.
* ``:[chars]`` (``[]`` is part of the syntax) is similar to the character class
  described above except that the allowed characters are set explicitly.
  Note that ranges is not supported, all characters must be specified.
  For example,
  ``%%my_var:[0123456789abcdefABCDEF]%%`` (same as
  ``%%my_var:@n:[abcdefABCDEF]%%``) for hex digits. To include a ']'
  as one of the characters, put it first, as in ``%%my_var:[]xyz]%%``.
* ``:min[-max]`` is the min and optional max length (bytes, inclusive) to
  extract. Without a max, the default is unlimited (actually ~64Kb).
* ``,brks`` defines a list of characters at which extraction of the variable
  should stop. For example, ``%%my_var,,;:%%`` will extract data into ``my_var``
  until one of ``,;:`` or end-of-string is encountered. This usuage is often
  followed by a wild card, as in ``%%my_var,,;:%%%*``.


.. _`MapFromSyntax`:

RegEx MapFrom Syntax
====================

Regular expression style ``MapFrom`` can be used in both `-mapf`_ and `-map`_
options. ``MapFrom`` defines what to match and/or extract from a string
value of a column.
Both the POSIX and PCRE (Perl Compatible regular expression) engines are
supported. Which one to use depends on the mapping option's attributes.
See `regular expression attributes <aq-emod.html#regex-attributes>`_ for
the appropriate attributes.

Differences between RegEx mapping and RT mapping:

* RT pattern always matches the entire string, while RegEx pattern matches a
  substring by default. To get the same behavior, add '^' and '$' to the
  beginning and end of a RegEx as in ``^pattern$``.
* The POSIX RegEx MapFrom does not have named variables for the extracted data.
  Instead, extracted data is put into implicit variables ``%%0%%``, ``%%1%%``,
  and so on. See `-mapc`_ for an usage example. The PCRE engine can optionally
  use named variables.
* In addition to the standard regular expression escape sequences
  (``\\``, ``\+``, ``\*``, etc), the followings are also recognized:

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

Regular expression is very powerful but also complex. Please consult the
POSIX or PCRE2 regular expression manuals for details.

.. _MapToSyntax:

MapTo Syntax
============

MapTo is used in `-mapc`_ and `-map`_. It renders the data
extracted by MapFrom into a column. Both RT and RegEx MapTo share the same
syntax:

* A literal - In other words, the result will be a constant.
* A variable -
  ``%%my_var%%`` -
  Substitute the value of ``my_var``.
* Literals and variables -
  ``literal_1%%my_var_1%%literal_2%%my_var_2%%`` -
  A common way to render extracted data.
* '\\' escape -
  ``\%\%not_var\%\%%%my_var%%a_backslash\\others`` -
  If a '%' is used in such a way that resembles an unintended MapTo spec,
  the '%' must be escaped. Literal '\\' must also be escaped.
  See `RT MapFrom Syntax`_ for all supported escape sequences.

Each ``%%var%%`` variable can have additional attributes. The general form of
a variable spec is:

 ::

  %%VarName[:cnv][[:start]:length][,brks]%%

where

* ``VarName`` is the variable to substitute in.
* ``:cnv`` sets a conversion method on the data in the variable. Note that the
  data is first subjected to the length and break considerations before the
  conversion. Supported conversions are:

  * ``b64`` - Apply base64 decode.
  * ``url[Num]`` - Apply URL decode. Optional ``Num`` is a number between 1-99.
    It is the number of times to apply URL decode.

  Normally, only use 1 conversion. If both are specified (in any order), URL
  decode is always done before base64 decode.
* ``:length`` (without a start position spec) is the number of bytes from the
  beginning of the extracted data to substitute. Default is till the end.
* ``:start:length`` is the starting byte position and subsequent length of the
  extracted data to substitute. The first byte has position 0.
* ``,brks`` defines a list of characters at which substitution of the variable's
  value should stop.

See `-mapc`_ for an usage example.


Target Udb Database
===================

``aq_pp`` obtains information about the target Udb database from a spec file.
The spec file contains server IPs (or domain names) and table/vector
definitions. See `udb.spec <udb.spec.html>`_ for details.
``aq_pp`` finds the relevant spec file in several ways:

* The spec file path is taken from the ``spec=UdbSpec`` attribute
  of the `-imp`_ or `-exp`_ option.
* The spec file path is deduced implicitly from the ``DbName`` parameters
  of the `-imp`_ or `-exp`_ option. This method sets the spec file to
  "``.conf/DbName.spec``" in the runtime directory of ``aq_pp``.
* If none of the above information is given, the spec file is assumed to be
  "``udb.spec``" in the runtime directory of ``aq_pp``.


.. _`ConditionalProcessingGroups`:

Conditional Processing Groups
=============================

Some of the data processing options can be placed in conditional groups such
that different processing rules can be applied depending on the logical result
of another rule. The basic form of a conditional group is:

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

Groups can be nested to form more complex conditions.
Supported ``RuleToCheck`` and ``RuleToRun`` are
`-eval`_, `-mapf`_, `-mapc`_, `-kenc`_, `-kdec`_,
`-filt`_, `-map`_, `-sub`_, `-grep`_, `-cmb`_, `-pmod`_,
`-o`_ and `-imp`_. Note that some of these rules may be responsible for the
initialization of dynamically created columns. If such rules get skipped
conditionally, numeric 0 or blank string will be assigned to the
uninitialized columns.

There are 2 special ``RuleToCheck``:

* ``-true`` - Evaluate to true.
* ``-false`` - Evaluate to false.

In addition, there are 3 special ``RuleToRun`` for output record disposition
control (they do not change any data):

* ``-skip`` - Do not output current row.
* ``-quit`` - Stop processing entirely.
* ``-quitafter`` - Stop processing after the current input record.

Example:

 ::

  $ aq_pp ... -d i:Col1 ...
      -if -filt 'Col1 == 1'
        -eval s:Col2 '"Is-1"'
      -elif -filt 'Col1 == 2'
        -false
      -else
        -eval Col2 '"Others"'
      -endif
      ...

* Set Col2's value based on Col1's.
  In addition, discard any record with Col1==2.

 ::

  $ aq_pp ... -d i:Col1 s:Col2 ...
      -if -filt 'Col1 == 1'
        -o Out1
      -elif -filt 'Col1 == 2'
        -o Out2 -c Col2
      -endif
      ...

* Output rows where Col1 equals 1 to Out1. Out1 will have all the input columns.
  Output rows where Col1 equals 2 to Out2. Out2 will have Col2 only.
  Rows with Col1 having other values are not output.


See Also
========

* `aq-input <aq-input.html>`_ - aq_tool input specifications
* `aq-output <aq-output.html>`_ - aq_tool output specifications
* `aq-emod <aq-emod.html>`_ - aq_tool eval functions.
* `mcc.pmod <mcc.pmod.html>`_ - aq_pp module script compiler
* `udbd <udbd.html>`_ - Udb server
* `udb.spec <udb.spec.html>`_ - Udb spec file
* `aq_udb <aq_udb.html>`_ - Udb server interface
* `mcc.umod <mcc.umod.html>`_ - Udb module script compiler
* `Essentia Playground <https://essentia-playground.auriq.com/notebooks/README.ipynb>`_ - Interactive practice environment for ess commands and aq_tools

