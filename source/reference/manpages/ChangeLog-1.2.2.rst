.. |<br>| raw:: html

   <br>

===================
Change Log - V1.2.2
===================

:Replaces: V1.2.1
:Dev cycle: 2015-03-02 to 2015-05-06


Introduction
============

The following sections list the category/command specific changes.
There are 3 kind of changes:

* [Warn] |<br>|
  A feature has changed in a backward compatible manner.
  The old usage is still supported, but applications should switch to the new
  usage as soon as possible.

* [Critical] |<br>|
  A feature has changed in a non backward compatible manner.
  Applications must be ported to the new usage in order to use the new version.

* [New] |<br>|
  A feature is new.


Common
======

* [Critical] |<br>|
  Pattern comparison operators (``~~`` ``##`` etc) in ``aq_pp``/``aq_udb``
  filter expression  have been removed.
  A new ``PatCmp(Val, Pattern [, AtrLst])`` function is provided for the
  purpose. Convert old filter expressions this way:

  * ``-filt LHS ~~ "pattern"`` => ``-filt PatCmp(LHS, "pattern")``
  * ``-filt LHS ~~~ "pattern"`` => ``-filt PatCmp(LHS, "pattern", "ncas")``
  * ``-filt LHS ## "pattern"`` => ``-filt PatCmp(LHS, "pattern", "rx")``
  * ``-filt LHS ~## "pattern"`` => ``-filt PatCmp(LHS, "pattern", "ncas,rx")``
  * ``-filt LHS ### "pattern"`` => ``-filt PatCmp(LHS, "pattern", "ncas,rx")``

* [Critical] |<br>|
  Retired the ``-tag TagLab`` feature. Message *tagging* did not seem useful.

* [Warn] |<br>|
  Need quotes around string values for ``-var`` and ``-bvar`` in
  ``aq_pp``/``aq_udb``
  If double quoted, escape sequence in the value is interpreted.
  In order to preserve compatibility, the program assumes new syntax if the
  value has matching leading and trailing quotes, old syntax otherwise.
  If the quotes are part of the intended value, then the new syntax must be
  used to protect the intended quotes.

* [Warn] |<br>|
  ``-notitle`` options for all aq_tool commands should be specified as an
  attribute for the intended output option. For example,

  * ``-o File -notitle`` => ``-o,notitle File``

* [New] |<br>|
  Generalized/simplified ``aq_pp``/``aq_udb`` filter expression syntax.
  The goal was to support an expression like:

  ::

    Col1 + 2 > Func(Col2) && Col3 && Func(Col4) ...

  To accomplish this, ``aq_pp``/``aq_udb`` expression parser were redesigned
  with these enhancements:

  * Expression evaluation without ``Eval()``.
  * Expression evaluation on either side of comparison.
  * Comparison operator optional.
    Convert result to Boolean when there is no comparison operator.

* [New] |<br>|
  Support ``-eval - Expr`` in ``aq_pp``/``aq_udb``.
  In other words, evaluate an expression without putting the result anywhere.
  Note that the ``ColName`` parameter is set to "-" (a dash).
  Useful for functions that put their outputs in individual columns by
  themselves (e.g., ``QryParmExt()`` of ``aq_pp`` and
  ``KDec()`` of ``aq_udb``).

* [New] |<br>|
  Support escape sequences (``\t``, ``\n``, ... ``\xHH``) in various specs
  and string constants.
  Interpretation of the following are affected:

  * Mapping spec in ``aq_pp``.
  * Double quoted string constants in ``aq_pp``/``aq_udb`` filter/evaluation
    expressions.
  * Double quoted ``-var`` and ``-bvar`` string value in ``aq_pp``/``aq_udb``.
  * ``sep=CHAR`` input attribute in all aq_tool commands.

* [New] |<br>|
  Redesigned broken pipe handling in ``aq_pp``, ``aq_udb`` and Udb server.
  ``aq_pp``/``aq_udb`` used to ignore SIG_PIPE, causing a chain of I/O error
  messages because the signal was ignored and the program continued to run.
  Simplest way to avoid the unneccessary errors is NOT to ignore SIG_PIPE
  and let the program die.

  On the Udb server side, broken pipe condition must be detected via the
  communication channels. This is only necessary for export operations which
  is handled by threads. Unfortunately, an export thread cannot detect
  a broken pipe until it writes to the the pipe (i.e, send data back to
  ``aq_udb``). In order to catch the condition sooner, a new broken pipe
  detection was added to main so that main can tell a thread to stop in case
  it has not yet detected the broken pipe condition.

* [New] |<br>|
  Inputting from stdin or outputting to stdout can take an optional label
  as in ``-f -,Label`` or ``-o -,Label``. The given ``Label`` will replace the
  default "<stdin>" and "<stdout>" labels used in various progress and
  error messages.


Udb Spec
========

* [Warn] |<br>|
  PKEY is now defined *outside* of table/vector spec. Only one PKEY spec
  is needed per DB. This is done using a a new udb.spec entry:

  ::

    @PKey:
      s:common_pkey_colname

* [Critical] |<br>|
  Defining PKEY per table/vector (the old way) is still supported,
  but all PKEY columns *must* have the same name.


aq_pp
=====

* See also `common`_ changes.

* [Warn] |<br>|
  Option name change:

  * ``-evlc`` => ``-eval``

  Old one still works for now.

* [Warn] |<br>|
  Reduced mapping option set.
  Old-to-new options are:

  * ``-mapfrx`` => ``-mapf,rx[,rx_*]``
  * ``-maprx`` => ``-map,rx[,rx_*]``

  Old ones still work for now.

* [Critical] |<br>|
  The file ID concept and relate features are no longer needed.
  ``-fileid`` option removed.
  ``$FileId`` variable removed.

* [Critical] |<br>|
  ``-rx_syntax`` option removed.
  Regex syntax related settings must now be specified as attributes for
  the mapping options.

* [New] |<br>|
  Support column aliases and column rename. New options are:

  * ``-alias ColName AltName`` - Allow a column or an alias to be addressed
    using another name. The same column can be aliased multiple times.
  * ``-renam ColName NewName`` - Rename a column or an alias.

  Use cases include:

  * Use arbitrary names in output title line without having to duplicate
    columns. For example, "aq_pp -d s:Col1 -alias Col1 Val1 -c Val1" will
    output the label "Val1" instead "Col1" in the title line.
  * Match Udb spec columns that are named differently from the aq_pp columns.
    Simply tie the columns together using aliases.
  * Raname columns during processing to reflect changes in their values.
    For example, a column called "Sum" can be renamed to "Avg" after the
    appropriate arithmetics.

* [New] |<br>|
  A new option that prints a message. Useful for debugging.
  Should be used with ``-if`` though. The new option is ``-mesg Message``.

* [New] |<br>|
  Suppress error messages from ``-eval`` and ``-kdec`` when they follow
  a ``-if`` or ``-elif``. Also, error handling no longer depends on the
  input's "eok" and "qui" attributes. New scheme is:

  * No ``-if`` - A message is printed and the row is skipped.
    In other words, error is not fatal.
  * With ``-if`` - No error message is printed and the row is kept.
    ``-mesg`` and ``-skip``/``-quit`` must be used to change this behavior.


aq_udb/udb server
=================

* See also `common`_ changes.

* [Critical] |<br>|
  ``aq_tool/udb/udbd`` and ``aq_tool/udb/.udbd`` have been removed.
  Use ``aq_tool/bin/udbd`` to start Udb server.

* [Warn] |<br>|
  To set the user bucket as the ``-pp`` target, use pseudo table name
  "." (a dot) instead of "bucket".

* [Critical] |<br>|
  To address the user bucket key, use the common PKEY column name in
  Udb spec instead of the pseudo column name "name".

* [Warn] |<br>|
  Reduced top level option set.
  Old-to-new options are:

  * ``-exp_usr`` => ``-exp [DbName:].``
  * ``-cnt_usr`` => ``-cnt [DbName:].``
  * ``-scn_usr`` => ``-scn [DbName:].``
  * ``-ord_all`` => ``-ord [DbName:].``
  * ``-clr_all`` => ``-clr [DbName:].``

  These are consistent with the existing ``-Action [DbName:]TabName`` specs.
  Note the use of table name "." (a dot).

* [Critical] |<br>|
  Major ``-pp`` specific option changes.
  Old-to-new options are:

  * ``-pp_var`` => ``-bvar``
  * ``-pp_evlc`` => ``-eval`` (note abbrevriation change)
  * ``-pp_filt`` => ``-filt``
  * ``-pp_goto`` => ``-goto``
  * ``-pp_end_of_scan`` => ``-end_of_scan``

  More importantly, ``-pp`` group should now be terminated with a ``-endpp``
  marker. The reason is that ``-bvar``, ``-eval`` and so on are also valid
  options *outside* of ``-pp``; the end marker is needed to set the scope of
  the common options.

* [New] |<br>|
  Support ``-eval``, ``-goto``, ``-bvar`` and ``-if-else-endif`` outside of
  ``-pp``.
  In other words, all the ``-pp`` related options can now be used on the
  target ``-exp``, ``-cnt`` and ``-scn`` table.

* [New] |<br>|
  Support "ObjName.ColName" when selecting output columns, sort columns and
  column reference in filter/evaluation expressions.
  Currently, "ObjName" is implicit - it is the target/relevent object or
  the Var vector. With "ObjName.ColName", coverage can be extended to
  other objects. Applicable objects are usage dependent:

  * Export output columns (``-c``) - Target table/vector, "Var", "." (user
    bucket) and any vectors.
  * Internal table sort (``-ord``) - Target table only.
  * Export result sort (``-sort``) - Anything from the output columns.
  * Filter and evaluation expression - Target table/vector, "Var", "." (user
    bucket) and any vectors.

* [New] |<br>|
  Support ``-c`` during an user export (``-exp_usr`` or ``-exp .``).
  In particular, Var columns can now be selected along with the PKEY.
  The PKEY column can be selected using the common PKEY column name in
  Udb spec.
  Var columns can be selected using their names or "Var.ColName".
  Recall that older versions can only output PKEY.

* [New] |<br>|
  Added new ``KDec(Val, "KeySpec;KeySpec;...")`` function to decode an
  ``aq_pp -kenc`` encoded ``Val`` and save the decoded components into
  individual columns. "KeySpec" can be a column name or just "Type:" if the
  decoded component is not needed.

* [New] |<br>|
  ``roi`` module for ROI counting. ROI spec is given in the module argument:

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


loginf
======

* [New] |<br>|
  ``-f`` can take a ``notitle`` attribute as in ``-f,notitle ...``.
  With this attribute, the program will not assume that the first record from
  each input file is a column label line.

  Also, a new label-check will be used when ``notitle`` is not set.
  If *any* label from the first record fails this check, the entire record
  will be re-interpreted as a data record and no label will be extracted.

* [New] |<br>|
  Output more per-column info in JSON report:

  * ``Index`` - Column index; starts from 1.
  * ``Label`` - Column label. Not always available.
  * ``pp-Type`` - Column type for aq_tool column spec.
  * ``pp-Attr`` - Column attribute for aq_tool column spec.
  * ``pp-Name`` - Column name for aq_tool column spec.
  * ``pp-Sample`` - First column sample value.

* [New] |<br>|
  Add a ``-b64`` option that encodes strings in base64 format when outputting
  the JSON report. Added a new output field:

  * Report String Encoding`` - ``true`` if base64 encoding has been applied,
    ``false`` otherwise.


logcnv
======

* [Critical] |<br>|
  Removed special ``hl1`` column attribute for the first HTTP request line.
  With this attribute, 3 columns were automatically from a single
  input field. Now, this should be done manually using 3 separate column
  specs and 2 separator specs:

  * ``-d ... S,clf,hl1:r ...`` =>
    ``-d ... S:r_f1 SEP:' ' S,clf:r_f2 SEP:' ' S:r_f3 ...``

* [New] |<br>|
  Support fixed-length data column extraction.
  Data columns are uaually terminated by a separator or at end-of-record.
  With a length spec, a data column can be followed by another data column.


jsncnv
======

* [New] |<br>|
  Made a JSON converter that works like ``logcnv``. It has a newly designed
  stream based JSON parser. This specialized parser does not create any
  JSON structure - it merely extracts the requested fields.
  Requested fields can be specified as
  "KeyName[Index].KeyName[Index]...."  or
  "[Index].KeyName[Index].KeyName[Index]...."

  This is a new tool. See its manual page for details.

