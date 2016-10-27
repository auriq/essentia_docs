.. |<br>| raw:: html

   <br>

=======
aq-emod
=======

aq_tool eval functions


Synopsis
========

::

  aq_command ... -eval ColName '... Func(arg, ...) ...'


Description
===========

Functions are designed to perform more complicated processings than what the
builtin evaluation and filtering operators provide. Supported fubnctions are:

* `String property functions`_
* `Math functions`_
* `Comparison functions`_
* `Data extraction and encode/decode functions`_
* `General data conversion functions`_
* `Date/Time conversion functions`_
* `Character set encoding conversion functions`_
* `Speciality functions`_
* `RTmetrics functions`_
* `Udb specific functions`_

They can be used in any evaluation and filtering expressions in
the `aq_pp <aq_pp.html>`_ and `aq_udb <aq_udb.html>`_ commands.
A function always returns a value. The value can either be the actual result
or a status code. In general,

* For functions that always succeed, their results are returned directly.
  For example, `Min()`_ returns the minimum value among its arguments,
  `ToS()`_ returns the string representation of its argument, etc.
* For functions that may fail, a numeric status code is returned.
  The code is usually 0 for a failured operation and non-zero otherwise.
  The code can also be a count that indicates the number of successful
  operations (e.g., `QryDec()`_).

If the return code is not needed, invoke the function this way:

 ::

   $ aq_command ... -eval - Func(...) ...


String property functions
=========================

.. _`SHash()`:

``SHash(Val)``
  Returns the numeric hash value of a string.

  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.

  Example:

   ::

    $ aq_command ... -filt 'SHash(String_Col) % 10 == 0' ...

  * A way to sample 1/10th of ``String_Col``'s unique values.

.. _`SLeng()`:

``SLeng(Val)``
  Returns the length of a string.

  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.

  Example:

   ::

    $ aq_command ... -eval Integer_Col 'SLeng(String_Col)' ...
    $ aq_command ... -filt 'SLeng(String_Col) < 10' ...


Math functions
==============

.. _`Ceil()`:

``Ceil(Val)``
  Rounds ``Val`` up to the nearest integral value and returns the result.

  * ``Val`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.

.. _`Floor()`:

``Floor(Val)``
  Rounds ``Val`` *down* to the nearest integral value and returns the result.

  * ``Val`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.

.. _`Round()`:

``Round(Val)``
  Rounds ``Val`` up/down to the nearest integral value and returns the result.
  Half way cases are rounded *away* from zero.

  * ``Val`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.

.. _`Abs()`:

``Abs(Val)``
  Computes the absolute value of ``Val`` and returns the result.

  * ``Val`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.

.. _`Min()`:

``Min(Val1, Val2 [, Val3 ...])``, ``Max(Val1, Val2 [, Val3 ...])``
  Returns the smallest or greatest value among ``Val1``, ``Val2`` and so on.

  * Each ``Val`` can be a numeric column's name, a number,
    or an expression that evaluates to a number.
  * If all values are integers, the result will also be an integer.
  * If *any* value is a floating point number, the result will be a floating
    point number.

  Example:

   ::

    $ aq_command ... -eval Float_Col 'Min(1, Integer_Col, Float_Col)' ...
    $ aq_command ... -eval Integer_Col 'Min(ToI(String_Col), Integer_Col)' ...

.. _`IsNaN()`:

``IsNaN(Val)``
  Tests if ``Val`` is not-a-number.

  * Returns 1 if true (not-a-number), 0 otherwise.
  * ``Val`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.

.. _`IsInf()`:

``IsInf(Val)``
  Tests if ``Val`` is infinite.

  * Returns 1, -1 or 0 if the value is positive infinity, negative infinity or
    finite respectively.
  * ``Val`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.


Comparison functions
====================

.. _`PatCmp()`:

``PatCmp(Val, Pattern [, AtrLst])``
  Compares a string with a generic wildcard pattern.

  * Returns 1 if they match, 0 otherwise.
    ``Pattern`` must match the *entire* ``Val`` to be successful.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``Pattern`` is a `string constant`_ that specifies
    the pattern to match. It is a simple wildcard pattern containing
    just '*' (matches any number of bytes) and '?' (matches any 1 byte) only;
    literal '*', '?' and '\\' in the pattern must be '\\' escaped.
  * Optional ``AtrLst`` is a list of ``|`` separated attributes containing:

    * ``ncas`` - Perform a case insensitive match (default is case sensitive).

  Example:

   ::

    $ aq_command ... -filt 'PatCmp(String_Col, "* ABC *")' ...
    $ aq_command ... -filt 'PatCmp(String_Col, "* \"ABC\" *")' ...
    $ aq_command ... -filt 'PatCmp(String_Col, "* \"\\\\ & \\*\" *")' ...

  * The first example matches values containing a basic literal " ``ABC`` ".
  * The second example matches values containing a literal " ``"ABC"`` ".
    To specify this as a *double quoted* `string constant`_,
    the quotes must be escaped,
    resulting in " ``\"ABC\"`` ".
  * The third example matches values containing a literal " ``"\ & *"`` ".
    This literal contains special pattern characters "``\``" and "``*``"
    that must be escaped, so the desire pattern is " ``"\\ & \*"`` ".
    Finally, to specify this as a *double quoted* `string constant`_,
    the quotes and backslashes must be escaped,
    resulting in " ``\"\\\\ & \\*\"`` ".

   ::

    $ aq_command ... -filt 'PatCmp(String_Col, "* ABC *", ncas)' ...

  * Same as the first example above except for the case insensitive attribute.

.. _`RxCmp()`:

``RxCmp(Val, Pattern [, AtrLst])``
  Compares a string with a GNU RegEx.

  * Returns 1 if they match, 0 otherwise.
    ``Pattern`` only needs to match a *subpart* of ``Val`` to be successful.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``Pattern`` is a `string constant`_ that specifies the GNU RegEx to match.
  * Optional ``AtrLst`` is a list of ``|`` separated attributes containing:

    * ``ncas`` - Perform a case insensitive match (default is case sensitive).
    * ``rx_extended`` - Enable POSIX Extended Regular Expression syntax.
    * ``rx_newline`` - Apply certain newline matching restrictions.

  Example:

   ::

    $ aq_command ... -filt 'RxCmp(String_Col, "^.* ABC .*$")' ...
    $ aq_command ... -filt 'RxCmp(String_Col, "^.* \"ABC\" .*$")' ...
    $ aq_command ... -filt 'RxCmp(String_Col, "^.* \"\\\\ & \\*\" .*$")' ...

  * Performs the same matches as the `PatCmp()`_ examples.
  * The ``^`` and ``$`` in the above expressions are not strictly necessary
    because of the leading and trailing ``.*``.

.. _`NumCmp()`:

``NumCmp(Val1, Val2, Delta)``
  Tests if ``Val1`` and ``Val2`` are within ``Delta`` of each other -
  i.e., whether ``Abs(Val1 - Val2) <= Delta``.

  * Returns 1 if true, 0 otherwise.
  * ``Val1``, ``Val2`` and ``Delta`` can be a numeric column's name,
    a numeric constant, or an expression that evaluates to a number.
  * ``Delta`` should be greater than or equal to zero.


Data extraction and encode/decode functions
===========================================

.. _`SubStr()`:

``SubStr(Val, Start [, Length])``
  Returns a substring of a string.

  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``Start`` is the starting position (zero-based) of the substring in ``Val``.
    It can be a numeric column's name, a number,
    or an expression that evaluates to a number.

    * If ``Start`` is negative, the length of ``Val`` will be added to it.
      If it is still negative, 0 will be used.

  * Optional ``Length`` specifies the length of the substring in ``Val``.
    It can be a numeric column's name, a number,
    or an expression that evaluates to a number.

    * Max length is length of ``Val`` minus ``Start``.
    * If ``Length`` is not specified, max length is assumed.
    * If ``Length`` is negative, max length will be added to it.
      If it is still negative, 0 will be used.

  Example:

   ::

    $ aq_command ... -eval String_Col 'SubStr(Str2, SLeng(Str2) - 2, 1)' ...
    $ aq_command ... -eval String_Col 'SubStr(Str2, -2, 1)' ...

  * These yield the same result.

.. _`ClipStr()`:

``ClipStr(Val, ClipSpec)``
  Returns a substring of a string.

  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``ClipSpec`` is a `string constant`_ that specifies
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

.. _`StrIndex()`:

``StrIndex(Val, Str [, AtrLst])``
  Returns the position (zero-based) of the first occurrence of ``Str`` in
  ``Val`` or -1 if it is not found.

  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``Str`` is the value to find within ``Val``.
    It can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * Optional ``AtrLst`` is a list of ``|`` separated attributes containing:

    * ``ncas`` - Perform a case insensitive match (default is case sensitive).
    * ``back`` - Search backwards from the end of ``Val``.

  Example:

   ::

    $ aq_command ... -filt 'StrIndex(Str1, Str2, ncas) >= 0' ...

  * Select records whose ``Str1`` contains ``Str2`` (case insensitive).

   ::

    $ aq_command ... -eval is:Pos 'StrIndex(Str1, Str2, ncas)' ...

  * If the result is to be assigned to a column, remember to use a *signed*
    numeric type since the result can be -1.

.. _`RxMap()`:

``RxMap(Val, MapFrom [, Col, MapTo ...] [, AtrLst])``
  Extracts substrings from a string based on a ``MapFrom``
  expression and place the results in columns based on ``MapTo``
  expressions.

  * Returns 1 if successful or 0 otherwise.
    ``MapFrom`` only needs to match a *subpart* of ``Val`` to be successful.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``MapFrom`` is a `string constant`_ that specifies the GNU RegEx to match.
    The expression should contain *subexpressions* for substring extractions.
  * The ``Col`` and ``MapTo`` pairs define how to save the results.
    ``Col`` is the column to put the result in. It must be of string type.
    ``MapTo`` is a `string constant`_ that defines how to render the result.
    It has the form:

     ::

      literal_1%%subexpression_N1%%literal_2%%subexpression_N2%%...

    where ``%%subexpression_N%%`` represents the extracted substring of the
    *Nth* subexpression in ``MapFrom``.
  * Optional ``AtrLst`` is a list of ``|`` separated attributes containing:

    * ``ncas`` - Perform a case insensitive match (default is case sensitive).
    * ``rx_extended`` - Enable POSIX Extended Regular Expression syntax.
    * ``rx_newline`` - Apply certain newline matching restrictions.

  Example:

   ::

    $ aq_command ... -eval - 'RxMap(String_Col, "^\(.*\) ABC \(.*\)$", OutCol1, "%%1%%", OutCol2, "%%2%%-%%1%%")' ...

  * Extracts the substrings before and after " ``ABC`` ". Then place different
    combinations of the substrings in 2 columns.

.. _`KeyEnc()`:

``KeyEnc(Col, [, Col ...])``
  Encodes columns of various types into a single string.

  * Returns a string key. The key is binary.
  * ``Col`` are the columns to encode into the key.

  Example:

   ::

    $ aq_command ... -eval s:Key 'KeyEnc(Col1, Col5, Col3)' ...

  * Encodes 3 columns in the given order into Key.

.. _`KeyDec()`:

``KeyDec(Key, Col|"ColType" [, Col|"ColType" ...])``
  Decodes a key previously encoded by `KeyEnc()`_
  and place the resulting components in the given columns.

  * Returns 1 if successful. A failure is considered a processing error.
    There is no failure return value.
  * ``Key`` is the previously encoded value.
    It can be a string column's name, a `string constant`_
    or an expression that evaluates to a string.
  * Each ``Col`` or ``ColType`` specifies a components in the key.

    * If a column is given, a component matching the column's type is expected;
      the extracted value will be placed in the given column.
    * If a column type string is given, a component matching this type is
      expected, but the extracted value will not be saved.

  * The components must be given in the same order as in the encoding call.

  Example:

   ::

    $ aq_command ... -eval - 'KeyDec(String_Col, Col1, "I", Col3)' ...

  * Extracts and saves the 1st and 3rd components in the key. A type must
    be given for the 2nd component even though its value is not needed.

.. _`QryDec()`:

``QryDec(Val, [, AtrLst], Col, KeyName [, AtrLst] [, Col, KeyName [, AtrLst] ...])``
  Extracts the values of selected query parameters from ``Val``
  and place the results in columns.

  * Returns the number of parameters extracted.
  * ``Val`` can be a string column's name, a `string constant`_
    or an expression that evaluates to a string.
  * Optional ``AtrLst`` following ``Val`` sets the default extraction behavior.
    It is a list of ``|`` separated attributes containing:

    * ``beg=c`` - Skip over the initial portion of ``Val`` up to and including
      the first 'c' character (single byte). A common value for 'c' is '?'.
      Without this attribute, the entire ``Val`` will be used.
    * ``zero`` - Zero out all destination columns before extraction.
    * ``dec=Num`` - Number of times to perform URL decode on the extracted
      values. ``Num`` must be between 0 and 99. Default is 1.
    * ``trm=c`` - Trim one leading and/or trailing 'c' character (single byte)
      from the decoded extracted values.

    A commonly used combination is ``beg=?,zero`` which processes the query
    portion of an URL and zero out all output columns before processing each
    URL in case certain parameters are not in the query.

  * The ``Col``, ``KeyName`` and optional ``AtrLst`` sets define what to
    extract. ``Col`` is the column to save the extracted value in.
    ``KeyName`` is a `string constant`_ that specifies the query key to extract.
    It should be URL decoded.
    Optional ``AtrLst`` sets the key specific extraction behavior.
    It is a list of ``|`` separated attributes containing:

    * ``zero`` - Zero out the destination column before extraction.
    * ``dec=Num`` - Number of times to perform URL decode on the extracted
      value of this Key. ``Num`` must be between 0 and 99.
    * ``trm=c`` - Trim one leading and/or trailing 'c' character (single byte)
      from the decoded extracted value.

  Example:

   ::

    $ aq_command ... -eval - 'QryDec(String_Col, "beg=?", Col1, "k1", Col2, "k1", zero)' ...

  * Extracts up to 2 values of "``k1``" into columns ``Col1`` and
    ``Col2`` from ``String_Col`` after the first "``?``".
    This assumes ``k1`` may appear more than once in the query.

.. _`UrlDec()`:

``UrlDec(Val)``
  Decodes an URL-encoded string.

  * Returns the decoded result.
    ``Val`` is returned if there is no URL-encoded components in it.
  * ``Val`` is the previously encoded value.
    It can be a string column's name, a `string constant`_
    or an expression that evaluates to a string.


.. _`Base64Dec()`:

``Base64Dec(Val)``
  Decodes a base64-encoded string.

  * Returns the decoded result.
    There is no integrity check. Portions of ``Val`` that is not base64-encoded
    are simply skipped. As a result, the function may return a blank string.
  * ``Val`` is the previously encoded value.
    It can be a string column's name, a `string constant`_
    or an expression that evaluates to a string.


General data conversion functions
=================================

.. _`ToIP()`:

``ToIP(Val)``
  Returns the IP address value of ``Val``.

  * ``Val`` can be a string/IP column's name, a `string constant`_,
    or an expression that evaluates to a string/IP.

  Example:

   ::

    $ aq_command ... -eval IP_Col 'ToIP("1.2.3.4")' ...
    $ aq_command ... -eval IP_Col 'ToIP(String_Col)' ...

.. _`ToF()`:

``ToF(Val)``
  Returns the floating point value of ``Val``.

  * ``Val`` can be a string/numeric column's name, a string/numeric constant,
    or an expression that evaluates to a string/number.

  Example:

   ::

    $ aq_command ... -eval Float_Col 'ToF("0.1234")' ...
    $ aq_command ... -eval Float_Col 'ToF(String_Col)' ...

.. _`ToI()`:

``ToI(Val)``
  Returns the integral value of ``Val``.

  * ``Val`` can be a string/numeric column's name, a string/numeric constant,
    or an expression that evaluates to a string/number.

  Example:

   ::

    $ aq_command ... -eval Integer_Col 'ToI("1234")' ...
    $ aq_command ... -eval Integer_Col 'ToI(String_Col)' ...

.. _`ToS()`:

``ToS(Val)``
  Returns the string representation of ``Val``.

  * ``Val`` can be a numeric column's name, a string/numeric/IP constant,
    or an expression that evaluates to a string/number/IP.

  Example:

   ::

    $ aq_command ... -eval String_Col 'ToS(1234)' ...
    $ aq_command ... -eval String_Col 'ToS(Integer_Col)' ...
    $ aq_command ... -eval String_Col 'ToS(1.2.3.4)' ...
    $ aq_command ... -eval String_Col 'ToS(IP_Col)' ...

.. _`ToUpper()`:

``ToUpper(Val)``, ``ToLower(Val)``
  Returns the upper or lower case string representation of ``Val``.

  * For ASCII strings only. May corrupt multibyte character strings.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.

.. _`RxReplace()`:

``RxReplace(Val, RepFrom, Col, RepTo [, AtrLst])``
  Replaces the first or all occurrences of a substring in ``Val`` matching
  expression ``RepFrom`` with expression ``RepTo`` and place the result in
  ``Col``.

  * Returns the number of replacements performed or 0 if there is no match.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``RepFrom`` is a `string constant`_ that specifies the GNU RegEx to match.
    Substring(s) matching this expression will be replaced.
    The expression can contain *subexpressions* that can be referenced in
    ``RepTo``.
  * ``Col`` is the column to put the result in. It must be of string type.
  * ``RepTo`` is an expression defining the replace-to value of each substring
    matching ``RepFrom``. It has this general form:

     ::

      literal_1%%subexpression_N1%%literal_2%%subexpression_N2%%...

    ``%%subexpression_N%%`` represents the substring that matches the
    *Nth* subexpression in ``RepFrom``.
  * Optional ``AtrLst`` is a list of ``|`` separated attributes containing:

    * ``ncas`` - Perform a case insensitive match (default is case sensitive).
    * ``rx_extended`` - Enable POSIX Extended Regular Expression syntax.
    * ``rx_newline`` - Apply certain newline matching restrictions.
    * ``all`` - Replace all occurrences of ``RepFrom`` in ``Val``.

  Example:

   ::

    $ aq_command ... -eval - 'RxReplace(String_Col, " *", OutCol, "\n", "all")' ...

  * Replaces all sequences of one or more blanks with newlines.


Date/Time conversion functions
==============================

.. _`DateToTime()`:

``DateToTime(DateVal, DateFmt)``, ``GmDateToTime(DateVal, DateFmt)``
  Both functions return the UNIX time in integral seconds corresponding to
  ``DateVal``.

  * ``DateVal`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``DateFmt`` is a `string constant`_ that specifies the format of
    ``DateVal``. The format is a sequence of conversion codes:

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
    Both functions will return the same result.
  * If there is no GMT offset in ``DateVal``, ``DateToTime()`` will return a
    UNIX time based on the program's default timezone (set the program's
    timezone, e.g, via the TZ environment, before execution if necessary)
    while ``GmDateToTime()`` will return a UNIX time based on GMT.

  Example:

   ::

    $ aq_command ... -eval Integer_Col 'DateToTime(Str2, "%Y.%m.%d.%H.%M.%S.....%z")' ...

  * This format is designed for a date string (``Str2``) like
    "``1969-12-31 16:00:01.123 -0800``". Note the use of extra dots in the
    format to map out the unwanted "``.123``".

.. _`TimeToDate()`:

``TimeToDate(TimeVal, DateFmt)``, ``TimeToGmDate(TimeVal, DateFmt)``
  Both functions return the date string corresponding to ``TimeVal``.
  The result string's maximum length is 127.

  * ``TimeVal`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.
  * ``DateFmt`` is a `string constant`_ that specifies
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


Character set encoding conversion functions
===========================================

These functions are implemented using the standard ``iconv`` library support.
Therefore, supported conversions are ``iconv`` dependent.
Run "``iconv --list``" to see the supported encodings.

.. _`IConv()`:

``IConv(Val, FromCodes, ToCode)``
  Converts a string from one character set encoding to another.

  * Returns the converted string if successful.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``FromCodes`` is a `string constant`_ containing a semi-colon separated
    list of character sets to try to convert from -
    e.g., "``utf8;euc-jp;sjis``".

    * A conversion is successful when *all* the data from ``Val`` is converted.
    * An attribute of ``eok`` can be added to any character of the sets -
      e.g., "``euc-jp;sjis;utf8,eok``".
      It tells the function to skip over any portion of ``Val`` that cannot be
      converted.
      An ``eok`` conversion is successful when *any* data from ``Val`` is
      converted.
    * If desired, add a character set of "``.``" (a dot) to the end of the list
      to tell the function to return ``Val`` as-is when none of the character
      sets match - e.g., "``utf8;euc-jp;sjis;.``". This conversion is always
      successful.

  * ``ToCode`` is a `string constant`_ containing the character set to convert
    to - e.g., "``utf8``".
  * The function returns on the first successful conversion in ``FromCodes``.
    If none of them worked, the function fails.

  Example:

   ::

    $ aq_command ... -eval String_Col 'IConv(Japanese_Col, "sjis;euc-jp;utf8", "utf8")' ...
    $ aq_command ... -eval String_Col 'IConv(Japanese_Col, "sjis;euc-jp;.", "utf8")' ...

  * Converts ``Japanese_Col`` from either SJIS or EUC into UTF8.
    The first example enforces that the result be UTF8.
    The second is more relaxed, its result may not be UTF8.


Speciality functions
====================

.. _`Set()`:

``Set(Str, Val)``
  Sets a column of name ``Str`` to value ``Val``. Note that the target
  column is determined at runtime during each evaluation.

  * Returns 1 if successful, 0 if the column cannot be found or if there is
    a datatype mismatch so that the assignment cannot be done.
    ``Pattern`` must match the *entire* ``Val`` to be successful.
  * ``Str`` is the column name. It can be a string column's name,
    or an expression that evaluates to a string.
    It can also be a `string constant`_; however, if this is the case,
    the standard ``-eval`` assignment should be used instead.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.


RTmetrics functions
===================

These functions provide some of the *RTmetrics* capabilities.
They require some support files to operate. A set of default support
files are included with the aq_tool installation package.

.. _`SearchKey()`:

``SearchKey(Site, Path)``, ``SearchKey(Url)``
  Extracts search key from the given site/path combination or URL.
  The extraction is done according to the rules in a search engine database
  supplied with the tool.

  * Returns the extracted search key (string).

    * A blank is returned if the site is not a search engine.
    * A "-" is returned if the site is a search engine but there is
      no search key.

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

.. _`IpToCountry()`:

``IpToCountry(Ip)``
  Looks up the given IP and return a "country_info[:region_info]" string.

  * The return string is a compact code suitable for data analysis.
    For reporting, use ``CountryName()`` and ``CountryRegion()`` to convert the
    code to names.
  * ``Ip`` can be a IP column's name, a literal IP
    or an expression that evaluates to an IP.

  Example:

   ::

    $ aq_command ... -eval String_Col 'IpToCountry(IP_Col)' ...
    $ aq_command ... -eval String_Col 'IpToCountry(1.2.3.4)' ...

.. _`CountryName()`:

``CountryName(Code)``, ``CountryRegion(Code)``
  ``CountryName()`` returns the country name (string) corresponding to the
  country info in ``Code``. |<br>|
  ``CountryRegion()`` returns the region name (string) corresponding to the
  region info in ``Code``.

  * ``Code`` can be a string column's name, a `string constant`_
    or an expression that evaluates to a string.
    It should contain a value previously returned from `IpToCountry()`_.
  * If ``Code`` does not contain any country/region info, a blank string is
    returned.

  Example:

   ::

    $ aq_command ... -eval String_Code_Col 'IpToCountry(IP_Col)' ...
        -eval String_Name_Col 'CountryName(String_Code_Col)' ...
        -eval String_Region_Col 'CountryRegion(String_Code_Col)' ...

.. _`AgentParse()`:

``AgentParse(Agent [, Ip])``
  Parses the given user-agent string and returns a string containing the
  extracted agent components.

  * The return string has these forms:

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

.. _`AgentName()`:

``AgentName(Code)``, ``AgentOS(Code)``, ``AgentDevType(Code)``, ``AgentDevName(Code)``
  ``AgentName()`` returns the browser name (string) portion of ``Code``. |<br>|
  ``AgentOS()`` returns the OS name (string) portion of ``Code``. |<br>|
  ``AgentDevType()`` returns the device type (string) portion of ``Code``. |<br>|
  ``AgentDevName()`` returns the device name (string) portion of ``Code``.

  * ``Code`` can be a string column's name, a `string constant`_
    or an expression that evaluates to a string.
    It should contain a value previously returned from `AgentParse()`_.

  Example:

   ::

    $ aq_command ... -eval String_Code_Col 'AgentParse(Str2)' ...
        ... -eval String_Name_Col 'AgentName(String_Code_Col)' ...
        ... -eval String_OS_Col 'AgentOS(String_Code_Col)' ...
        ... -eval String_DevType_Col 'AgentDevType(String_Code_Col)' ...
        ... -eval String_DevName_Col 'AgentDevName(String_Code_Col)' ...

.. _`IsCrawler()`:

``IsCrawler(Code)``
  Checks if the given ``Code`` is a crawler.

  * Returns 1 if true (i.e., ``Code`` is a crawler's name), 0 otherwise.
  * ``Code`` can be a string column's name, a `string constant`_
    or an expression that evaluates to a string.
    It should contain a value previously returned from `AgentParse()`_.

  Example:

   ::

    $ aq_command ... -eval String_Code_Col 'AgentParse(Str2)' ...
        ... -eval Integer_Col 'IsCrawler(String_Code_Col)' ...


Udb specific functions
======================

These functions are specific to Udb. They can only be used with
`aq_udb <aq_udb.html>`_.

.. _`RowCount()`:

``RowCount(TabName)``
  Returns the row count of the given table belonging to the current key.
  For a vector, it returns 1 if the verctor has been initialized, 0 otherwise.

  Example:

   ::

    $ aq_udb ... -pp . -if -filt 'RowCount(MyTable) < 10' -goto next_key -endif -endpp ...

  * Skip any keys that have less than 10 rows in ``MyTable``.


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

