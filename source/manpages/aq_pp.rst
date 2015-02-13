=====
aq_pp
=====

-------------------
Record preprocessor
-------------------

:Copyright: AuriQ Systems Inc.
:Manual group: Data Processing Command
:Manual section: 1
:Date: 2015-01-28
:Version: 1.2.1


Synopsis
========

::

  aq_pp [-h] Global_Opt Input_Spec Process_Spec/Output_Spec Final_Output

  Global_Opt:
      [-test] [-verb] [-stat] [-tag TagLab] [-bz ReadBufSiz]
      [-ddef]
      [-rx_syntax Syntax]
      [-seed RandSeed]
      [-rownum StartNum]
      [-emod ModSpec]

  Input_Spec:
      [-fileid FileId] [-f[,AtrLst] File [File ...]] [-d ColSpec [ColSpec ...]]
      [-fileid FileId] [-cat[,AtrLst] File [File ...] ColSpec [ColSpec ...]]
      [-var ColSpec Val]

  Process_Spec/Output_Spec:
      [-evlc ColSpec|ColName Expr]
      [-mapf[rx][,AtrLst] ColName MapFrom] [-mapc ColSpec|ColName MapTo]
      [-kenc ColSpec|ColName ColName [ColName ...]]
      [-kdec ColName ColSpec|ColName[+] [ColSpec|ColName[+] ...]]
      [-filt FilterSpec]
      [-map[rx][,AtrLst] ColName MapFrom MapTo]
      [-sub[,AtrLst] ColName File [File ...] [ColTag ...]]
      [-grep[,AtrLst] ColName File [File ...] [ColTag ...]]
      [-cmb[,AtrLst] File [File ...] ColSpec [ColSpec ...]]
      [-pmod ModSpec]
      [[-o[,AtrLst] File] [-c ColName [ColName ...]] [-notitle]]
      [-udb [-spec UdbSpec | -db DbName] -imp [DbName:]TabName
        [-seg N1[-N2]/N] [-nobnk] [-nonew] [-mod ModSpec]]

  Final_Output:
      [-ovar[,AtrLst] File [-c ColName [ColName ...]] [-notitle]]


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
  column values. An example is `-evlc`_ which sets a column's value
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
  perform a `-evlc`. Even outputs can be controlled this way.
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

    aq_pp:TagLab rec=Count err=Count out=Count


.. _`-tag`:

``-tag TagLab``
  Set label used to tag output messages. Default is blank.
  Currently, it is only used in:

  * The `-stat`_ summary line.
  * Final error message before program aborts.


.. _`-bz`:

``-bz ReadBufSiz``
  Set input buffer length.
  It is also the maxium record length. If a record exceeds this length, it is
  considered broken and will cause the program to abort or the record to be
  discarded.
  Default length is 64KB. Use this option if a longer record is expected.
  ``ReadBufSiz`` is a number in bytes.


.. _`-ddef`:

``-ddef``
  Turns on implicit column support for Udb import. If a column
  required by the target Udb table is not defined in the data set,
  its value will be set to 0 or blank during import.

  * Instead of (or in addition to) this option, `-var`_ and/or `-evlc`_
    can be used to add the required columns to the data set.
  * The "PKEY" column in a Udb table cannot be implicit.
  * This option applies to all Udb imports.


.. _`-rx_syntax`:

``-rx_syntax Syntax``
  Set the syntax used for any subsequent RegEx. RegEx can be used in various
  "mapping" and filtering operations.
  Syntax is one of these values:

  * ``none`` - No particular syntax (default).
  * ``extended`` - Uses POSIX Extended Regular Expression syntax.
  * ``newline`` - Apply certain newline matching restrictions.

  Generally, set this option once before any RegEx is used. It is also possible
  to change syntax within the processing chain; new syntax will affect
  operations specified afterwards.

  Example:

   ::

    sh# aq_pp ...Operation_0...
          -rx_syntax extended ...Operation_1...
          -rx_syntax none ...Operation_2...

  * Operation_0 will not use any particular syntax.
    Operation_1 will use "grep" syntax.
    Operation_2 will again use no particular syntax.


.. _`-seed`:

``-seed RandSeed``
  Set the seed of random sequence used by the ``$Random``
  ``evlc`` builtin variable.


.. _`-rownum`:

``-rownum StartNum``
  Set the starting value for the ``$RowNum`` ``evlc `` builtin variable.
  ``StartNum`` is the index of the first row.
  Default starting row index is 1.
  See `-evlc`_ for an usage example.


.. _`-emod`:

``-emod ModSpec``
  Load a module that supplies custom evaluation functions.
  The supplied functions will be available for use in subsequent `-evlc`_
  specs.

  ``ModSpec`` has the form ``ModName[:argument]`` where ``ModName``
  is the logical module name and ``argument`` is an optional module specific
  parameter string.
  aq_pp will look for "emod/``ModName``.so" in the directory where aq_pp is
  installed. For example, if aq_pp is installed as ``SomeDirectory/aq_pp``,
  aq_pp will load ``SomeDirectory/emod/ModName.so``.
  Multiple eval modules can be specified.
  In case a function of the same name is supplied by multiple
  modules, the one from the most recently loaded module will be used.
  Each emod is individually documented. See the "aq_pp-emod-\*" manual pages
  for details.


.. _`-fileid`:

``-fileid FileId``
  Set the file ID number for any inputs from `-f`_ and `-cat`_
  specified after this option.
  This ID is a constant until another `-fileid`_ where a different ID can be
  set for any further inputs from `-f`_ and `-cat`_.
  This ID can be retrieved during processing via the ``$FileId``
  `-evlc`_ builtin variable. The value retrieved depends on
  the file ID of the input file where the active record comes from.
  Default file ID is 1.
  See `-evlc`_ for an usage example.


.. _`-f`:

``-f[,AtrLst] File [File ...]``
  Set the input attributes and files.
  If the data come from stdin, set ``File`` to '-' (a single dash).
  Optional ``AtrLst`` is described under `Input File Attributes`_.
  If this option is not given, stdin is assumed.

  Example:

   ::

    sh# aq_pp ... -f,+1l,eok file1 -f file2 ...

  * File1 and file2 can have different attributes.


.. _`-d`:

``-d ColSpec [ColSpec ...]``
  Define the columns of the input records from all `-f`_ specs.
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

  Up to 256 ``ColSpec`` can be defined (excluding ``X`` type columns).
  Optional ``AtrLst`` is a comma separated list containing:

  * ``esc`` - Denote that the input field uses '\\' as escape character. Data
    exported from databases (e.g. MySQL) sometimes use this format. Be careful
    when dealing with multibyte character set because '\\' can be part of a
    multibyte sequence.
  * ``noq`` - Denote that the input field is not quoted. Any quotes in or around
    the field are considered part of the field value.
  * ``hex`` - For numeric type. Denote that the input field is in hexdecimal
    notation. Starting ``0x`` is optional. For example, ``100`` is
    converted to 256 instead of 100.
  * ``trm`` - Trim leading/trailing spaces from input field value.
  * ``lo``, ``up`` - For ``S`` type. Convert input field to lower/upper case.

  ``ColName`` restrictions:

  * Cannot exceed 31 bytes long.
  * Contain only alphanumeric and '_' characters. The first character
    cannot be a digit.
  * It is case insensitive. However, this spec may change in the future.

  **Note**: Optional ``ColSpec`` attributes only apply to input data.
  They cannot be used on the dynamically created columns discussed later.

  Example:

   ::

    sh# aq_pp ... -d s:Col1 s,lo:Col2 i,trm:Col3 ...

  * Col1 is a string. Col2 also a string, but the input value will be converted
    to lower case. Col3 is an unsigned integer, the ``trm`` attribute removes
    blanks around the value before it is converted to an internal number.


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

    sh# aq_pp ... -d s:Col1 s:Col2 i:Col3 s:Col4 ...
          -cat more.csv i:Col3 s:Col1 s:Col5 s:Col6
          ...

  * Add data from more.csv. Column Col3 and Col1 are common. The original data
    set does not have Col5 and Col6, so they are set to blank in rows from the
    original inputs. On the other hand, more.csv does not have Col2 and Col4,
    so they are set to blank in rows from more.csv. The resulting data set will
    have columns Col1, Col2, Col3, Col4, Col5 and Col6.


.. _`-var`:

``-var ColSpec Val``
  Define a new variable and initialize its value to Val.
  A variable stores a value that persists between rows over the entire run.
  Recall that normal column values change from row to row.
  ``ColSpec`` is the variable's spec in the form ``Type:ColName`` where Type
  is the data type and ColName is the variable's name. See the `-d`_ for
  details.
  ``Val`` is the literal value to initialize the variable to
  (``Val`` is not an expression, there is no need to enclose
  a string value in double quotes).

  Example:

   ::

    sh# aq_pp ... -d i:Col1 ...
          -var 'i:Sum' 0 ...
          -evlc 'Sum' 'Sum + Col1' ...

  * Initialize variable Sum to 0, then update the rolling sum for each row.


.. _`-evlc`:

``-evlc ColSpec|ColName Expr``
  Evaluate ``Expr`` and save the result to a column. The column can be a new
  column or an existing column/variable.

  * If ``ColSpec`` is given, a new column will be created using the spec.
    See `-d`_ for details. Note that the new column cannot participate in
    ``Expr``.
  * If a ColName is given, it must refer to a previously defined
    column/variable.

  ``Expr`` is the expression to evaluate.
  Data type of the evaluated result must be compatible with the data type of
  the target column. For example, string result for a string column and
  numeric result for a numeric column.
  Operands in the expression can be the names of previously defined columns or
  variables, numeric/string constants, builtin variables and functions.

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

  ``$FileId``
    The file ID assigned to the input file currently being processed
    Its value can be set using the `-fileid`_ option.

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

  ``DateToTime(DateVal, DateFmt)``
    Returns the UNIX time in integral seconds corresponding to ``DateVal``.
    ``DateVal`` can be a string column's name, a literal string,
    or an expression that evaluates to a string.
    ``DateFmt`` is a literal string (quoted with double quotes) specifying
    the format of ``DateVal``.
    The format is a sequence of single-letter conversion codes:

    * (a dot) ``.`` - represent a single unwanted character (e.g., a separator).
    * ``Y`` - 1-4 digit year.
    * ``y`` - 1-2 digit year.
    * ``m`` - month in 1-12.
    * ``b`` - abbreviated English month name ("JAN" ... "DEC", case
      insensitive).
    * ``d`` - day of month in 1-31.
    * ``H`` - hour in 0-23 or 1-12.
    * ``M`` - minute in 0-59.
    * ``S`` - second in 0-59.
    * ``p`` - AM/PM (case insensitive).
    * ``z`` - timezone as HHMM offset from GMT.

    This conversion is timezone dependent. If there is no timezone information
    (``z`` conversion) in the ``DateVal``, set the timezone appropriately
    (TZ environment) when running the program.

  ``TimeToDate(TimeVal, DateFmt)``
    Returns the date string corresponding to ``TimeVal``.
    The string's maximum length is 127.
    ``TimeVal`` can be a numeric column's name, a literal number,
    or an expression that evaluates to a number.
    ``DateFmt`` is a literal string (quoted with double quotes) specifying
    the format of the output. See the ``strftime()`` C function manual
    page regarding the format of ``DateFmt``.

    This conversion is timezone dependent. Set the timezone appropriately
    (TZ environment) when running the program.

  ``QryParmExt(QryVal, ParmSpec)``
    Extract query parameters from ``QryVal`` and place the results in columns.
    Returns the number of parameters extracted.
    Note that this function does not generate any error.
    ``QryVal`` can be a string column's name, a literal string
    or an expression that evaluates to a string.
    ``ParmSpec`` is a literal string (quoted with double quotes) specifying
    the parameters to extract and the destination columns for the result.
    It has the form:

     ::

      [AtrLst]&Key[:ColName][,AtrLst][&Key[:ColName][,AtrLst]...]

    It can start with a comma separated attribute list:

    * ``beg=c`` - Skip over the initial portion of QryVal up to and including
      the first 'c' character (single byte). A common value for 'c' is '?'.
      Without this attribute, the entire QryVal will be used.
    * ``zero`` - Zero out all destination columns before extraction.
    * ``dec=Num`` - Number of times to perform URL decode on the extracted
      values. Num must be between 0 and 99. Default is 1.
    * ``trm=c`` - Trim one leading and/or trailing 'c' character (single byte)
      from the decoded extracted values.

    ``Keys`` are the name of the parameters to extract.
    It should be URL encoded if it contains any special characters.
    Note that each ``Key`` specification starts with an '&'.
    The extracted value of Key is stored in a column given by ``ColName``.
    The column must be a previously defined column. If ``ColName`` is not
    given, a column with the same name as ``Key`` is assumed.
    Each ``Key`` can also have a comma separated attribute list:

    * ``zero`` - Zero out the destination column before extraction.
    * ``dec=Num`` - Number of times to perform URL decode on the extracted
      value of this Key. Num must be between 0 and 99.
    * ``trm=c`` - Trim one leading and/or trailing 'c' character (single byte)
      from the decoded extracted value.

  Example:

   ::

    sh# aq_pp ... -d i:Col1 ... -evlc l:Col_evl 'Col1 * 10' ...

  * Set new column Col_evl to 10 times the value of Col1.

   ::

    sh# aq_pp -rownum 101 ... -d i:Col1 ... -evlc i:Seq '$RowNum' ...

  * Set starting row index to 101 and set new column Seq to the row index.

   ::

    sh# aq_pp -fileid 1 -f file1 -d i:Col1 ... -evlc i:Id '$FileId'
          -fileid 2 -cat file2 ...

  * After file1 and file2 are concatenated together, the new "Id" column will
    have a value of 1 or 2 depending on which input file the record came from.

   ::

    sh# aq_pp ... -d s:Col1 s:Col2 ...
          -evlc is:Dt 'DateToTime(Col2, "Y.m.d.H.M.S.p") - DateToTime(Col1, "Y.m.d.H.M.S.p")'
          ...

  * Col1 and Col2 are date strings of the form "Year/Month/day Hour:Min:Sec AM".
    Dt will contain the time difference in seconds.


.. _`-mapf`:

``-mapf[,AtrLst] ColName MapFrom``
  Extract data from a string column.
  ``ColName`` is a previously defined column to extract data from.
  ``MapFrom`` defines the extraction rule using the
  `RT MapFrom Syntax`_.
  Optional ``AtrLst`` is:

  * ncas - Do case insensitive pattern match (default is case sensitive).

  Example:

   ::

    sh# aq_pp ... -d s:Col1 ...
          -mapf Col1 '%%v1_beg%%.%%v1_end%%'
          -mapc s:Col_beg '%%v1_beg%%'
          -mapc s:Col_end '%%v1_end%%'
          ...

  * Extract data from Col1, then put "parts" of this columns in 2 new columns.


.. _`-mapfrx`:

``-mapfrx[,AtrLst] ColName MapFrom``
  Extract data from a string column.
  ``ColName`` is a previously defined column/variable to extract data from.
  ``MapFrom`` defines the extraction rule using the
  `RegEx MapFrom Syntax`_.
  Optional ``AtrLst`` is:

  * ncas - Do case insensitive pattern match (default is case sensitive).

  Example:

   ::

    sh# aq_pp ... -d s:Col2 s:Col3 ...
          -mapfrx Col2 '\(.*\)-\(.*\)'
          -mapfrx Col3 '\(.*\)_\(.*\)'
          -mapc s:Col_beg '%%1%%,%%4%%'
          -mapc s:Col_end '%%2%%,%%5%%'
          ...

  * Extract data from Col2 and Col3, then put "parts" of those columns in 2
    new columns. Note that the RegEx based MapFrom's do not have named
    placeholders for the extracted data, they are implicit.
  * ``%%0%%`` - Reference the entire match in first ``-mapfrx`` (not used in example).
  * ``%%1%%`` - Reference the 1st subpattern match in first ``-mapfrx``.
  * ``%%2%%`` - Reference the 2nd subpattern match in first ``-mapfrx``.
  * ``%%3%%`` - Reference the entire match in second ``-mapfrx`` (not used in example).
  * ``%%4%%`` - Reference the 1st subpattern match in second ``-mapfrx``.
  * ``%%5%%`` - Reference the 2nd subpattern match in second ``-mapfrx``.


.. _`-mapc`:

``-mapc ColSpec|ColName MapTo``
  Render data extracted via previous `-mapf`_ and/or `-mapfrx`_ into a new
  column or into an existing column/variable.
  The column must be of string type.

  * If ``ColSpec`` is given, a new column will be created using the spec.
    See `-d`_ for details.
  * If a ``ColName`` is given, it must refer to a previously defined
    column/variable.

  ``MapTo`` is the rendering spec. See `MapTo Syntax`_ for details.

  Example:

   ::

    sh# aq_pp ... -d s:Col1 s:Col2 s:Col3 ...
          -mapf Col1 '%%v1_beg%%.%%v1_end%%'
          -mapfrx Col2 '\(.*\)-\(.*\)'
          -mapfrx Col3 '\(.*\)_\(.*\)'
          -mapc s:Col_beg '%%v1_beg%%,%%1%%,%%4%%'
          -mapc s:Col_end '%%v1_end%%,%%2%%,%%5%%'
          ...

  * Extract data from Col1, Col2 and Col3, then put "parts" of those columns
    in 2 new columns. Note that the RegEx based MapFrom's do not have named
    placeholders for the extracted data, they are implicit.
  * ``%%0%%`` - Reference the entire match in first ``-mapfrx`` (not used in example).
  * ``%%1%%`` - Reference the 1st subpattern match in first ``-mapfrx``.
  * ``%%2%%`` - Reference the 2nd subpattern match in first ``-mapfrx``.
  * ``%%3%%`` - Reference the entire match in second ``-mapfrx`` (not used in example).
  * ``%%4%%`` - Reference the 1st subpattern match in second ``-mapfrx``.
  * ``%%5%%`` - Reference the 2nd subpattern match in second ``-mapfrx``.


.. _`-kenc`:

``-kenc ColSpec|ColName ColName [ColName ...]``
  Encode a *key* column from the given ``ColNames``.
  The *key* column must be of string type.
  The *encoded* value it stores constains binary data.

  * If ``ColSpec`` is given, a new column will be created using the spec.
    See `-d`_ for details.
  * If a ``ColName`` is given, it must refer to a previously defined
    column/variable.

  The source ``ColNames`` must be previously defined.
  They can have any data type.

  Example:

   ::

    sh# aq_pp ... -d s:Col1 i:Col2 ip:Col3 ...
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

    sh# aq_pp ... -d s:Key1 ...
          -kdec Key1 s:Col1 i:Col2 ip:Col3
          ...

  * Extract Col1, Col2 and Col3 from Key1.

   ::

    sh# aq_pp ... -d s:Key1 ...
          -kdec Key1 s: i:Col2 ip:
          ...

  * Extract only Col2 from Key1. Since there is no '+' in the extract-to spec,
    the value of Key1 is NOT altered.

   ::

    sh# aq_pp ... -d s:Key1 ...
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
  It has the basic form ``LHS <compare> RHS``.
  LHS can be a column/variable name or an expression to evaluate:

  * Column/variable name is case insensitive.
  * Evaluation has the form ``Eval(Expr)`` where ``Expr`` is the expression
    to evaluate as in `-evlc`_.

  RHS can be a column/variable name or a literal value:

  * Column/variable name is case insensitive.
  * Literal string must be quoted with double quotes.

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
    LHS value matches RHS pattern. LHS must be a string column and
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
  For example::

    LHS_1 == RHS_1 && !(LHS_2 == RHS_2 || LHS_3 == RHS_3)

  In a quoted string literal, '\\' and double quotes must be '\\' escaped.
  In addition, if the RHS is a pattern (``~~`` and ``!~`` operators)
  literal '*' and '?' in the pattern must also be '\\' escaped.

  Example:

   ::

    sh# aq_pp ... -d s:Col1 s:Col2 i:Col3 s:Col4 ...
          -filt 'Col1 === Col4 && Col2 != "" && Col3 >= 100'
          ...

  * Only keep records whose Col1 and Col4 are the same (case insensitive) and
    Col2 is not blank and Col3's value is greater than or equal to 100.


.. _`-map`:

``-map[,AtrLst] ColName MapFrom MapTo``
  See `-maprx`_ below.


.. _`-maprx`:

``-maprx[,AtrLst] ColName MapFrom MapTo``
  Remap (a.k.a., rewrite) a string column's value.
  ``ColName`` is a previously defined column/variable.
  ``MapFrom`` is the extraction rule.

  * See `RT MapFrom Syntax`_ regarding ``-map`` MapFrom syntax.
  * See `RegEx MapFrom Syntax`_ regarding ``-maprx`` MapFrom syntax.

  ``MapTo`` is the rendering spec. See `MapTo Syntax`_ for details.
  Optional ``AtrLst`` is:

  * ncas - Do case insensitive pattern match (default is case sensitive).

  Example:

   ::

    sh# aq_pp ... -d s:Col1 ...
          -map Col1 '%%v1_beg%%-%*' 'beg=%%v1_beg%%'
          ...
    sh# aq_pp ... -d s:Col1 ...
          -maprx Col1 '\(.*\)-*' 'beg=%%1%%'
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

  ``ColTags`` are optional. They specify the columns in the files. Supported
  tags (case insensitive) are:

  * ``FROM`` - marks the column used to match the value of ColName.
  * ``TO`` - marks the column used as the new value of ColName.
  * ``X`` - marks an unused column.

  If ``ColTag`` is used, both the ``FROM`` and ``TO`` tags must be given.
  Any number of ``X`` can be specified.
  If ``ColTag`` is not used, the files are assumed to contain
  *exactly 2 columns* - the ``FROM`` and ``TO`` columns, in that order.

  The ``FROM`` value is generally a string constant. Patterns can also be used,
  see the ``pat`` attribute description above.
  The ``TO`` value is always a string constant.
  Matches are carried out according to the order of the match value in the
  files. Match stops when the first match is found. If the files contain both
  exact value and pattern, then:

  1) Exact values are matched first, skipping over any interleaving patterns.
  2) Patterns are matched next, skipping over any interleaving fixed values.

  **Note**: If a file name happens to be one of ``FROM``, ``TO`` or ``X``
  (case insensitive), prepend the name with a path (e.g., "./X")
  to avoid misinterpretation.

  Example:

   ::

    sh# aq_pp ... -d s:Col1 ... -sub Col1 lookup.csv ...

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

  The ``FROM`` value is generally a string constant. Patterns can also be used,
  see the ``pat`` attribute description above.
  Matches are carried out according to the order of the match value in the
  files. Match stops when the first match is found. If the files contain both
  exact value and pattern, then:

  1) Exact values are matched first, skipping over any interleaving patterns.
  2) Patterns are matched next, skipping over any interleaving fixed values.

  **Note**: If a file name happens to be one of ``FROM`` or ``X``
  (case insensitive), prepend the name with a path (e.g., "./X")
  to avoid misinterpretation.

  Example:

   ::

    sh# aq_pp ... -d s:Col1 ... -grep,rev Col1 lookup.csv ...

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

    sh# aq_pp ... -d s:Col1 s:Col2 i:Col3 s:Col4 ...
          -cmb lookup.csv i:Col3 s:Col1 s:Col5 s:Col6
          ...

  * Combine lookup.csv into the data set according to composite key
    <Col3, Col1>.
    The resulting data set will have columns Col1, Col2, Col3, Col4, Col5 and
    Col6.

   ::

    sh# aq_pp ... -d s:Col1 s:Col2 i:Col3 s:Col4 ...
          -cmb lookup.csv i:Col3 s:Col1 s:Col5 s:Col6 s,cmb:Col2
          ...
    sh# aq_pp ... -d s:Col1 s:Col2 i:Col3 s:Col4 ...
          -cmb lookup.csv i,key:Col3 s,key:Col1 s,cmb:Col5 s,cmb:Col6 s,cmb:Col2
          ...

  * Both are the same as the previous example, except that Col2 is explicitly
    set as a combine column. That is, its value will originally come from the
    current data set, then it will be overwritten if there is a match from the
    lookup table.


.. _`-pmod`:

``-pmod ModSpec``
  Call the processing function in the module to process the current record.
  The function is typically used to implement custom logics.

  * Retrieve and/or modify one or more columns in the current data row.
  * Filter out the current data row.
  * Generate multiple output rows from the current row.
  * Stop processing.

  ``ModSpec`` has the form ``ModName[:argument]`` where ``ModName``
  is the logical module name and ``argument`` is a module specific
  parameter string.
  aq_pp will look for "pmod/``ModName``.so" in the directory where aq_pp is
  installed. For example, if aq_pp is installed as ``/SomeDirectory/aq_pp``,
  aq_pp will load ``/SomeDirectory/pmod/ModName.so``.
  See the examples under "pmod/" in the source package regarding how this
  type of module is implemented.


.. _`-o`:

``[-o[,AtrLst] File] [-c ColName [ColName ...]] [-notitle]``
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

  Optional ``-notitle`` suppresses the column name label row from the output.
  A label row is normally included by default.

  Multiple sets of "``-o ... -c ... -notitle``" can be specified.

  Example:

   ::

    sh# aq_pp ... -d s:Col1 s:Col2 s:Col3 ... -o,esc,noq - -c Col2 Col1

  * Output Col2 and Col1 (in that order) to stdout in a format suitable for
    Amazon Cloud.


.. _`-udb`:

``-udb [-spec UdbSpec|-db DbName] -imp [DbName:]TabName [-seg N1[-N2]/N] [-nobnk] [-nonew] [-mod ModSpec]``
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

  Optional "``-mod ModSpec``" specifies a module to load on the server side.
  ``ModSpec`` has the form ``ModName[:argument]`` where ``ModName``
  is the logical module name and ``argument`` is a module specific
  parameter string. Udb server will try to load "mod/``ModName``.so"
  in the server directory.

  Multiple sets of "``-udb -spec ... -imp ...``" can be specified.


.. _`-ovar`:

``-ovar[,AtrLst] File [-c ColName [ColName ...]] [-notitle]``
  Output the final variable values.
  Variables are those defined using the `-var`_ option.
  Only a single data row is output.

  "``-ovar[,AtrLst] File``" sets the output attributes and file.
  If ``File``` is a '-' (a single dash), data will be written to stdout.
  Optional ``AtrLst`` is described under `Output File Attributes`_.

  Optional "``-c ColName [ColName ...]``" selects the variables to output.
  ``ColName`` refers to a previously defined variable.
  Without ``-c``, all variables are selected by default.

  Optional ``-notitle`` suppresses the column name label row from the output.
  A label row is normally included by default.

  Multiple sets of "``-ovar ... -c ... -notitle``" can be specified.

  Example:

   ::

    sh# aq_pp ... -d i:Col1 i:Col2 ... -var i:Sum1 0 -var i:Sum2 0 ...
          -evlc Sum1 'Sum1 + Col1' -evlc Sum2 'Sum2 + (Col2 * Col2)' ...
          -ovar - -c Sum1 Sum2

  * Calculate sums and output their evaluates at the end of processing.


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


Input File Attributes
=====================

Each input file can have these comma separated attributes:

* ``eok`` - Make error non-fatal. If there is an input error, program will
  try to skip over bad/broken records. If there is a record processing error,
  program will just discard the record.
* ``qui`` - Quiet; i.e., do not print any input/processing error message.
* ``tsv`` - Input is in TSV format (default is CSV).
* ``sep=c`` - Use separator 'c' (single byte) as column separactor.
* ``bin`` - Input is in binary format (default is CSV).
* ``esc`` - '\\' is an escape character in input fields (CSV or TSV).
* ``noq`` - No quotes around fields (CSV).
* ``+Num[b|r|l]`` - Specifies the number of bytes (``b`` suffix), records (``r``
  suffix) or lines (no suffix or ``l`` suffix) to skip before processing.

By default, input files are assumed to be in formal CSV format. Use the
``tsv``, ``esc`` and ``noq`` attributes to set input characteristics as needed.


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
  ``%%myVar%%`` -
  Extract the value into a variable named ``myVar``. ``myVar`` can later be
  used in the MapTo spec.
* Literals and variables -
  ``literal_1%%myVar_1%%literal_2%%myVar_2%%`` -
  A common way to extract specific data portions.
* Case sensitive or insensitive toggling -
  ``literal_1%=literal_2%=literal_3`` -
  ``%=`` is used to toggle case sensitive/insensitive match. In the above case,
  if `-mapf`_ or `-map`_ does not have the ``ncas`` attribute, then
  ``literal_1``'s match will be case sensitive, but ``literal_2``'s will be
  case insensitive, and ``literal_3``'s will be case sensitive again.
* '\\' escape -
  ``\%\%not_var\%\%%%myVar%%a_backslash\\others`` -
  If a '%' is used in such a way that resembles an unintended MapFrom spec,
  the '%' must be escaped. Literal '\\' must also be escaped.
  On the other hand, '\\' has no special meaning within a variable spec
  (described below).

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

  Multiple classes can be used; e.g., ``%%myVar:@nab%%`` for all alphanumerics.
* ``:[chars]`` (``[]`` is part of the syntax) is similar to the character class
  described above except that the allowed characters are set explicitly.
  Note that ranges is not supported, all characters must be specified.
  For example,
  ``%%myVar:[0123456789abcdefABCDEF]%%`` (same as
  ``%%myVar:@n:[abcdefABCDEF]%%``) for hex digits. To include a ']'
  as one of the characters, put it first, as in ``%%myVar:[]xyz]%%``.
* ``:min[-max]`` is the min and optional max length (bytes, inclusive) to
  extract. Without a max, the default is unlimited (actually ~64Kb).
* ``,brks`` defines a list of characters at which extraction of the variable
  should stop. For example, ``%%myVar,,;:%%`` will extract data into myVar
  until one of ``,;:`` or end-of-string is encountered. This usuage is often
  followed by a wild card, as in ``%%myVar,,;:%%%*``.


RegEx MapFrom Syntax
====================

Regular expression style MapFrom is used in both `-mapfrx`_ and `-maprx`_
options. The MapFrom spec is used to match and/or extract data from a string
(a column value).

Differences between RegEx mapping and RT mapping:

* RT pattern always matches the entire string, while RegEx pattern matches a
  substring by default. To get the same behavior, add '^' and '$' to the
  beginning and end of a RegEx as in ``^pattern$``.
* RegEx MapFrom does not have named variables for the extracted data. Instead,
  extracted data is put into implicit variables ``%%0%%``, ``%%1%%``, and so on.
  See `-mapfrx`_ for an usage example.

Regular Expression is very powerful but also complex. Please consult the
GNU RegEx manual for details.


MapTo Syntax
============

MapTo is used in `-mapc`_, `-map`_ and `-maprx`_. It renders the data
extracted by MapFrom into a column. Both RT and RegEx MapTo share the same
syntax:

* A literal - In other words, the result will be a constant.
* A variable -
  ``%%myVar%%`` -
  Substitute the value of ``myVar``.
* Literals and variables -
  ``literal_1%%myVar_1%%literal_2%%myVar_2%%`` -
  A common way to render extracted data.
* '\\' escape -
  ``\%\%not_var\%\%%%myVar%%a_backslash\\others`` -
  If a '%' is used in such a way that resembles an unintended MapTo spec,
  the '%' must be escaped. Literal '\\' must also be escaped.
  On the other hand, '\\' has no special meaning within a variable spec
  (described below).

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

See `-mapfrx`_ for an usage example.


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
`-evlc`_, `-mapf`_, `-mapc`_, `-kenc`_, `-kdec`_,
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

  sh# aq_pp ... -d i:Col1 ...
        -if -filt 'Col1 == 1'
          -evlc s:Col2 '"Is-1"'
        -elif -filt 'Col1 == 2'
          -false
        -else
          -evlc Col2 '"Others"'
        -endif
        ...

* Set Col2's value based on Col1's.
  In addition, discard any record with Col1==2.

 ::

  sh# aq_pp ... -d i:Col1 s:Col2 ...
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

* `udbd <udbd.html>`_ - User (Bucket) Database server
* `udb.spec <udb.spec.html>`_ - Udb spec file.
* `aq_udb <aq_udb.html>`_ - Interface to Udb server

