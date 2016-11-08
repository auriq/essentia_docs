.. |<br>| raw:: html

   <br>

===================
Change Log - V1.2.4
===================

:Replaces: V1.2.3
:Revision: V1.2.4-0 2016-03-10
:Revision: V1.2.4-1 2016-06-28
:Revision: V1.2.4-2 2016-08-09
:Revision: V1.2.4-3 2016-09-06
:Revision: V1.2.4-4 2016-09-29
:Revision: V1.2.4-5 2016-10-26
:Revision: V1.2.4-6 2016-11-03


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

New features:

* ``aq_pp`` can take data from Udb as its input as in
  ``aq_pp -exp Udb_export_options -- ...`` where the standard ``-f`` option
  has been replaced by a set of Udb export options.
* aq_tool can take input in JSON, XML and generic separator delimited formats
  with ``-f,jsn``, ``-f,xml`` and ``-f,div`` respectively.
* aq_tool can output in JSON format with ``-o,jsn``.
* aq_tool can pass column spec from one command to another. For
  example, in ``aq_command ... -o,aq - -c c3 c9 c1 | aq_command -f,aq - ..``,
  no column spec is needed in the second command.
* Output columns specified under ``-c`` can be negated. For example,
  ``-c ~c5 ~c8`` will *exclude* ``c5`` and ``c8``.
* Output columns specified under ``-c`` can have a format spec as in
  ``-d ... i:c1 ... -c c1+0x%x``. For numeric columns only.
* New regular expression based functions - e.g., ``RxReplace()``
  is designed to perform generic substring replacement.
* Udb can accept any primary key data type, not just string.
* Udb can take a composite primary key (a multi-column key).
* Udb can be a key-only database with no table/vector.
* Database definition can be created with ``aq_udb -crt ...`` without importing.
* Udb data rows and keys can be removed with ``-del_row`` and ``-del_key``
  during an ``aq_udb`` export/count/scan operation.
* A single Udb server can manage multiple databases.
  The old port-based database requirement is no longer necessary.

Incompatible changes:

* ``-f File1 File2 ... -f File3 ...`` --> ``-f File1 File2 File3 ... ...``
* ``-o File -notitle`` --> ``-o,notitle File``
* ``-evlc`` --> ``-eval``
* ``-f,noq`` --> ``-f,sep=,`` (add ``esc`` as needed)
* ``-o,noq`` --> ``-o,sep=,`` (add ``esc`` as needed)
* ``-f ... -d s:c1 s,noq:c2 ...`` --> ``-f,div`` with custom separator specs
* ``-maprx ...`` --> ``-map,rx ...``
* ``-mapfrx ...`` --> ``-mapf,rx ...``
* ``-imp ... -seg N1[-N2]/N`` --> ``-imp,seg=N1[-N2]/N ...``
* ``-imp ... -nobnk`` --> ``-imp,nobnk ...``
* ``-imp ... -nonew`` --> ``-imp,nonew ...``
* ``-exp_usr`` --> ``-exp DbName``
* ``-cnt_usr`` --> ``-cnt DbName``
* ``-scn_usr`` --> ``-scn DbName``
* ``-ord_all`` --> ``-ord DbName``
* ``-clr_all`` --> ``-clr DbName``
* ``-dec`` --> ``-ord,dec`` or ``-sort,dec``
* ``+add`` attribute cannot be used on a string column.
* ``aq_sess``, ``logcnv`` and ``objcnv`` have been removed from the package.
* Udb related documentation now uses the word "key" in place of "user" or
  "bucket".

Changes to be enforced in a future release:

* ``-udb ... -imp ...`` --> ``-imp[,AtrLst] ...`` (``-udb`` not needed)
* ``-ddef ... -imp ...`` --> ``-imp,ddef ...``
* ``-map``, ``-mapf`` and ``-mapc`` --> ``RxMap()`` function
* ``-kenc`` and ``-kdec`` --> ``KeyEnc()`` and ``KeyDec()`` functions
* ``KDec()`` --> ``KeyDec()``
* ``QryParmExt()`` --> ``QryDec()``
* ``-pp ... -end_of_scan DestSpec ...`` --> ``-pp,post=DestSpec ...``
* ``-lim_usr`` --> ``-lim_key``
* ``next_bucket`` and ``proc_bucket`` --> ``next_key`` and ``proc_key``


Common
======
Cf: `aq_cat <aq_cat.html>`_, `aq_cnt <aq_cnt.html>`_, `aq_ord <aq_ord.html>`_, `aq_pp <aq_pp.html>`_, `aq_udb <aq_udb.html>`_, etc.

* [Critical] 1.2.4-1/3: |<br>|
  Some depreciated options no longer supported. Use the newer specs:

  * ``-o File -notitle`` --> ``-o,notitle File``
  * ``-evlc`` --> ``-eval``

* [Critical] 1.2.4-1: |<br>|
  The ``-bz`` option has been replaced by an ``bz=BufSize`` attribute of the
  ``-f`` option. In fact, each input related option can have its own
  ``bz`` attribute. This option is rarely needed since the default is usually
  sufficient.

  * ``-bz 100 -f File`` --> ``-f,bz=100 File``

* [Critical] 1.2.4-1: |<br>|
  Some aspects of the ``-f`` (input source) option have changed. They were
  changed to accommodate several new features.

  * Multiple ``-f`` no longer supported. All inputs must be specifed under the
    same ``-f`` option. That is,

    * ``-f File1 File2 ... -f File3 ...`` --> ``-f File1 File2 File3 ... ...``

  * ``-f`` should be specified *before* any ``-d`` (column spec) options.
    This is because column spec interpretation may depend on the data format
    chosen in the ``-f`` attributes.  For example, JSON and XML formats
    require extended column specs.

  * A ``div`` attribute is required to process data in the old ``logcnv``'s
    format. That is,

    * ``-f ... -d ... SEP:"sep1" ...`` --> ``-f,div ... -d ... SEP:"sep1" ...``

* [Critical] 1.2.4-1: |<br>|
  The ``noq`` attribute of ``-f``, ``-o`` and individual column spec has been
  removed because it produces the wrong result on CSV data. Use one of these
  approaches instead:

  * ``-f,noq`` --> ``-f,sep=,`` (add ``esc`` as needed)
  * ``-o,noq`` --> ``-o,sep=,`` (add ``esc`` as needed)
  * ``-f ... -d s:c1 s,noq:c2 ...`` --> ``-f,div`` with custom separator specs

* [Warn] 1.2.4-1: |<br>|
  The error messages of most commandline option/parameter specification errors
  have changed.

* [New] 1.2.4-1/2: |<br>|
  New input option attributes (apply to options like ``-f``, ``-cat``,
  ``-sub`` and so on):

  * ``jsn`` - Input is in JSON format.
  * ``xml`` - Input is in XML format.
  * ``aq`` - The input is generated by another aq_tool outputting in ``aq``
    format. This is a special format that contains an embedded column spec.
    For this reason, *no* column spec is needed (nor accepted).
  * ``div`` - Select a format that used to be handled by ``logcnv``.
  * ``bz=BufSize`` - Replaces the old ``-bz`` option.
  * ``nox`` - Reject records with more fields than the column spec.
    For separator delimited format and HTML table format only.
  * ``eok[=Num[/Rows]]`` - New optional parameter ``Num`` or ``Num/Rows``.
    ``Num`` sets the number of errors per file to allow.
    ``Num/Rows`` allows ``Num`` errors every ``Rows`` rows.
  * ``qui[=Num]`` - New optional parameter ``Num``. It sets the number of
    error messages to print for each input file before becoming quiet.

* [New] 1.2.4-1: |<br>|
  New output option attributes (apply to options like ``-o``, ``-ovar``
  and so on):

  * ``aq`` - Output using an internal binary output format.
  * ``jsn`` - Output each record as an JSON object.
  * ``nodelay`` - Output each record as soon as possible instead of
    waiting until the output buffer is full.

* [New] 1.2.4-1/5: |<br>|
  New evaluation functions:

  * ``RxCmp()`` works like ``PatCmp()`` with a RegEx attribute.
  * ``RxMap()`` works like the ``-map,rx`` and ``-mapf,rx`` options.
  * ``RxReplace()`` is a pattern replacement function.
  * ``StrIndex()`` finds the position of a substring in another string.
  * ``QryDec()`` works like the the old ``QryParmExt()`` function
    but with a revised argument schematics.
  * ``KeyEnc()`` and ``KeyDec()`` works like the ``-kenc`` and
    ``-kdec`` options.
  * ``UrlDec()`` and ``Base64Dec()`` are Web related decoding functions.
  * ``ToUpper()`` and ``ToLower()`` are simple ASCII test conversion functions.
  * ``Set()`` sets a column's value. Unlike a standard ``-eval``, the target
    column here is determined at runtime during each evaluation (it is taken
    from a string argument).

* [New] 1.2.4-4: |<br>|
  Output column selection (``-c``) can accept columns *not* to include.
  For example, ``-c ~c5 ~c8`` will remove ``c5`` and ``c8`` from the default
  output column set.

* [New] 1.2.4-4: |<br>|
* Output columns specified under ``-c`` can have a format spec as in
  ``-d ... i:c1 ... -c c1+0x%x``. For numeric columns only. Everything
  following the ``+`` (plus sign) is a format string that will be passed to
  the C library's ``printf`` function. The user must specify the right format;
  otherwise, the program may crash.

  Note: This is an experimental option. It will not be documented
  until its design and usability have been confirmed.


aq_pp
=====
Cf: `aq_pp <aq_pp.html>`_

* See also `common`_ changes.

* [Critical] 1.2.4-1: |<br>|
  The ``-maprx`` and ``-mapfrx`` options are no longer supported. Use the
  ``rx`` attribute instead:

  * ``-maprx ...`` --> ``-map,rx ...``
  * ``-mapfrx ...`` --> ``-mapf,rx ...``

  Furthermore, the mapping related options will be depreciated soon.
  Use the new ``RxMap()`` function instead.

* [Critical] 1.2.4-1: |<br>|
  Several Udb import related commandline options have changed:

  * ``-spec SpecFile -imp TabName`` --> ``-imp,spec=SpecFile DbName:TabName``
  * ``-db DbName -imp TabName`` --> ``-imp DbName:TabName``
  * ``-imp ... -seg N1[-N2]/N`` --> ``-imp,seg=N1[-N2]/N ...``
  * ``-imp ... -nobnk`` --> ``-imp,nobnk ...``
  * ``-imp ... -nonew`` --> ``-imp,nonew ...``

* [Warn] 1.2.4-1: |<br>|
  The ``-udb`` option is depreciated. The extended ``-imp`` option alone
  is sufficient.

  * ``-udb ... -imp ...`` --> ``-imp[,AtrLst] ...``

* [Warn] 1.2.4-1: |<br>|
  The ``-ddef`` option is depreciated. Use the new ``ddef`` attribute on
  ``-imp`` instead:

  * ``-ddef ... -imp ...`` --> ``-imp,ddef ...``

* [New] 1.2.4-1/3: |<br>|
  The ``-imp`` (Udb import) option can now have attributes, as in
  ``-imp[,AtrLst]``:

  * ``spec=SpecFile``, ``seg=N1[-N2]/N``, ``nobnk``, ``nonew``, ``ddef`` -
    They replace the old ``-spec``, ``-seg``, ``-nobnk``, ``-nonew`` and
    ``-ddef``  options respectively.
  * ``noold`` - Only import to *new* keys. It is the opposite of ``nonew``.
  * ``nodelay`` - Sent each record to Udb as soon as possible instead of
    waiting until the output buffer is full.

* [New] 1.2.4-1: |<br>|
  ``aq_pp`` can now obtain its main input from an Udb export. To do this,
  use the new ``-exp Udb_export_options --`` spec instead of a ``-f``.
  ``Udb_export_options`` represents any of the export related options of
  `aq_udb <aq_udb.html>`_ (other than the ``-o`` output option). The ``--``
  indicates the end of the export spec.

* [New] 1.2.4-1: |<br>|
  Additonal information is now available at the end of an Udb import:

  * Successful - ``aq_pp`` will show the combined server
    memory usage if ``-stat`` is enabled. Per server usages can be obtained
    with ``-verb``.
  * Failure - ``aq_pp`` will show an error message from each failed server.

* [New] 1.2.4-2: |<br>|
  Added license file checks:

  * ``/opt/essentia/essentia.license``
  * ``/opt/essentia/essentia.sign``


aq_ord
======
Cf: `aq_ord <aq_ord.html>`_

* See also `common`_ changes.

* [Bug] 1.2.4-2: |<br>|
  Wrong result when sorting certain string value combinations.

* [Critical] 1.2.4-1: |<br>|
  A depreciated option has been removed:

  * ``-dec`` --> ``-sort,dec``


aq_udb/udb server
=================
Cf: `aq_udb <aq_udb.html>`_, `udbd <udbd.html>`_

* See also `common`_ changes.

* [Bug] 1.2.4-1: |<br>|
  ``udbd`` (script) has a hardcoded limit on the number of Udb servers it
  would handle. This limit was set too low (32). Extended it yto 70.
  Note that this is only a soft limit. To manage more servers,
  run ``udbd`` several times, each time on a different range of ports.

* [Bug] 1.2.4-1: |<br>|
  Any Udb action *immediately* following a broken pipe may produce
  unpredictable result. An example is:

  ::

    $ aq_udb -exp mydb:mytable | head -1 ; aq_udb -exp mydb:mytable

  The ``head`` command will cause a broken pipe; for this reason, the second
  export may not produce the correct result.

* [Bug] 1.2.4-2: |<br>|
  When a Udb module source is supplied with the ``aq_udb`` or ``aq_pp``
  command, the resulting module will get truncated if it is greater than 64K
  byte in size (the truncated size can be less than 64K).

* [Bug] 1.2.4-6: |<br>|
  The server normally writes log/error messages to a log file. If the server
  cannot open the file (e.g., due to file permission problem), the old
  behavior was to ignore the error and log to stdout/stderr implicitly.
  But this caused a problem when the server was being started by a
  ``ssh`` command - the command will not exit until the server closes
  stdout/stderr. The new behavior is to print an error message and quit.

* [Critical] 1.2.4-1: |<br>|
  The action specification option - ``-exp``, ``-cnt``, ``-scn``, ``-ord``,
  ``-clr`` and ``-probe`` - must be specified *before* options that depend
  on it. For example, ``-sort`` is only valid for export,
  so an ``-exp`` must be given first. If in doubt, follow the
  `aq_udb <aq_udb.html>`_ synopsis.

* [Critical] 1.2.4-1: |<br>|
  Some depreciated options no longer supported. Use the newer specs:

  * ``-spec SpecFile -Action TabName`` --> ``-Action,spec=SpecFile DbName:TabName``
  * ``-db DbName -Action TabName`` --> ``-Action DbName:TabName``
  * ``-exp_usr`` --> ``-exp DbName`` or ``-exp,spec=SpecFile DbName``
  * ``-cnt_usr`` --> ``-cnt DbName`` or ``-cnt,spec=SpecFile DbName``
  * ``-scn_usr`` --> ``-scn DbName`` or ``-scn,spec=SpecFile DbName``
  * ``-ord_all`` --> ``-ord DbName`` or ``-ord,spec=SpecFile DbName``
  * ``-clr_all`` --> ``-clr DbName`` or ``-clr,spec=SpecFile DbName``
  * ``-dec`` --> ``-ord,dec`` or ``-sort,dec``

* [Critical] 1.2.4-1: |<br>|
  The ``-probe`` (server check) option now *requires* a parameter:

  * ``-spec SpecFile -probe`` --> ``-probe,spec=SpecFile DbName``

* [Critical] 1.2.4-2: |<br>|
  The ``-sort`` (output sorting) option now *requires* a sort column spec.

* [Critical] 1.2.4-5: |<br>|
  Removed ``+add`` attribute support on string columns.

* [Warn] 1.2.4-1: |<br>|
  Output column labels in the title line have changed. This only happens when
  the columns come from more than one source. For example, if table colums are
  exported along with vector columns and var columns, the labels will appear
  like this:

  ::

    "col1","col2","vectorX.col1","vectorX.col2","var.col1","var.col2"

  In older versions, the labels would be indistinguishable:

  ::

    "col1","col2","col1","col2","col1","col2"

* [Warn] 1.2.4-3: |<br>|
  The ``-end_of_scan DestSpec`` option for ``-pp`` is depreciated.
  Use the new ``post`` attribute on ``-pp`` instead:

  * ``-pp ... -end_of_scan DestSpec ...`` --> ``-pp,post=DestSpec ...``

* [New] 1.2.4-1: |<br>|
  The ``-probe`` (server check) option will show the combined server
  memory usage if ``-stat`` is enabled. Per server usages can be obtained
  with ``-verb``.

* [New] 1.2.4-2: |<br>|
  Per key row count of a table can be obtained from the new
  ``RowCount(TabName)`` evaluation function.
  The count is stored as part of the key specific data, no row scan is involved.
  For vectors where the row count is always 1, the function returns 1
  if the row has been initialized, 0 otherwise.

* [New] 1.2.4-2: |<br>|
  The Udb primary key has been generalized:

  * It can have an arbitrary data type, not just string.
  * It can be a composite key, one made up of multiple columns of arbitrary
    data types.

* [New] 1.2.4-2: |<br>|
  Each Udb server can now handle more than one databases at a time.
  Databases are identified by their names. Their data are
  stored independently. But they share a common string hash for efficiency.
  The database name is obtained from the commandline - e.g., ``mydb`` will
  be the database name in these commands:

  ::

    $ aq_pp ... -imp mydb:mytable ...
    $ aq_udb -exp mydb:mytable ...

* [New] 1.2.4-2: |<br>|
  ``udbd`` will apply a default memory limit of ``(SystemTotal - 500M)`` when
  starting Udb servers. This can be overriden with the ``-mem`` or ``-memx``
  option of ``udbd``.

* [New] 1.2.4-3: |<br>|
  Support explicit DB creation with the new ``-crt`` ``aq_udb`` option.

* [New] 1.2.4-3: |<br>|
  Support key-only import, no table/vector data needed.
  This is useful for a DB that has *no* table or vector.
  Example usage:

  ::

    $ aq_pp ... -imp mydb ...
    $ aq_udb -exp mydb ...

* [New] 1.2.4-3: |<br>|
  Delete is now supported during an export/scan/count operation.

  * ``-del_row`` will delete the current row.
  * ``-del_key`` will delete the current key and its associated data.


aq_sess
=======

* [Critical] 1.2.4-1: |<br>|
  ``aq_sess`` has been retired.


logcnv
======

* [Critical] 1.2.4-1: |<br>|
  ``logcnv`` has been retired. Its functionality is now supported by all
  ``aq_*`` commands. Use the ``div`` input attribute to enable it.
  For example,

  * ``logcnv -f[,AtrLst] ...`` --> ``aq_pp -f,div[,AtrLst] ...``


loginf
======

* [Bug] 1.2.4-5: |<br>|
  Fixed ``loginf`` crash that happens when any record from the log is greater
  than 64KB long.


objcnv
======

* [Critical] 1.2.4-1: |<br>|
  ``objcnv`` has been retired. Its functionality is now supported by all
  ``aq_*`` commands. Use the ``jsn`` or ``xml`` input attribute to enable it.
  For example,

  * ``objcnv -jsn -f[,AtrLst] ...`` or ``objcnv -f,jsn[,AtrLst] ...`` -->
    ``aq_pp -f,jsn[,AtrLst] ...``

