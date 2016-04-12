.. |<br>| raw:: html

   <br>

=====
aq_pp
=====

Record preprocessor


Synopsis
========

::

  aq_pp [-h] Global_Opt Input_Spec Prep_Spec Process_Spec Output_Spec

  Global_Opt:
      [-test] [-verb] [-stat] [-bz ReadBufSiz]

  Input_Spec:
      [-f[,AtrLst] File [File ...]] [-d ColSpec [ColSpec ...]]
      [-cat[,AtrLst] File [File ...] ColSpec [ColSpec ...]]

  Prep_Spec:
      [-ddef]
      [-seed RandSeed]
      [-rownum StartNum]
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
      [-sub[,AtrLst] ColName File [File ...] [ColTag ...]]
      [-grep[,AtrLst] ColName File [File ...] [ColTag ...]]
      [-cmb[,AtrLst] File [File ...] ColSpec [ColSpec ...]]
      [-pmod ModSpec [ModSrc]]

  Output_Spec:
      [-o[,AtrLst] File] [-c ColName [ColName ...]]
      [-udb [-spec UdbSpec | -db DbName] -imp [DbName:]TabName
        [-seg N1[-N2]/N] [-nobnk] [-nonew] [-mod ModSpec [ModSrc]]
      ]
      [-ovar[,AtrLst] File [-c ColName [ColName ...]]]


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


.. _`-bz`:

``-bz ReadBufSiz``
  Set input buffer length.
  It is also the maxium record length. If a record exceeds this length, it is
  considered broken and will cause the program to abort or the record to be
  discarded.
  Default length is 64KB. Use this option if a longer record is expected.
  ``ReadBufSiz`` is a number in bytes.


.. _`-f`:

``-f[,AtrLst] File [File ...]``
  Set the input attributes and files.
  If the data come from stdin, set ``File`` to '-' (a single dash).
  Optional ``AtrLst`` is described under `Input File Attributes`_.
  If this option is not given, stdin is assumed.

  Example:

   ::

    $ aq_pp ... -f,+1l,eok file1 -f file2 ...

  * File1 and file2 can have different attributes.


.. _`-d`:

``-d ColSpec [ColSpec ...]`` or |<br>| ``-d [SepSpec] ColSpec [[SepSpec] ColSpec ...]``
  Define the columns in the input records from all the `-f`_ specs.
  Up to 2048 ``ColSpec`` can be defined (excluding ``X`` type columns).
  ``ColSpec`` has the form ``Type[,AtrLst]:ColName``.
  Supported ``Types`` are:

  * ``S`` - String.
  * ``F`` - Double precision floating point.
  * ``L`` - 64-bit unsigned integer.
  * ``LS`` - 64-bit signed integer.
  * ``I`` - 32-bit unsigned integer.
  * ``IS`` - 32-bit signed integer.
  * ``IP`` - v4/v6 address.
  * ``X[Type]`` - marks an unwanted input column.
    Type is optional. It can be one of the above (default is ``S``).
    ColName is also optional. Such a name is simply discarded.

  Optional ``AtrLst`` is used in conjunction with the `input file attributes`_
  to determine how column data are to be extracted from the input.
  It is a comma separated list containing:

  * ``n=Len`` - Extract exactly ``Len`` source bytes. Use this for a fixed
    length data column.
  * ``esc`` - Denote that the input field uses '\\' as escape character. Data
    exported from databases (e.g. MySQL) sometimes use this format. Be careful
    when dealing with multibyte character set because '\\' can be part of a
    multibyte sequence.
  * ``clf`` - Denote that the input field uses these encoding methods:

    * Non-printable bytes encoded as '\\xHH' where ``HH`` is the hex value of
      the byte.
    * '"' and '\\' encoded as '\\"' and '\\\\'.
    * Selected whitespaces encoded as '\\r', '\\n', '\\t', '\\v' and '\\f'.

  * ``noq`` - Denote that the input field is not quoted. Any quotes in or around
    the field are considered part of the field value.
  * ``hex`` - For numeric type. Denote that the input field is in hexdecimal
    notation. Starting ``0x`` is optional. For example, ``100`` is
    converted to 256 instead of 100.
  * ``trm`` - Trim leading/trailing spaces from input field value.
  * ``lo``, ``up`` - For ``S`` type. Convert input field to lower/upper case.

  ``ColName`` is case insensitive. It can have up to 31 alphanumeric and '_'
  characters. The first character must not be a digit.

  The alternate column definition involving ``SepSpec`` is designed for
  input data that have multibyte separators and/or varying separators from
  field to field. In these cases, *all* the separators must be individually
  specified. ``SepSpec`` has the form ``SEP:SepStr`` where ``SEP``
  (case insensitive) is a keyword and ``SepStr`` is a literal separator of one
  or more bytes. A ``SepSpec`` is generally needed between two adjacent
  ``ColSpec`` unless the former column has a length spec.

  Example:

   ::

    $ aq_pp ... -d s:Col1 s,lo:Col2 i,trm:Col3 ...

  * Col1 is a string. Col2 is also a string, but the input value will be
    converted to lower case. Col3 is an unsigned integer, the ``trm``
    attribute removes blanks around the value before it is converted to
    an internal number.

   ::

    $ aq_pp ... -d sep:' [' s:time_s sep:'] "' s,clf:url sep:'"' ...

  * This parses data of the form: [01/Apr/2016:01:02:03 +0900] "/index.html".


.. _`-cat`:

``-cat[,AtrLst] File [File ...] ColSpec [ColSpec ...]``
  Add rows from ``Files`` to the current data set.
  If the data come from stdin, set ``File`` to '-' (a single dash).
  Optional ``AtrLst`` is described under `Input File Attributes`_.
  ``ColSpecs`` define the columns in the files as with `-d`_.
  The columns may differ from those of the current data set.
  The new data set will contain unique columns from both sets.
  Columns that do not exist in a data set will be set to zero or blank when
  that data set is loaded.

  Example:

   ::

    $ aq_pp ... -d s:Col1 s:Col2 i:Col3 s:Col4 ...
        -cat more.csv i:Col3 s:Col1 s:Col5 s:Col6
        ...

  * Add data from more.csv. Column Col3 and Col1 are common. The original data
    set does not have Col5 and Col6, so they are set to blank in rows from the
    original inputs. On the other hand, more.csv does not have Col2 and Col4,
    so they are set to blank in rows from more.csv. The resulting data set will
    have columns Col1, Col2, Col3, Col4, Col5 and Col6.


.. _`-ddef`:

``-ddef``
  Turns on implicit column support for Udb import. If a column
  required by the target Udb table is not defined in the data set,
  its value will be set to 0 or blank during import.

  * Instead of (or in addition to) this option, `-var`_ and/or `-eval`_
    can be used to add the required columns to the data set.
  * The "PKEY" column cannot be implicit.
  * This option applies to all Udb imports.


.. _`-seed`:

``-seed RandSeed``
  Set the random sequence seed of the ``$Random`` evaluation builtin variable.
  Default seed is 1.


.. _`-rownum`:

``-rownum StartNum``
  Set the starting value for the ``$RowNum`` evaluation builtin variable.
  ``StartNum`` is the index of the first row.
  Default starting row index is 1.


.. _`-var`:

``-var ColSpec Val``
  Define a new variable and initialize its value to Val.
  A variable stores a value that persists between rows over the entire run.
  Recall that normal column values change from row to row.
  ``ColSpec`` is the variable's spec in the form ``Type:ColName`` where Type
  is the data type and ColName is the variable's name. See the `-d`_ for
  details.
  Note that a string ``Val`` must be quoted,
  see `String Constant`_ spec for details.

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
  * Operator precedency is *NOT* supported. Use '(' and ')' to group
    operations as appropriate.

  Builtin variables:

  ``$Random``
    A random number (postive integer).
    Its value changes every time the variable is referenced.
    The seed of this random sequence
    can be set using the `-seed`_ option.

  ``$RowNum``
    The input row index.
    First row is 1 by default.
    Its initial value can be set using the `-rownum`_ option.

  Standard functions:

    See `aq-emod <aq-emod.html>`_ for a list of supported functions.

  Example:

   ::

    $ aq_pp ... -d i:Col1 ... -eval l:Col_evl 'Col1 * 10' ...

  * Set new column Col_evl to 10 times the value of Col1.

   ::

    $ aq_pp -rownum 101 ... -d i:Col1 ... -eval i:Seq '$RowNum' ...

  * Set starting row index to 101 and set new column Seq to the row index.

   ::

    $ aq_pp ... -d s:Col1 s:Col2 ...
        -eval is:Dt 'DateToTime(Col2, "Y.m.d.H.M.S.p") - DateToTime(Col1, "Y.m.d.H.M.S.p")'
        ...

  * Col1 and Col2 are date strings of the form "Year/Month/day Hour:Min:Sec AM".
    Dt will contain the time difference in seconds.


.. _`-mapf`:

``-mapf[,AtrLst] ColName MapFrom``
  Extract data from a string column. This option should be used in
  conjunction with `-mapc`_.
  ``ColName`` is a previously defined column/variable to extract data from.
  ``MapFrom`` defines the extraction rule.
  Optional ``AtrLst`` is a comma separated list containing:

  * ``ncas`` - Do case insensitive pattern match (default is case sensitive).
  * ``rx`` - Do Regular Expression matching.
  * ``rx_extended`` - Do Regular Expression matching.
    In addition, enable POSIX Extended Regular Expression syntax.
  * ``rx_newline`` - Do Regular Expression matching.
    In addition, apply certain newline matching restrictions.

  If any of the Regular Expression related attributes are enabled, then
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

  * ``ncas`` - Do case insensitive pattern match (default is case sensitive).
  * ``rx`` - Do Regular Expression matching.
  * ``rx_extended`` - Do Regular Expression matching.
    In addition, enable POSIX Extended Regular Expression syntax.
  * ``rx_newline`` - Do Regular Expression matching.
    In addition, apply certain newline matching restrictions.

  If any of the Regular Expression related attributes are enabled, then
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

``-sub[,AtrLst] ColName File [File ...] [ColTag ...]``
  Update the value of a string column/variable according to a lookup table.
  ``ColName`` is a previously defined column/variable.
  ``Files`` contain the lookup table.
  If the input comes from stdin, set ``File`` to '-' (a single dash).
  Optional ``AtrLst`` is a comma separated list containing:

  * Standard `Input File Attributes`_.
  * ``ncas`` - Do case insensitive match (default is case sensitive).
  * ``pat`` - Support '?' and '*' wild cards in the "From" value. Literal '?',
    '*' and '\\' must be escaped by a '\\'. Without this attribute,
    "From" value is assumed constant and no escape is necessary.
  * ``req`` - Discard records not matching any entry in the lookup table.
    Normally, column value will remain unchanged if there is no match.
  * ``all`` - Use all matches. Normally, only the first match is used.
    With this attribute, one row is produced for each match.

  ``ColTags`` are optional. They specify the columns in the files. Supported
  tags (case insensitive) are:

  * ``FROM`` - marks the column used to match the value of ColName.
  * ``TO`` - marks the column used as the new value of ColName.
  * ``X`` - marks an unused column.

  If ``ColTag`` is used, both the ``FROM`` and ``TO`` tags must be given.
  Any number of ``X`` can be specified.
  If ``ColTag`` is not used, the files are assumed to contain
  *exactly 2 columns* - the ``FROM`` and ``TO`` columns, in that order.

  The ``FROM`` value is generally a literal. Patterns can also be used,
  see the ``pat`` attribute description above.
  The ``TO`` value is always a literal.
  Matches are carried out according to the order of the match value in the
  files. Match stops when the first match is found. If the files contain both
  exact value and pattern, then:

  * Exact values are matched first, skipping over any interleaving patterns.
  * Patterns are matched next, skipping over any interleaving fixed values.

  **Note**: If a file name happens to be one of ``FROM``, ``TO`` or ``X``
  (case insensitive), prepend the name with a path (e.g., "./X")
  to avoid misinterpretation.

  Example:

   ::

    $ aq_pp ... -d s:Col1 ... -sub Col1 lookup.csv ...

  * Substitute Col1 according to lookup table.


.. _`-grep`:

``-grep[,AtrLst] ColName File [File ...] [ColTag ...]``
  Like filtering, but matches a single column/variable against a list of
  values from a lookup table.
  ``ColName`` is a previously defined column/variable.
  ``Files`` contain the lookup table.
  If the input comes from stdin, set ``File`` to '-' (a single dash).
  Optional ``AtrLst`` is a comma separated list containing:

  * Standard `Input File Attributes`_.
  * ``ncas`` - Do case insensitive match (default is case sensitive).
  * ``pat`` - Support '?' and '*' wild cards in the "From" value. Literal '?',
    '*' and '\\' must be escaped by a '\\'. Without this attribute,
    match value is assumed constant and no escape is necessary.
  * rev - Reverse logic, select records that do not match.

  ``ColTags`` are optional. They specify the columns in the files. Supported
  tags (case insensitive) are:

  * ``FROM`` - marks the column used to match the value of ColName.
  * ``X`` - marks an unwanted column.

  If ``ColTag`` is used, the ``FROM`` tag must be given.
  Any number of ``X`` can be specified.
  If ``ColTag`` is not used, the files are assumed to contain
  *exactly 1 column* - the ``FROM`` column.

  The ``FROM`` value is generally a literal. Patterns can also be used,
  see the ``pat`` attribute description above.
  Matches are carried out according to the order of the match value in the
  files. Match stops when the first match is found. If the files contain both
  exact value and pattern, then:

  * Exact values are matched first, skipping over any interleaving patterns.
  * Patterns are matched next, skipping over any interleaving fixed values.

  **Note**: If a file name happens to be one of ``FROM`` or ``X``
  (case insensitive), prepend the name with a path (e.g., "./X")
  to avoid misinterpretation.

  Example:

   ::

    $ aq_pp ... -d s:Col1 ... -grep,rev Col1 lookup.csv ...

  * Select (or retain) only records whose Col1 values are not in lookup table.


.. _`-cmb`:

``-cmb[,AtrLst] File [File ...] ColSpec [ColSpec ...]``
  Combine data from lookup table into the current data set by joining rows
  from both data sets based on common key column values.
  The new data set will contain unique columns from both sets.
  ``Files`` contain the lookup table.
  If the data come from stdin, set ``File`` to '-' (a single dash).
  Optional ``AtrLst`` is a comma separated list containing:

  * Standard `Input File Attributes`_.
  * ``ncas`` - Do case insensitive match (default is case sensitive).
  * ``req`` - Discard unmatched records.
  * ``all`` - Use all matches. Normally, only the first match is used.
    With this attribute, one row is produced for each match.

  ``ColSpecs`` define the columns in the files as with `-d`_.
  In addition to the standard `-d`_ column attributes,
  the followings are supported:

  * ``key`` - Mark a key column. This column must exist in the current
    data set.
  * ``cmb`` - Mark a column to be combined into the current data set. If this
    column does not exist, one will be added.

  If a column has neither the ``key`` nor ``cmb`` attribute, it will be
  implicitly used as a combine key if a column with the same name already
  existed in the current data set.

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
  Output data rows.
  Optional "``-o[,AtrLst] File``" sets the output attributes and file.
  If ``File`` is a '-' (a single dash), data will be written to stdout.
  Optional ``AtrLst`` is described under `Output File Attributes`_.

  Optional "``-c ColName [ColName ...]``" selects the columns to output.
  ``ColName`` refers to a previously defined column/variable.
  Without ``-c``, all columns are selected by default. Variables are not
  automatically included though.
  If ``-c`` is specified without a previous ``-o``, output to stdout is
  assumed.

  In case a title line is desired but certain column names are not
  appropriate, use `-alias`_ or `-renam`_ before the ``-o`` to remap the
  name of those columns manually.
  With `-alias`_, the alternate names must be explicitly selected with ``-c``.
  With `-renam`_, ``-c`` is optional.

  Multiple sets of "``-o ... -c ...``" can be specified.

  Example:

   ::

    $ aq_pp ... -d s:Col1 s:Col2 s:Col3 ... -o,esc,noq - -c Col2 Col1

  * Output Col2 and Col1 (in that order) to stdout in a format suitable for
    Amazon Cloud.


.. _`-udb`:

``-udb [-spec UdbSpec|-db DbName] -imp [DbName:]TabName [-seg N1[-N2]/N] [-nobnk] [-nonew] [-mod ModSpec [ModSrc]]``
  Output data directly to Udb (i.e., a Udb import).
  ``-udb`` marks the beginning of Udb import specific options.
  Optional "``-spec UdbSpec``" sets the Udb spec file for the import.
  Alternatively, "``-db DbName``" indirectly sets the spec file to
  ".conf/``DbName``.spec" in the current work directory.
  If neither option is given, "udb.spec" in the current work directory
  is assumed.
  See the "udb.spec" manual page for details.

  "``-imp [DbName:]TabName``" specifies an import operation.

  * ``TabName`` set the table in the spec to import data to.
  * ``TabName`` is case insensitive. It must not exceed 31 bytes long.
  * Optional ``DbName`` defines ``UdbSpec`` indirectly as in the ``-db`` option.
  * Columns from the current data set, including variables, matching the
    columns of ``TabName`` are automatically selected for import.
    In case certain columns in the current data set are named
    differently from tbe columns of ``TabName``, use `-alias`_ or `-renam`_
    to remap those columns manually.
  * See `-ddef`_ if any column in the target table is missing from the
    current data set.

  Optional "``-seg N1[-N2]/N``" applies sampling by selecting segment N1 or
  segment N1 to N2 (inclusive) out of N segments of unique users from the
  input data to import. Users are segmented based on the hash value of the
  user key. For example, "``-seg 2-4/10``" will divide user pool into 10
  segments and import segments 2, 3 and 4; segments 1 and 5-10 are discarded.

  Optional ``-nobnk`` excludes records with a blank user key from the import.

  Optional ``-nonew`` tells the server not to create any new user during this
  import. Records belonging to users not yet in the DB are discarded.

  Optional "``-mod ModSpec [ModSrc]``" specifies a module to be
  loaded on the *server side*.
  ``ModSpec`` has the form ``ModName`` or ``ModName("Arg1", "Arg2", ...)``
  where ``ModName`` is the module name and ``Arg*`` are module dependent
  arguments. Note that the arguments must be string constants;
  for this reason, they must be quoted according to the
  `string constant`_ spec.

  ``ModSrc`` is an optional module source file. It can be:

  * A module script source file that can be used to build the specified
    module. See the `Udb module script compiler <mcc.umod.html>`_
    documentation for more information.
  * A ready-to-use module object file. It *must* have a ``.so`` extension.

  Without ``ModSrc``, the server will look for a preinstalled module matching
  ``ModName``.

  Multiple sets of "``-udb -spec ... -imp ...``" can be specified.


.. _`-ovar`:

``-ovar[,AtrLst] File [-c ColName [ColName ...]]``
  Output the final variable values.
  Variables are those defined using the `-var`_ option.
  Only a single data row is output.

  "``-ovar[,AtrLst] File``" sets the output attributes and file.
  If ``File``` is a '-' (a single dash), data will be written to stdout.
  Optional ``AtrLst`` is described under `Output File Attributes`_.

  Optional "``-c ColName [ColName ...]``" selects the variables to output.
  ``ColName`` refers to a previously defined variable.
  Without ``-c``, all variables are selected by default.

  In case a title line is desired but certain variable names are not
  appropriate, use `-alias`_ or `-renam`_ before ``-ovar`` to remap the
  name of those variables manually.
  With `-alias`_, the alternate names must be explicitly selected with ``-c``.
  With `-renam`_, ``-c`` is optional.

  Multiple sets of "``-ovar ... -c ...``" can be specified.

  Example:

   ::

    $ aq_pp ... -d i:Col1 i:Col2 ... -var i:Sum1 0 -var i:Sum2 0 ...
        -eval Sum1 'Sum1 + Col1' -eval Sum2 'Sum2 + (Col2 * Col2)' ...
        -ovar - -c Sum1 Sum2

  * Calculate sums and output their evaluates at the end of processing.


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


Input File Attributes
=====================

Each input option can have a list of comma separated attributes that control
input processing.

Positioning the start of input:

* ``+Num[b|r|l]`` - Specifies the number of bytes (``b`` suffix), records (``r``
  suffix) or lines (``l`` suffix) to skip before processing.
  Line is the default.

Error handling:

* ``eok`` - Make input error non-fatal. If there is an input parse error,
  program will try to skip over bad/broken record. If there is an input data
  processing error, program will just discard the record.
* ``qui`` - Quiet; i.e., do not print any input error message.

Input formats  - these attributes are mutually exclusive except for
``sep=c`` and ``csv`` that can be used together:

* ``sep=c`` or ``sep=\xHH`` - Input is in 'c' (single byte) separated value
  format. '\\xHH' is a way to specify 'c' via its HEX value ``HH``.
* ``csv`` - Input is in CSV format. This is the only format that supports
  quoted data fields. Although CSV implies *comma separated*,
  ``sep=c`` can be used to override this.
* ``fix`` - Input columns are all fixed width *without* any separator.
  Individual column widths are set in the ``n=Len``
  `column spec attribute <-d_>`_.
* ``tab`` - Input is in HTML table format. Columns must be enclosed in
  "``<td>data</td>``" or "``<td ...>data</td>``" and rows must be terminated
  by a "``</tr>``".
* ``bin`` - Input is in aq_tool's internal binary format.

These are used in conjunction with the `column spec attributes <-d_>`_:

* ``esc`` - '\\' is an escape character in input fields.
* ``noq`` - No quotes around fields in ``csv`` format.

If no input format attribute is given, ``csv`` is assumed.


Output File Attributes
======================

Each output option can have a list of comma separated attributes:

* ``notitle`` - Suppress the column name label row from the output.
  A label row is normally included by default.
* ``app`` - When outputting to a file, append to it instead of overwriting.
* ``sep=c`` or ``sep=\xHH`` - Output in 'c' (single byte) separated value
  format. '\\xHH' is a way to specify 'c' via its HEX value ``HH``.
* ``csv`` - Output in CSV format. Strings will be quoted. The default
  separator is comma, but ``sep=c`` can be used to override this.
* ``bin`` - Output in aq_tool's internal binary format.
* ``esc`` - Use '\\' to escape the field separator, '"' and '\\' (non binary).
* ``noq`` - Do not quote string fields in ``csv`` format.
* ``fmt_g`` - Use "%g" as print format for ``F`` type columns. Only use this
  to aid data inspection (e.g., during integrity check or debugging).

If no output format attribute is given, ``csv`` is assumed.


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


RegEx MapFrom Syntax
====================

Regular expression style ``MapFrom`` can be used in both `-mapf`_ and `-map`_
options. ``MapFrom`` defines what to match and/or extract from a string
value of a column.

Differences between RegEx mapping and RT mapping:

* RT pattern always matches the entire string, while RegEx pattern matches a
  substring by default. To get the same behavior, add '^' and '$' to the
  beginning and end of a RegEx as in ``^pattern$``.
* RegEx MapFrom does not have named variables for the extracted data. Instead,
  extracted data is put into implicit variables ``%%0%%``, ``%%1%%``, and so on.
  See `-mapc`_ for an usage example.
* In addition to the standard regular expression escape sequences
  (``\\``, ``\+``, ``\*``, etc), the following are also recognized:

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

Regular Expression is very powerful but also complex. Please consult the
GNU RegEx manual for details.


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

  %%VarName[:cnv][:start[:length]][,brks]%%

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
* ``:start`` is the starting byte position of the extracted data to substitute.
  The first byte has position 0. Default is 0.
* ``:length`` is the number of bytes (from ``start``) to substitute. Default is
  till the end.
* ``,brks`` defines a list of characters at which substitution of the variable's
  value should stop.

See `-mapc`_ for an usage example.


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
`-o`_ and `-udb`_. Note that some of these rules may be responsible for the
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

* `aq-emod <aq-emod.html>`_ - aq_tool eval functions.
* `mcc.pmod <mcc.pmod.html>`_ - aq_pp module script compiler
* `udbd <udbd.html>`_ - Udb server
* `udb.spec <udb.spec.html>`_ - Udb spec file
* `aq_udb <aq_udb.html>`_ - Udb server interface
* `mcc.umod <mcc.umod.html>`_ - Udb module script compiler
* `Example aq_pp Commands <../../usecases/syntaxexamples/aq_pp-option-examples.html>`_ - Additional examples of aq_pp options.

