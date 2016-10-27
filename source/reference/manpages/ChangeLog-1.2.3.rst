.. |<br>| raw:: html

   <br>

===================
Change Log - V1.2.3
===================

:Replaces: V1.2.2
:Dev Cycle: 2015-05-06 to 2016-03-22
:Revision: V1.2.3-1 2015-09-08
:Revision: V1.2.3-2 2015-10-29
:Revision: V1.2.3-3 2015-11-19
:Revision: V1.2.3-4 2015-12-14
:Revision: V1.2.3-5 2016-02-08
:Revision: V1.2.3-6 2015-03-22


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

* [New] 1.2.3-1: |<br>|
  ``logcnv`` style column spec is now supported by all ``aq_*`` commands.
  The only exception is the ``tim`` column attribute which is no longer
  supported. To reproduced this function, save the column as a string
  and then use ``-eval i:time 'DateToTime(time_str, "d.b.Y.H.M.S.z")'``
  in ``aq_pp`` to do an explicit time conversion.

* [New] 1.2.3-2: |<br>|
  ``aq_*`` commands support length spec in delimiter-separated-values
  format - for example, "...<sep>Fixed-length-value<sep>...".
  This differs from the ``logcnv`` specification in that surrounding
  separators (where appropriate) are expected.

* [New] 1.2.3-1: |<br>|
  ``aq_*`` commands now support an explicit column *index* spec.
  It is designed to help simplify column spec when many ``X`` columns are
  involved. For example, these 2 specs are equivalent:

  ::

    $ aq_command ... -d s:Col_1 x ... x s,trm:Col_98 s:Col_99 x ... x s:Col_999
    $ aq_command ... -d s:Col_1 s,trm@98:Col_98 s:Col_99 s@999:Col_999

  All unspecified columns are assigned ``X`` automatically.

* [New] 1.2.3-1: |<br>|
  ``aq_*`` commands now implicitly ignore unspecified columns at the end of
  a record. No ``eok`` attribute is needed and no error is generated.
  This only works for fixed separator formats (e.g., CSV).
  It does not work for binary or ``logcnv`` style formats.

* [New] 1.2.3-1: |<br>|
  (New but removed in 1.2.3-6.)
  Support command line *option-macros* - a kind of custom options that
  represent one or more options+parameters. aq_tool commands supporting this
  feature will automatically load the default command specific macro
  definitions at startup (e.g., from "``etc/aq_pp.d/*.m``" for ``aq_pp``,
  "``etc/aq_udb.d/*.m``" for ``aq_udb``).
  Custom macro files or directories can also be specified on the command line
  via the new ``-m`` option.

  This feature is availabe in ``aq_pp`` and ``aq_udb``.

* [New] 1.2.3-1: |<br>|
  Support ``csv`` as an input option attribute. This used to be supported,
  but was removed since CSV is the default. Turned out command generation
  became more difficult when it was removed, so it is back.

* [New] 1.2.3-1: |<br>|
  Support ``csv`` as an output option attribute. CSV used to be the *only*
  output format, so the attribute was not necessary. Now, ``sep=c`` can be
  used to select a custom separator. Note that a custom separator format is
  not as advanced as CSV - there is no provision for escaping the separator
  itself within a field value. Use the ``esc`` attribute if appropriate.
  CSV is still the default when no separator is selected.

* [Critical] 1.2.3-1: |<br>|
  ``aq_pp`` and ``aq_udb`` command line module specification has changed.
  Parameters are no longer given as a single string like
  "``module:parameters``". Instead, the new spec uses a function-like syntax
  as in "``module("arg1","arg2",...)``". Note the quotes (single or double)
  around the arguments. For now, the arguments can only be string constants.

* [Critical] 1.2.3-1: |<br>|
  Removed ``aq_ord_fil`` from package. Can easily be reinstated if necessary.

* [New] 1.2.3-5: |<br>|
  Support input data in HTML Table format via "``-f,tab``". The parser is
  rather primitive though - columns must be enclosed in "``<td>data</td>``" or
  "``<td ...>data</td>``" and rows must be terminated by a "``</tr>``"
  (everything else is simply ignored).

* [Warn] 1.2.3-5: |<br>|
  Allow *divide-by-zero* in floating point arithmetic. This result in either
  ``nan`` or ``inf`` (these are special floating point values).
  Other versions always map the divide-by-zero result to zero.

* [New] 1.2.3-5: |<br>|
  Column limit in the processing tools (excluding ``loginf``) has been raised
  from 256 to 2048.

* [Warn] 1.2.3-5: |<br>|
  Custom modlule handling has changed.
  On-the-fly module compilation is now done on the master machine. The compiled
  module will then be sent to the worders. The old design was to send the
  module source to the workers for compilation.
  The new design can also take a pre-compiled module file as input.
  The old design only accepted a module source file.

* [New] 1.2.3-5: |<br>|
  ``aq_tool`` commands now search for ``aq_tool`` home directory at several
  locations:

  * ``command_directory/../aq_tool/``
  * ``command_directory/../``
  * ``/opt/aq_tool/``

* [Critical] 1.2.3-6: |<br>|
  The command line *option-macros* feature introduced in 1.2.3-1 has been
  removed. It was not useful.


aq-emod
=======
Cf: `aq-emod <aq-emod.html>`_

* [New] 1.2.3-1: |<br>|
  Generalized the *emod* (``eval`` function module) design so that the
  same source can be used to build modules for both ``aq_pp`` and
  Udb (via ``aq_udb``). In this way, *all* emod functions are now
  available to both tools.

  Furthermore, ``aq_pp``'s ``-emod`` option for custom module loading has been
  removed. This has been replaced by predefined evaluation module specs
  "``etc/aq_pp.d/*.emod``". The specs contain evaluation function to module
  name lookup; in this way, ``aq_pp`` can determine which modules to load
  based on the functions needed.

* [Critical] 1.2.3-1: |<br>|
  Interpretation of the pattern argument in the ``PatCmp()`` function has
  changed. This is only important when the pattern contains *literal*
  backslashes. Old scheme was inconsistent and probably wrong as well.
  To illustrate, consider a pattern containing a literal ``\`` and
  a literal ``*`` - they must be escaped to prevent their special meaning.
  The old scheme's representations are:

  ::

    PatCmp(col, '* \\ and \* *')
    PatCmp(col, "* \\ and \* *")

  The first form, with single quotes, is correct and no change is needed.
  The second form, with double quotes, was unfortunately wrong.
  The new and correct form is:

  ::

    PatCmp(col, "* \\\\ and \\* *")

* [New] 1.2.3-1/2: |<br>|
  Added new functions.
  See the new "aq-emod" documentation page for more info.

  * ``SubStr()`` - Extract a substring by byte position and length.
  * ``ClipStr()`` - Extract a substring using RT's *clipping* mechanism.
  * ``IConv()`` - Converts language encoding; supports multiple from-types.
  * ``CountryName()``, ``CountryRegion()`` - Extract subsets of the
    ``IpToCountry()`` result.
  * ``AgentName()``, ``AgentOS()``, ``AgentDevType()``, ``AgentDevName()`` -
    Extract subsets of the ``AgentParse()`` result.
  * ``IsCrawler()`` - Check if the ``AgentParse()`` result is a crawler.

* [Critical] 1.2.3-2: |<br>|
  RT functions name change:

  * ``SearchKey2(Site, Path)`` -> ``SearchKey(Site, Path)``
  * ``AgentParse2(Agent, Ip)`` -> ``AgentParse(Agent, Ip)``

* [New] 1.2.3-5: |<br>|
  Added new functions.
  See the new "aq-emod" documentation page for more info.

  * ``Ceil()``, ``Floor()``, ``Round()`` - Correspond to standard math functions
    of the same names.
  * ``Abs()`` - Does absolute value.
  * ``IsNaN()``, ``IsInf()`` - Test if a number is ``nan`` or ``inf``.
  * ``NumCmp()`` - Compare numbers to within a delta precision.
  * ``GmDateToTime()``, ``TimeToGmDate()`` - Perform UTC date to/from time
    conversion.


aq_cat
======
Cf: `aq_cat <aq_cat.html>`_

* [New] 1.2.3-1: |<br>|
  Concencate multiple record streams into one. Records can be in
  delimiter-separated-values format or aq_tool's internal binary format.

  This is a new tool. See its manual page for details.

* [New] 1.2.3-1: |<br>|
  Support output column selection even when no column spec is given.
  This is done by supplying the column index (1+) instead of name.


aq_pp
=====
Cf: `aq_pp <aq_pp.html>`_

* See also `common`_ changes.

* [Critical] 1.2.3-1: |<br>|
  Removed ``-emod`` option. It was used for loading custom evaluation modules.
  See `aq-emod`` for details.

* [Critical] 1.2.3-1: |<br>|
  Removed "``rt.so``" help page. See the new "aq-emod" page instead.

* [New] 1.2.3-1: |<br>|
  ``aq_pp`` now supports all the standard Udb evaluation functions.
  See the new "aq-emod" documentation page for more info.

* [New] 1.2.3-5: |<br>|
  "-sub" and ``-cmb`` support an ``all`` attribute. This will make use of
  *all* the matches from the lookup table instead of just the first one.
  Each match will produce one output row.


aq_udb/udb server
=================
Cf: `aq_udb <aq_udb.html>`_, `udbd <udbd.html>`_

* See also `common`_ changes.

* [New] 1.2.3-1: |<br>|
  Udb now supports all the ``aq_pp`` evaluation functions.
  See `aq-emod`` for details.

* [New] 1.2.3-5: |<br>|
  Raised Udb server worker threads count limit from 8 to 32.

* [New] 1.2.3-6: |<br>|
  Udb server now returns a more detailed error message to ``aq_pp``/``aq_udb``
  in case of a request error (the same message that used to be stored in the
  server log only. Note that these messages are only available during request
  initialization. No message can be returned once processing has started.

* [Critical] 1.2.3-6: |<br>|
  Keyword ``bucket`` (case insensitive) can no longer be used to refer to the
  user bucket in "-pp" statements. A ``.`` (a dot) is the only valid
  representation.


loginf
======
Cf: `loginf <loginf.html>`_

* [New] 1.2.3-2: |<br>|
  ``loginf`` has an "``-f,auto``" mode for file format detection.
  This is done by examining the first 256k of the input.
  Supported formats are:

  * Delimiter-separated-values - Works best when the number of columns is
    constant.
  * Fixed-width values - For blank padded values only. Individual columns
    can be left or right adjusted (but not both on the same column).
  * Non tabulated formats - JSON and XML only.
  * Default - If all else failed, a single column is assumed.

* [New] 1.2.3-5: |<br>|
  Data format auto detection ("``-f,auto``") supports HTML Table format data.
  Manual selection also supported via "``-f,tab``".

* [New] 1.2.3-5: |<br>|
  New options that affect aq_tool related information:

  * ``-o_pp_atr File`` - Output attributes for aq_tool's "``-f``" option.
    For example, a dataset in HTML Table format will have an attribute of
    "``,tab``".
  * ``-pp_eok Percent`` - Set the acceptable error threshold percentage.
    It affects the aq_tool column type selection. For example, if 0.5% of
    a certain column has string type and the other 99.5% has interger type,
    the column type selected for aq_tool will be string; however, if the
    threshold is set to greater than 0.5, then integer will be selected.
    A non-zero threshold also adds a "``,eok``" to "``-o_pp_atr``"'s output.


logcnv
======

* [Warn] 1.2.3-1: |<br>|
  ``logcnv`` shall be retired in the next release. Please do not use it
  in your applications. Its functionality is now supported by all ``aq_*``
  commands. Its documentation has been removed.

  Old apps using ``logcnv`` can simply call ``aq_pp`` instead.
  No command option change is necessary except for the ``tim`` column
  attribute which is no longer supported. The function of this attribute
  can be reproduced by saving the column as a string and then use
  ``-eval i:time 'DateToTime(time_str, "d.b.Y.H.M.S.z")'`` to do the
  time conversion.


jsncnv
======

* [Critical] 1.2.3-3: |<br>|
  ``jsncnv`` has been replaced with a new `objcnv`_ command.
  Old apps using ``jsncnv`` should be able to call ``objcnv -jsn ...``
  instead.


objcnv
======
Cf: `objcnv <objcnv.html>`_

* [New] 1.2.3-3: |<br>|
  ``objcnv`` is a new command that replaces the functionality of the old
  ``jsncnv`` along with an added XML support. Which parsing mode to use
  must be specified on the command:

  * ``-jsn`` - JSON mode.
  * ``-xml`` - XML mode.

  In other words, old apps using ``jsncnv`` should call ``objcnv -jsn ...``
  instead.

  ``objcnv`` differs from ``jsncnv`` in its ability to output all array
  elements (i.e., "[*]") instead of one selected element (i.e., "[Num]").
  In additon, ``objcnv`` can handle nested arrays so that it can output
  all combination of all array elements to individual rows.

* [Critical] 1.2.3-3: |<br>|
  There is one feature in the old ``jsncnv`` that is not supported by
  ``objcnv`` - it is no longer possible to extract a particular array element
  by its array index (e.g., "key1.key2[5]") and use it as a column value.
  Instead, ``objcnv`` only supports "[*]", meaning that ALL array elements
  are extracted, with one element per row.


mcc.pmod
========
Cf: `mcc.pmod <mcc.pmod.html>`_

* [New] 1.2.3-1: |<br>|
  Module script compiler for ``aq_pp``'s processing module. It is mainly
  used internally by ``aq_pp``. It can also be invoked manually to aid
  module development.

  This is a new tool. See its manual page for details.

* [Critical] 1.2.3-6: |<br>|
  Changed a few module command names. For now, the compiler will try to convert
  the code automatically, but new code should use the new names.

  * ``MOD_LANG()`` -> ``DECL_LANG()``
  * ``MOD_COLUMN()`` -> ``DECL_COLUMN()``
  * ``MOD_COLUMN_DYNAMIC()`` -> ``DECL_COLUMN_DYNAMIC()``

* [New] 1.2.3-6: |<br>|
  Extensions:

  * ``DECL_BUILD_OPT()`` (new) specifies the build (compile+link) options
    such as include paths, required libraries, and so on.
  * DECL_COLUMN_DYNAMIC() (old MOD_COLUMN_DYNAMIC) can take a column *array*.
    Individual columns can then be addressed using an index. Example,

    ::

      DECL_COLUMN_DYNAMIC(myTab.col[MAX_NEEDED], I);
      ...
      for (i = 0; i < arg_n; ++i) {
        MOD_COLUMN_BIND(myTab.col[i], arg[i]);
        $myTab.col[i] = 0;
      }

  * ``DECL_DATA()`` - A new construct for the declaration of
    *instance specific* module variables. The use of *global* variables in a
    module is *not* recommended.
  * ``MOD_DATA()`` - Accesses a previously declared *instance specific*
    module variable.


mcc.umod
========
Cf: `mcc.umod <mcc.umod.html>`_

* [New] 1.2.3-1: |<br>|
  Module script compiler for Udb's runtime modules. It is mainly
  used internally by ``aq_udb``. It can also be invoked manually to aid
  module development.

  This is a new tool. See its manual page for details.

* [New] 1.2.3-2: |<br>|
  Completed import processing support for module scripts.

* [Critical] 1.2.3-6: |<br>|
  Changed a few module command names. For now, the compiler will try to convert
  the code automatically, but new code should use the new names.

  * ``MOD_LANG()`` -> ``DECL_LANG()``
  * ``MOD_COLUMN()`` -> ``DECL_COLUMN()``
  * ``MOD_COLUMN_DYNAMIC()`` -> ``DECL_COLUMN_DYNAMIC()``
  * ``MOD_TABLE_ROW()`` -> ``MOD_ROW()``

* [New] 1.2.3-6: |<br>|
  Extensions:

  * ``DECL_BUILD_OPT()`` (new) specifies the build (compile+link) options
    such as include paths, required libraries, and so on.
  * DECL_COLUMN_DYNAMIC() (old MOD_COLUMN_DYNAMIC) can take a column *array*.
    Individual columns can then be addressed using an index. Example,

    ::

      DECL_COLUMN_DYNAMIC(myTab.col[MAX_NEEDED], I);
      ...
      for (i = 0; i < arg_n; ++i) {
        MOD_COLUMN_BIND(myTab.col[i], arg[i]);
        $myTab.col[i] = 0;
      }

  * ``DECL_DATA()`` (new) declares *instance specific* module variables.
    The use of *global* variables in a module is *not* recommended.
  * ``MOD_DATA()`` accesses a previously declared *instance specific*
    module variable.
  * ``MOD_ROW_COUNT()`` (new) returns the row count of a table.
  * ``MOD_ERR_LOG()`` (new) specifically logs an error that can be passed back
    to the client (``aq_pp``/``aq_udb``) if it is called during module
    initialization.

