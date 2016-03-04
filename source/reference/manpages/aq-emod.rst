=======
aq-emod
=======

aq_tool eval functions


Description
===========

Functions for use in the evaluation and filtering expressions in
the `aq_pp <aq_pp.html>`_ and `aq_udb <aq_udb.html>`_ commands.


Synopsis
========

 ::

  aq_command ... -eval ColName '... Func(arg, ...) ...'


General purpose functions
=========================

``ToIP(Val)``

* Returns the IP address value of ``Val``.
* ``Val`` can be a string/IP column's name, a `string constant`_,
  or an expression that evaluates to a string/IP.

  Example:

   ::

    $ aq_command ... -eval IP_Col 'ToIP("1.2.3.4")' ...
    $ aq_command ... -eval IP_Col 'ToIP(String_Col)' ...

``ToF(Val)``

* Returns the floating point value of ``Val``.
* ``Val`` can be a string/numeric column's name, a string/numeric constant,
  or an expression that evaluates to a string/number.

  Example:

   ::

    $ aq_command ... -eval Float_Col 'ToF("0.1234")' ...
    $ aq_command ... -eval Float_Col 'ToF(String_Col)' ...

``ToI(Val)``

* Returns the integral value of ``Val``.
* ``Val`` can be a string/numeric column's name, a string/numeric constant,
  or an expression that evaluates to a string/number.

  Example:

   ::

    $ aq_command ... -eval Integer_Col 'ToI("1234")' ...
    $ aq_command ... -eval Integer_Col 'ToI(String_Col)' ...

``ToS(Val)``

* Returns the string representation of ``Val``.
* ``Val`` can be a numeric column's name, a string/numeric/IP constant,
  or an expression that evaluates to a string/number/IP.

  Example:

   ::

    $ aq_command ... -eval String_Col 'ToS(1234)' ...
    $ aq_command ... -eval String_Col 'ToS(Integer_Col)' ...
    $ aq_command ... -eval String_Col 'ToS(1.2.3.4)' ...
    $ aq_command ... -eval String_Col 'ToS(IP_Col)' ...

``Min(Val1, Val2 [, Val3 ...])``

* Returns the smallest among ``Val1``, ``Val2`` and so on.
* Each value can be a numeric column's name, a number,
  or an expression that evaluates to a number.
* If all values are integers, the result will also be an integer.
* If *any* value is a floating point number, the result will be a floating
  point number.

  Example:

   ::

    $ aq_command ... -eval Float_Col 'Min(1, Integer_Col, Float_Col)' ...
    $ aq_command ... -eval Integer_Col 'Min(ToI(String_Col), Float_Col)' ...

``Max(Val1, Val2 [, Val3 ...])``

* Returns the greatest among ``Val1``, ``Val2`` and so on.
* Each value can be a numeric column's name, a number,
  or an expression that evaluates to a number.
* If all values are integers, the result will also be an integer.
* If *any* value is a floating point number, the result will be a floating
  point number.

  Example:

   ::

    $ aq_command ... -eval Float_Col 'Max(1, Integer_Col, Float_Col)' ...
    $ aq_command ... -eval Integer_Col 'Max(ToI(String_Col), Float_Col)' ...

``PatCmp(Val, Pattern [, AtrLst])``

* Performs a pattern comparison between string value and a pattern.
* Returns 1 (True) if successful or 0 (False) otherwise.
* ``Val`` can be a string column's name, a `string constant`_,
  or an expression that evaluates to a string.
* ``Pattern`` is a `string constant`_ specifying
  the pattern to match.
* Optional ``AtrLst`` is a comma separated string list containing:

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

  Example:

   ::

    $ aq_command ... -filt 'PatCmp(String_Col, "* ABC *")' ...
    $ aq_command ... -filt 'PatCmp(String_Col, "* \"ABC\" *")' ...
    $ aq_command ... -filt 'PatCmp(String_Col, "* \"\\\\ & \\*\" *")' ...

  * The first example selects values containing a basic literal " ``ABC`` ".
  * The second example selects values containing a literal " ``"ABC"`` ".
    To specify this as a *double quoted* `string constant`_,
    the quotes must be escaped,
    resulting in " ``\"ABC\"`` ".
  * The third example selects values containing a literal " ``"\ & *"`` ".
    This literal contains special pattern characters "``\``" and "``*``"
    that must be escaped, so the desire pattern is " ``"\\ & \*"`` ".
    Finally, to specify this as a *double quoted* `string constant`_,
    the quotes and backslashes must be escaped,
    resulting in " ``\"\\\\ & \\*\"`` ".

``SHash(Val)``

* Returns the numeric hash value of a string.
* ``Val`` can be a string column's name, a `string constant`_,
  or an expression that evaluates to a string.

  Example:

   ::

    $ aq_command ... -filt 'SHash(String_Col) % 10 == 0' ...

  * A way to sample 1/10th of ``String_Col``'s unique values.

``SLeng(Val)``

* Returns the length of a string.
* ``Val`` can be a string column's name, a `string constant`_,
  or an expression that evaluates to a string.

  Example:

   ::

    $ aq_command ... -eval Integer_Col 'SLeng(String_Col)' ...
    $ aq_command ... -filt 'SLeng(String_Col) < 10' ...

``SubStr(Val, Start [, Length])``

* Returns a substring of a string.
* ``Val`` can be a string column's name, a `string constant`_,
  or an expression that evaluates to a string.
* ``Start`` is the starting position (zero-based) of the substring in ``Val``.
  It can be a numeric column's name, a number,
  or an expression that evaluates to a number.
  If ``Start`` is negative, the length of ``Val`` will be added to it.
  If it is still negative, 0 will be used.
* Optional ``Length`` specifies the length of the substring in ``Val``.
  It can be a numeric column's name, a number,
  or an expression that evaluates to a number.
  Max length is length of ``Val`` minus ``Start``.
  If ``Length`` is not specified, max length is assumed.
  If ``Length`` is negative, max length will be added to it.
  If it is still negative, 0 will be used.

  Example:

   ::

    $ aq_command ... -eval String_Col 'SubStr(Str2, SLeng(Str2) - 2, 1)' ...
    $ aq_command ... -eval String_Col 'SubStr(Str2, -2, 1)' ...

  * These yield the same result.

``ClipStr(Val, ClipSpec)``

* Returns a substring of a string.
* ``Val`` can be a string column's name, a `string constant`_,
  or an expression that evaluates to a string.
* ``ClipSpec`` is a `string constant`_ specifying
  how to *clip* the substring from the source.
  It is a sequence of individual clip elements separated by "``;``":

   ::

    [!]Num[-]Dir[Sep][;[!]Num[-]Dir[Sep]...]

  Each clip elements exacts either the starting or trailing portion of the
  source. The first element clips the input ``Val``, the second element clips
  the result from the first, and so on.
  The components in a clip element are:

  * ``!`` - The negation operator inverts the result of the clip.
    In other words, if the original clipped result is the starting portion of
    the source, negating that gives the tailing portion.
  * ``Num`` - The number of bytes or separators (see ``Sep`` below)
    to  clip.
  * ``-`` (a dash) - Do not include the *last* separator (see ``Sep`` below)
    in the result.
  * ``Dir`` - The clip direction. Specify a "``>``" to clip from the beginning
    to the end. Specify a "``<``" to clip backward from the end to the
    beginning.
  * ``Sep`` - Optional single byte clip separator. If given, a substring
    containing up to (and including, unless a "``-``" is given) ``Num``
    separators will be clipped in the ``Dir`` direction.
    If no separator is given, ``Num`` bytes will be clipped in the the same
    way.

* Do not put a "``;``" at the end of ``ClipSpec``. The reason is that it
  could be misinterpreted as the ``Sep`` for the last clip element.

  Example:

   ::

    $ aq_command ... -eval String_Col 'ClipStr(Str2, "2>/")' ...

  * Clips up to and including the 2nd "``/``" from ``Str2``. That is, if
    ``Str2`` is "``/A/B/C``", then the result will be "``/A/``".

``DateToTime(DateVal, DateFmt)``, ``GmDateToTime(DateVal, DateFmt)``

* Both functions return the UNIX time in integral seconds corresponding to
  ``DateVal``.
* ``DateVal`` can be a string column's name, a `string constant`_,
  or an expression that evaluates to a string.
* ``DateFmt`` is a `string constant`_ specifying
  the format of ``DateVal``.
  The format is a sequence of conversion codes:

  * (a dot) ``.`` - represent a single unwanted character (e.g., a separator).
  * ``%Y`` - 1-4 digit year.
  * ``%y`` - 1-2 digit year.
  * ``%m`` - month in 1-12.
  * ``%b`` - abbreviated English month name ("JAN" ... "DEC", case
    insensitive).
  * ``%d`` - day of month in 1-31.
  * ``%H`` or ``%I`` - hour in 0-23 or 1-12.
  * ``%M`` - minute in 0-59.
  * ``%S`` - second in 0-59.
  * ``%p`` - AM/PM (case insensitive).
  * ``%z`` - offset from GMT in the form [+|-]HHMM.

* If ``DateVal`` contains GMT offset information (``%z`` info),
  the UNIX time will be calculated using this offset.
  Both ``DateToTime()`` and ``GmDateToTime()`` will return the same result.
* If there is no GMT offset, ``DateToTime()`` will return a UNIX time
  based on the program's default timezone (set the program's timezone,
  e.g, via the TZ environment, before execution if necessary),
  while ``GmDateToTime()`` will return a UNIX time based on GMT.

  Example:

   ::

    $ aq_command ... -eval Integer_Col 'DateToTime(Str2, "%Y.%m.%d.%H.%M.%S.....%z")' ...

  * This format is designed for a date string (``Str2``) like
    "``1969-12-31 16:00:01.123 -0800``". Note the use of extra dots in the
    format to map out the unwanted "``.123``".

``TimeToDate(TimeVal, DateFmt)``, ``TimeToGmDate(TimeVal, DateFmt)``

* Both functions return the date string corresponding to ``TimeVal``.
  The result string's maximum length is 127.
* ``TimeVal`` can be a numeric column's name, a numeric constant,
  or an expression that evaluates to a number.
* ``DateFmt`` is a `string constant`_ specifying
  the format of the output. See the ``strftime()`` C function manual
  page regarding the format of ``DateFmt``.
* The ``TimeToDate()`` conversion is timezone dependent.
  It is done using the program's default timezone.
  Set the program's timezone, e.g, via the TZ environment, before execution
  if necessary.
* The ``TimeToGmDate()`` conversion always gives a date in GMT.

  Example:

   ::

    $ aq_command ... -eval String_Col 'TimeToDate(Int2, "%Y-%m-%d %H:%M:%S %z")' ...

  * Outputs date in "``1969-12-31 16:00:01 -0800``" format.

``QryParmExt(QryVal, ParmSpec)``

* Extracts query parameters from ``QryVal`` and place the results in columns.
* Returns the number of parameters extracted.
  (If the return value is not needed, invoke the function using
  ``-eval - QryParmExt(...)``.)
* ``QryVal`` can be a string column's name, a `string constant`_
  or an expression that evaluates to a string.
* ``ParmSpec`` is a `string constant`_ specifying
  the parameters to extract and the destination columns for the result.
  It has the general form:

   ::

    [AtrLst]&Key[:ColName][,AtrLst][&Key[:ColName][,AtrLst]...]

  At the beginning is an optional comma separated attribute list:

  * ``beg=c`` - Skip over the initial portion of QryVal up to and including
    the first 'c' character (single byte). A common value for 'c' is '?'.
    Without this attribute, the entire QryVal will be used.
  * ``zero`` - Zero out all destination columns before extraction.
  * ``dec=Num`` - Number of times to perform URL decode on the extracted
    values. Num must be between 0 and 99. Default is 1.
  * ``trm=c`` - Trim one leading and/or trailing 'c' character (single byte)
    from the decoded extracted values.

  A commonly used combination is ``beg=?,zero`` which processes the query
  portion of an URL and zero out all output columns before processing each
  URL in case certain parameters are not in the query.

  Following the optional attributes are the individual parameters to
  extract. Each extraction spec has the form:

   ::

    &Key[:ColName][,AtrLst]

  Each spec starts with an '&'.
  ``Key`` is the name of the parameter to extract.
  It should be URL encoded if it contains any special characters.
  The extracted value of Key is stored in a column given by ``ColName``.
  The column must be a previously defined column. If ``ColName`` is not
  given, a column with the same name as ``Key`` is assumed.
  Each spec can also have a comma separated attribute list:

  * ``zero`` - Zero out the destination column before extraction.
  * ``dec=Num`` - Number of times to perform URL decode on the extracted
    value of this Key. Num must be between 0 and 99.
  * ``trm=c`` - Trim one leading and/or trailing 'c' character (single byte)
    from the decoded extracted value.

  Example:

   ::

    $ aq_command ... -eval - 'QryParmExt(String_Col, "beg=?,zero&k1:Col1&k2:Col2")' ...

  * Extracts the values of "``k1``" and "``k2``" into columns ``Col1`` and
    ``Col2`` respectively from ``String_Col`` after the first "``?``".

``KDec(Key, DecSpec)``

* Decodes a key previously encoded via ``-kenc`` of `aq_pp <aq_pp.html>`_
  and place the results in columns according to ``DecSpec``.
* Returns the number of components in ``Key``.
  (If the return value is not needed, invoke function using
  ``-eval - KDec(...)``.)
* ``Key`` is the previously encoded value.
  It can be a string column's name, a `string constant`_
  or an expression that evaluates to a string.
* ``DecSpec`` is a `string constant`_ specifying
  how to decode ``Key``. It has the form:

   ::

    ColName;ColName[;ColName...]

  Each ``ColName`` specifies a decode-to column.
  The decode-to column types are very important - they must match those
  used in the original ``-kenc`` spec.
  If a decode-to component is not needed, specify ``ColType:`` (including
  the ":") in place of a ``ColName``.

  Example:

   ::

    $ aq_command ... -eval - 'KDec(String_Col, "Col1;Col2;S:")' ...

  * Extracts 3 encoded keys from ``String_Col``. The first 2 keys are to be
    saved in ``Col1`` and ``Col2``; the last is not needed, so only its type
    is specified.


Math functions
==============

These functions are implemented using the standard ``math`` library support.
More information on these functions are available from their individual
manpages (use the lower case function names).

``Ceil(Val)``

* Rounds ``Val`` up to the nearest integral value and returns the result.
* ``Val`` can be a numeric column's name, a numeric constant,
  or an expression that evaluates to a number.

``Floor(Val)``

* Rounds ``Val`` down to the nearest integral value and returns the result.
* ``Val`` can be a numeric column's name, a numeric constant,
  or an expression that evaluates to a number.

``Round(Val)``

* Rounds ``Val`` to the nearest integral value and returns the result.
  Half way cases are rounded *away* from zero.
* ``Val`` can be a numeric column's name, a numeric constant,
  or an expression that evaluates to a number.

``Abs(Val)``

* Computes the absolute value of ``Val`` and returns the result.
* ``Val`` can be a numeric column's name, a numeric constant,
  or an expression that evaluates to a number.

``IsNaN(Val)``

* Tests if ``Val`` is not-a-number.
* Returns 1 if true, 0 otherwise.
* ``Val`` can be a numeric column's name, a numeric constant,
  or an expression that evaluates to a number.

``IsInf(Val)``

* Tests if ``Val`` is infinite.
* Returns 1, -1 or 0 if the value is positive infinity, negative infinity or
  finite respectively.
* ``Val`` can be a numeric column's name, a numeric constant,
  or an expression that evaluates to a number.

``NumCmp(Val1, Val2, Delta)``

* Tests if ``Val1`` and ``Val2`` are within ``Delta`` of each other
  (i.e., whether ``Abs(Val1 - Val2) <= Delta``).
* Returns 1 if true, 0 otherwise.
* ``Val1``, ``Val2`` and ``Delta`` can be a numeric column's name,
  a numeric constant, or an expression that evaluates to a number.
* ``Delta`` should be greater than or equal to zero.


Character set encoding conversion functions
===========================================

These functions are implemented using the standard ``iconv`` library support.
Therefore, supported conversions are ``iconv`` dependent.
Run "``iconv --list``" to see the supported encodings.

``IConv(Val, FromCodes, ToCode)``

* Converts a string from one character set encoding to another.
* Returns the converted string if successful.
* ``Val`` can be a string column's name, a `string constant`_,
  or an expression that evaluates to a string.
* ``FromCodes`` is a `string constant`_ containing a semi-colon separated
  list of character sets to try to decode from -
  e.g., "``utf8;euc-jp;sjis``".
  If ``Val`` cannot be decoded using any of these encodings, the function
  will fail.
  If desired, add a "``.``" (a dot) to the end of the code list to tell the
  function to return ``Val`` as-is when none of the encodings match.
* ``ToCode`` is a `string constant`_ containing
  the character set to convert to - e.g., "``utf8``".

  Example:

   ::

    $ aq_command ... -eval String_Col 'IConv(Japanese_Col, "sjis;euc-jp;utf8", "utf8")' ...
    $ aq_command ... -eval String_Col 'IConv(Japanese_Col, "sjis;euc-jp;.", "utf8")' ...

  * Converts ``Japanese_Col`` from either SJIS or EUC into UTF8.
    The first example enforces that the result be UTF8.
    The second is more relaxed, its result may not be UTF8.


RT related functions
====================

These functions provide some of the *RTmetrics* capabilities.
They require some support files to operate. A set of default support
files are included with the aq_tool installation package.

``SearchKey(Site, Path)``, ``SearchKey(Url)``

* Extracts search key from the given site/path combination or URL.
  The extraction is done according to the rules in a search engine database
  supplied with the tool.
* Returns the extracted search key (string).

  * A blank is returned if the site is not a search engine.
  * A "-" is returned if the site is a search engine but there is no search key.

* ``Site``, ``Path`` and
  ``Url`` can be a string column's name, a `string constant`_
  or an expression that evaluates to a string.
* ``Site`` has the form "[http[s]://]site";
  ``Path`` has the form "/[path[?query]]".
* ``Url`` has the form "[http[s]://]site/[path[?query]]".

  Example:

   ::

    $ aq_command ... -eval String_Col 'SearchKey(Str2, Str3)' ...
    $ aq_command ... -eval String_Col 'SearchKey("www.google.com", "/search?q=Keyword")' ...
    $ aq_command ... -eval String_Col 'SearchKey(Str4)' ...
    $ aq_command ... -eval String_Col 'SearchKey("www.google.com/search?q=Keyword")' ...

``IpToCountry(Ip)``

* Looks up the given IP and return a "country_info[:region_info]" string.
  The string is a compact code suitable for data analysis.
  For reporting, use ``CountryName()`` and ``CountryRegion()`` to convert the
  code to names.
* ``Ip`` can be a IP column's name, a literal IP
  or an expression that evaluates to an IP.

  Example:

   ::

    $ aq_command ... -eval String_Col 'IpToCountry(IP_Col)' ...
    $ aq_command ... -eval String_Col 'IpToCountry(1.2.3.4)' ...

``CountryName(Code)``, ``CountryRegion(Code)``

* ``CountryName()`` returns the country name (string) corresponding to the
  country info in ``Code``.
* ``CountryRegion()`` returns the region name (string) corresponding to the
  region info in ``Code``.
  If ``Code`` does not contain any region info, a blank string is returned.
* ``Code`` can be a string column's name, a `string constant`_
  or an expression that evaluates to a string.
  It should contain a value previously returned from ``IpToCountry()``.

  Example:

   ::

    $ aq_command ... -eval String_Code_Col 'IpToCountry(IP_Col)' ...
        -eval String_Name_Col 'CountryName(String_Code_Col)' ...
        -eval String_Region_Col 'CountryRegion(String_Code_Col)' ...

``AgentParse(Agent [, Ip])``

* Parses the given user-agent string and returns a string of the following form:

  * "" (a blank) - No usable information was extracted.
  * "Browser:[OS]:[DeviveType]:[DeviceName]" - At least a browser name was
    extracted. The result contains up to four components. Use
    ``AgentName()``, ``AgentOS()``, ``AgentDevType()`` and ``AgentDevName()``
    to extract the desire components.
  * "Crawler" - A crawler signature was detected. The result is the crawler
    name. Use ``IsCrawler()`` to test if the result is a crawler.

* ``Agent`` can be a string column's name, a `string constant`_
  or an expression that evaluates to a string.
* ``Ip`` is an optional source IP for more accurate crawler matching.
  It can be an IP column's name, a literal IP
  or an expression that evaluates to an IP.

  Example:

   ::

    $ aq_command ... -eval String_Col 'AgentParse(Str2)' ...
    $ aq_command ... -eval String_Col 'AgentParse(Str2, IP2)' ...

``AgentName(Code)``, ``AgentOS(Code)``, ``AgentDevType(Code)``, ``AgentDevName(Code)``

* ``AgentName()`` returns the browser name (string) portion of ``Code``.
* ``AgentOS()`` returns the OS name (string) portion of ``Code``.
* ``AgentDevType()`` returns the device type (string) portion of ``Code``.
* ``AgentDevName()`` returns the device name (string) portion of ``Code``.
* ``Code`` can be a string column's name, a `string constant`_
  or an expression that evaluates to a string.
  It should contain a value previously returned from ``AgentParse()``.

  Example:

   ::

    $ aq_command ... -eval String_Code_Col 'AgentParse(Str2)' ...
        ... -eval String_Name_Col 'AgentName(String_Code_Col)' ...
        ... -eval String_OS_Col 'AgentOS(String_Code_Col)' ...
        ... -eval String_DevType_Col 'AgentDevType(String_Code_Col)' ...
        ... -eval String_DevName_Col 'AgentDevName(String_Code_Col)' ...

``IsCrawler(Code)``

* Checks if the given ``Code`` is a crawler and returns 1 if true, 0 otherwise.
* If true, ``Code`` will be the crawler name.
* ``Code`` can be a string column's name, a `string constant`_
  or an expression that evaluates to a string.
  It should contain a value previously returned from ``AgentParse()``.

  Example:

   ::

    $ aq_command ... -eval String_Code_Col 'AgentParse(Str2)' ...
        ... -eval Integer_Col 'IsCrawler(String_Code_Col)' ...

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


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udbd <udbd.html>`_ - Udb server
* `aq_udb <aq_udb.html>`_ - Udb server interface

