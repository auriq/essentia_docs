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
* `Key hashing functions`_
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
  The code is usually 0 for a failed operation and non-zero otherwise.
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

.. _`Sqrt()`:

``Sqrt(Val)``
  Computes the square root of ``Val``.

  * ``Val`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.

``Cbrt(Val)``
  Computes the cube root of ``Val``.

  * ``Val`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.

``Log(Val)``
  Computes the natural logarithm of ``Val``.

  * ``Val`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.

``Log10(Val)``
  Computes the base 10 logarithm of ``Val``.

  * ``Val`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.

``Exp(Val)``
  Computes ``e`` (natural logarithm's base) raised to the power of ``Val``.

  * ``Val`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.

``Exp10(Val)``
  Computes 10 raised to the power of ``Val``.

  * ``Val`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.

``Pow(Val, Power)``
  Computes ``Val`` raised to the power of ``Power``.

  * ``Val`` and ``Power`` can be a numeric column's name, a numeric constant,
    or an expression that evaluates to a number.

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

.. _`BegCmp()`:

``BegCmp(Val, BegStr [, BegStr ...])``
  Compares one or more starting string ``BegStr`` with the head of ``Val``.
  All the comparisons are case sensitive.

  * Returns 1 if there is a match, 0 otherwise.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * Each ``BegStr`` is a `string constant`_ that specifies
    the starting string to match.

  Example:

   ::

    $ aq_command ... -filt 'BegCmp(String_Col, "* ABC *")' ...

  * Match a literal "``* ABC *``" with the head of the value of ``String_Col``.
    Note that '*' has no special meaning here.

.. _`EndCmp()`:

``EndCmp(Val, EndStr [, EndStr ...])``
  Compares one or more ending string ``EndStr`` with the tail of ``Val``.
  All the comparisons are case sensitive.

  * Returns 1 if there is a match, 0 otherwise.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * Each ``EndStr`` is a `string constant`_ that specifies
    the ending string to match.

  Example:

   ::

    $ aq_command ... -filt 'EndCmp(String_Col, "* ABC *")' ...

  * Match a literal "``* ABC *``" with the tail of the value of ``String_Col``.
    Note that '*' has no special meaning here.

.. _`SubCmp()`:

``SubCmp(Val, SubStr [, SubStr ...])``
  Compares one or more substring ``SubStr`` with with any part of ``Val``.
  All the comparisons are case sensitive.

  * Returns 1 if there is a match, 0 otherwise.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * Each ``SubStr`` is a `string constant`_ that specifies
    the substring to match.

  Example:

   ::

    $ aq_command ... -filt 'SubCmp(String_Col, "* ABC *", "D * E")' ...

  * Match a literal "``* ABC *``" *or* a literal "``D * E``"
    with any part of the value of ``String_Col``.
    Note that '*' has no special meaning here.

.. _`SubCmpAll()`:

``SubCmpAll(Val, SubStr [, SubStr ...])``
  Compares one or more substring ``SubStr`` with any part of ``Val``.
  All the comparisons are case sensitive.

  * Returns 1 if all the substrings match, 0 otherwise.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * Each ``SubStr`` is a `string constant`_ that specifies
    the substring to match.

  Example:

   ::

    $ aq_command ... -filt 'SubCmpAll(String_Col, "* ABC *", "D * E")' ...

  * Match a literal "``* ABC *``" *and* a literal "``D * E``"
    within the value of ``String_Col``.
    Note that '*' has no special meaning here.

.. _`MixedCmp()`:

``MixedCmp(Val, SubStr, Typ [, SubStr, Typ ...])``
  Compares one or more substring ``SubStr`` with ``Val`` according to the
  corresponding comparison type ``Typ`` of each ``SubStr``.
  All the comparisons are case sensitive.

  * Returns 1 if there is a match, 0 otherwise.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * Each ``SubStr`` and ``Typ`` pair specifies what and how to match.
    ``SubStr`` is a `string constant`_ that specifies the substring to match.
    ``Typ`` is a name with one of these values:

    * ``BEG`` - Match with the head of ``Val``.
    * ``END`` - Match with the tail of ``Val``.
    * ``SUB`` - Match with any part of ``Val``.

  Example:

   ::

    $ aq_command ... -filt 'MixedCmp(String_Col, "* ABC *", BEG, "D * E", END)' ...

  * Match a literal "``* ABC *``" with the head of the value of ``String_Col``
    *or*
    match a literal "``D * E``" with the tail of the value of ``String_Col``.
    Note that '*' has no special meaning here.

.. _`MixedCmpAll()`:

``MixedCmpAll(Val, SubStr, Typ [, SubStr, Typ ...])``
  Compares one or more substring ``SubStr`` with ``Val`` according to the
  corresponding comparison type ``Typ`` of each ``SubStr``.
  All the comparisons are case sensitive.

  * Returns 1 if all the substrings match, 0 otherwise.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * Each ``SubStr`` and ``Typ`` pair specifies what and how to match.
    ``SubStr`` is a `string constant`_ that specifies the substring to match.
    ``Typ`` is a name with one of these values:

    * ``BEG`` - Match with the head of ``Val``.
    * ``END`` - Match with the tail of ``Val``.
    * ``SUB`` - Match with any part of ``Val``.

  Example:

   ::

    $ aq_command ... -filt 'MixedCmpAll(String_Col, "* ABC *", BEG, "D * E", END)' ...

  * Match a literal "``* ABC *``" with the head of the value of ``String_Col``
    *and*
    match a literal "``D * E``" with the tail of the value of ``String_Col``.
    Note that '*' has no special meaning here.

.. _`Contain()`:

``Contain(Val, SubStrs)``
  Compares the substrings in ``SubStrs`` with any part of ``Val``.
  All the comparisons are case sensitive.

  * Returns 1 if there is a match, 0 otherwise.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``SubStrs`` is a `string constant`_ that specifies
    what substrings to match. It is a comma-newline separated list of literal
    substrings of the form "``SubStr1,[\r]\nSubStr2...``".

  Example:

   ::

    $ aq_command ... -filt 'Contain(String_Col, "* ABC *,\nD * E")' ...

  * Match a literal "``* ABC *`` " *or* a literal "``D * E``" with any part of
    the value of ``String_Col``.

.. _`ContainAll()`:

``ContainAll(Val, SubStrs)``
  Compares the substrings in ``SubStrs`` with any part of ``Val``.
  All the comparisons are case sensitive.

  * Returns 1 if all the substrings match, 0 otherwise.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``SubStrs`` is a `string constant`_ that specifies
    what substrings to match. It is a comma-newline separated list of literal
    substrings of the form "``SubStr1,[\r]\nSubStr2...``".

  Example:

   ::

    $ aq_command ... -filt 'ContainAll(String_Col, "* ABC *,\nD * E")' ...

  * Match a literal "``* ABC *`` " *and* a literal "``D * E``" with any part of
    the value of ``String_Col``.

.. _`PatCmp()`:

``PatCmp(Val, Pattern [, AtrLst])``
  Compares a generic wildcard pattern with ``Val``.

  * Returns 1 if it matches, 0 otherwise.
    ``Pattern`` must match the *entire* ``Val`` to be successful.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``Pattern`` is a `string constant`_ that specifies
    the pattern to match. It is a simple wildcard pattern containing
    just '*' (matches any number of bytes) and '?' (matches any 1 byte) only;
    literal '*', '?' and '\\' in the pattern must be '\\' escaped.
  * Optional ``AtrLst`` is a list of ``|`` separated attributes containing:

    * ``ncas`` - Perform a case insensitive match (default is case sensitive).
      For ASCII data only.

  Example:

   ::

    $ aq_command ... -filt 'PatCmp(String_Col, "* ABC *")' ...
    $ aq_command ... -filt 'PatCmp(String_Col, "* \"ABC\" *")' ...
    $ aq_command ... -filt 'PatCmp(String_Col, "* \"\\\\ & \\*\" *")' ...

  * The first example matches values of ``String_Col`` that contain a literal
    " ``ABC`` ".
  * The second example matches values of ``String_Col`` that contain a literal
    " ``"ABC"`` ".
    Note the "``\"``" escape sequence used on the literal quotes in the pattern.
    it is necessary because the ``Pattern`` is given as a
    *double quoted* `string constant`_.
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
  Compares a string with a regular expression.

  * Returns 1 if they match, 0 otherwise.
    ``Pattern`` only needs to match a *subpart* of ``Val`` to be successful.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``Pattern`` is a `string constant`_ that specifies the regular expression
    to match.
  * Optional ``AtrLst`` is a list of ``|`` separated
    `regular expression attributes <#regex-attributes>`_.

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
      For ASCII data only.
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
  * ``MapFrom`` is a `string constant`_ that specifies the regular expression
    to match. The expression should contain *subexpressions* for substring
    extractions.
  * The ``Col`` and ``MapTo`` pairs define how to save the results.
    ``Col`` is the column to put the result in. It must be of string type.
    ``MapTo`` is a `string constant`_ that defines how to render the result.
    It has the form:

     ::

      literal_1%%subexpression_N1%%literal_2%%subexpression_N2%%...

    where ``%%subexpression_N%%`` represents the extracted substring of the
    *Nth* subexpression in ``MapFrom``.
  * Optional ``AtrLst`` is a list of ``|`` separated
    `regular expression attributes <#regex-attributes>`_.

  Example:

   ::

    $ aq_command ... -eval - 'RxMap(String_Col, "^\(.*\) ABC \(.*\)$", OutCol1, "%%1%%", OutCol2, "%%2%%-%%1%%")' ...

  * Extracts the substrings before and after " ``ABC`` ". Then place different
    combinations of the substrings in 2 columns.

.. _`KeyEnc()`:

``KeyEnc(Col, [, Col ...])``
  Encodes columns of various types into a single string.

  * Returns a string key. The key is *binary*, do not try to interpret or
    modify it.
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

.. _`UrlEnc()`:

``UrlEnc(Val)``
  URL-encode a string.

  * Returns the encoded result.
  * ``Val`` is the string to encoded.
    It can be a string column's name, a `string constant`_
    or an expression that evaluates to a string.

.. _`UrlDec()`:

``UrlDec(Val)``
  Decodes an URL-encoded string.

  * Returns the decoded result.
  * ``Val`` is an URL-encoded string.
    It can be a string column's name, a `string constant`_
    or an expression that evaluates to a string.

.. _`Base64Enc()`:

``Base64Enc(Val)``
  Base64-encode a string.

  * Returns the encoded result.
  * ``Val`` is the string to encode.
    It can be a string column's name, a `string constant`_
    or an expression that evaluates to a string.

.. _`Base64Dec()`:

``Base64Dec(Val)``
  Decodes a base64-encoded string.

  * Returns the decoded result.
    There is no integrity check. Portions of ``Val`` that is not base64-encoded
    are simply skipped. As a result, the function may return a blank string.
  * ``Val`` is a base64-encoded string.
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

.. _`MaskStr()`:

``MaskStr(Val)``
  Irreversibly masks (or obfuscates) a string value.
  The result should be nearly as unique as the original (the probability of
  two different values having the same masked value is extremely small).

  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * The length of the result may be the same or longer than the original.

.. _`RxReplace()`:

``RxReplace(Val, RepFrom, Col, RepTo [, AtrLst])``
  Replaces the first or all occurrences of a substring in ``Val`` matching
  expression ``RepFrom`` with expression ``RepTo`` and place the result in
  ``Col``.

  * Returns the number of replacements performed or 0 if there is no match.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``RepFrom`` is a `string constant`_ that specifies the regular expression
    to match. Substring(s) matching this expression will be replaced.
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

    * ``all`` - Replace all occurrences of ``RepFrom`` in ``Val``.
    * One or more `regular expression attributes <#regex-attributes>`_.

  Example:

   ::

    $ aq_command ... -eval - 'RxReplace(String_Col, " *", OutCol, "\n", "all")' ...

  * Replaces all sequences of one or more blanks with newlines.

.. _`RxRep()`:

``RxRep(Val, RepFrom, RepTo [, AtrLst])``
  The same as `RxReplace()`_ except that it returns the result string directly
  (for this reason, it does not have `RxReplace()`_'s ``Col`` argument).


Date/Time conversion functions
==============================

.. _`DateToTime()`:

``DateToTime(DateVal, DateFmt)``, ``GmDateToTime(DateVal, DateFmt)``

  * By default, both functions return the UNIX time in integral seconds
    corresponding to ``DateVal``. However, if ``%S1``, ..., ``%S9`` is used,
    the result will be in deci-seconds, ..., nano-seconds.
  * ``DateVal`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``DateFmt`` is a `string constant`_ that specifies the format of
    ``DateVal``. The format is a sequence of conversion codes:

    * (a dot) ``.`` - represent a single unwanted character (e.g., a separator).
    * ``%Y`` - 1-4 digit year.
    * ``%y`` - 1-2 digit year.
    * ``%m`` - Month in 1-12.
    * ``%b`` - Abbreviated English month name ("JAN" ... "DEC", case
      insensitive).
    * ``%d`` - Day of month in 1-31.
    * ``%H`` or ``%I`` - hour in 0-23 or 1-12.
    * ``%M`` - Minute in 0-59.
    * ``%S`` - Second in 0-59.
    * ``%S0`` to ``%S9`` - Second in 0-59 plus an optional ``.digits`` fraction
      (any number of digits is fine).
      The result will be in sub-seconds - deci-seconds for ``%S1``,
      centi-seconds for ``%S2``, milli-seconds for ``%S3``, and so on.
      ``%S0`` is a special case where the fraction is parsed by not used
      in the result.
    * ``%p`` - AM/PM (case insensitive).
    * ``%z`` - Offset from GMT in the form [+|-]HHMM.

  * If ``DateVal`` contains GMT offset information (``%z`` info),
    the UNIX time will be calculated using this offset.
    Both functions will return the same result.
  * If there is no GMT offset in ``DateVal``, ``DateToTime()`` will return a
    UNIX time based on the program's default timezone (set the program's
    timezone, e.g, via the TZ environment, before execution if necessary)
    while ``GmDateToTime()`` will return a UNIX time based on GMT.

  Example:

   ::

    $ aq_command ... -eval I:Sec 'DateToTime(Str2, "%Y.%m.%d.%H.%M.%S......%z")' ...

  * This format is designed for a date string (``Str2``) like
    "``1969-12-31 16:00:01.1234 -0800``". Note the use of extra dots in the
    format to map out the unwanted "``.1234``".

   ::

    $ aq_command ... -eval L:MSec 'DateToTime(Str2, "%Y.%m.%d.%H.%M.%S3.%z")' ...

  * This format is designed for a date string (``Str2``) like
    "``1969-12-31 16:00:01.1234 -0800``". Note the use of ``%S3`` to extract
    milliseconds. The result is placed in an ``L`` column because ``I`` may
    overflow.

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
    If multiple ``FromCodes`` (see below) are given, the first code that
    successfully converted the *most amount* of ``Val`` will be used.
    The function fails if no conversion was successful.
  * ``Val`` can be a string column's name, a `string constant`_,
    or an expression that evaluates to a string.
  * ``FromCodes`` is a `string constant`_ containing a semi-colon separated
    list of character sets to try to convert from -
    e.g., "``utf8;euc-jp;sjis``".

    * A conversion is successful when *all* the data from ``Val`` is converted.
    * To allow partial conversion on ``Val``, add an ``eok`` attribute to the
      desired character set - e.g., "``euc-jp;sjis,eok;utf8``".
      This conversion *always succeeds*, even when nothing can be converted.
    * A character set of "``.``" (a dot) will use ``Val`` as the converted
      result. This conversion always succeeds. Use this at the end of the list
      as a fallback if desired - e.g., "``utf8;euc-jp;sjis;.``".
    * A character set of "``-``" (a dash) will use a blank as the converted
      result. This conversion always succeeds. Use this at the end of the list
      as a fallback if desired - e.g., "``utf8;euc-jp;sjis;-``".

  * ``ToCode`` is a `string constant`_ containing the character set to convert
    to - e.g., "``utf8``".

  Example:

   ::

    $ aq_command ... -eval String_Col 'IConv(Japanese_Col, "sjis;euc-jp", "utf8")' ...
    $ aq_command ... -eval String_Col 'IConv(Japanese_Col, "sjis;euc-jp;.", "utf8")' ...
    $ aq_command ... -eval String_Col 'IConv(Japanese_Col, "sjis;euc-jp;-", "utf8")' ...
    $ aq_command ... -eval String_Col 'IConv(Japanese_Col, "sjis,eok;euc-jp", "utf8")' ...

  * All the commands convert ``Japanese_Col`` from either SJIS or EUC into UTF8.
  * Command #1 - both the SJIS-UTF8 and EUC-UTF8 conversions must be
    exact. If neither were successful, the function fails.
  * Command #2 - similar to #1 except that the input is used as the result if
    neither conversions were successful.
  * Command #3 - similar to #1 except that a blank is used as the result if
    neither conversions were successful.
  * Command #4 - the SJIS-UTF8 conversion can be partial while the EUC-UTF8
    conversion must still be exact.


Key hashing functions
=====================

.. _`KeyHash()`:

``KeyHash(Col, [, Col ...])``
  Hashes the given columns into a 32-bit hash value.
  This is the hash value used by Udb internally.
  It is a good quality hash suitable for many uses (other than the 2 cases
  covered by `ImpHash()`_  and `SegHash()`_).

  * Returns a 32-bit hash value.
  * ``Col`` are the columns to be hashed.

.. _`ImpHash()`:

``ImpHash(Col, [, Col ...])``
  Hashes the given columns into a 32-bit hash value.
  This is the hash value used by `aq_pp <aq_pp.html>`_ to distribute data
  over Udb workers during an `import <aq_pp.html#imp>`_.
  Use this to reproduce the Udb data distribution behavior as needed.

  * Returns a 32-bit hash value.
  * ``Col`` are the columns to be hashed.

.. _`SegHash()`:

``SegHash(Col, [, Col ...])``
  Hashes the given columns into a 32-bit hash value.
  This is the hash value used by `aq_pp <aq_pp.html>`_ to select sample data
  for `import <aq_pp.html#imp>`_ into Udb.
  Use this to reproduce Udb import's data sampling behavior as needed.

  * Returns a 32-bit hash value.
  * ``Col`` are the columns to be hashed.


Speciality functions
====================

.. _`Set()`:

``Set(NameStr, Val)``
  Sets a column of name ``NameStr`` to value ``Val``. Note that the target
  column is determined at runtime during each evaluation.

  * Returns 1 if successful, 0 if the column cannot be found or if there is
    a datatype mismatch so that the assignment cannot be done.
  * ``NameStr`` is the target column name. It can be a string column's name,
    or an expression that evaluates to a string.
    It can also be a `string constant`_; however, if this is the case,
    the standard ``-eval`` assignment should be used instead.
  * ``Val`` is the value to assign to the target column. It must have the same
    type as the target column. It can be a column's name, a constant,
    or an expression that evaluates to a value.


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

.. _`AgentToUId()`:

``AgentToUId(Agent [, Ip])``
  Convert the given user-agent string to a numeric RTmetrics user ID.

  * An user ID of ``2`` indicates a crawler.
  * ``Agent`` can be a string column's name, a `string constant`_
    or an expression that evaluates to a string.
  * ``Ip`` is an optional source IP for more accurate crawler matching.
    It can be an IP column's name, a literal IP
    or an expression that evaluates to an IP.

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

.. _`UNameHash()`:

``UNameHash(NameStr)``
  Convert the given string (usually an user name) to an RTmetrics hashed name
  string. |<br>|
  *Note*: for generic string obfuscation, use `MaskStr()`_ instead.

  * Returns the hashed string. It is an alphanumeric string of length 8.
    This is a low quality hash, so collision is possible.
  * ``NameStr`` can be a string column's name, a `string constant`_
    or an expression that evaluates to a string.


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

.. _`RegexAttributes`:

RegEx Attributes
================

These attributes are used by the `aq_pp <aq_pp.html>`_ mapping options and
the regular expression related funstions described above.

* In command line options, the attributes are specified as a ``,`` separated
  list on the options
  (e.g., ``-map,pcre,ncas``).
* In evaluation functions, the attributes are specified as a ``|`` separated
  list in one the functions' parameters
  (e.g., ``RxCmp(Col, "[0-9]*", pcre|ncas)``).

There are 2 major sets of attributes, one for the POSIX engine and one for PCRE.

* ``ncas`` - Perform a case insensitive match (default is case sensitive).
* ``rx`` - Select the POSIX engine. This is the default if no engine is
  selected explicitly.
* These are POSIX specific attributes. Selecting any of them implies ``rx``:

  * ``rx_extended`` - Enable POSIX Extended Regular Expression syntax.
  * ``rx_icase`` - Same as ``rx`` and ``ncas`` together.
  * ``rx_newline`` - Apply certain newline matching restrictions.

* ``pcre`` - Select the PCRE engine.
* These are PCRE specific attributes. Selecting any of them implies ``pcre``.
  For details, see the corresponding ``PCRE2_*`` descriptions in the
  `PCRE2 manual <http://www.pcre.org/current/doc/html/pcre2api.html>`_.

  * ``allow_empty_class`` (PCRE2_ALLOW_EMPTY_CLASS) - Allow empty classes.
  * ``alt_bsux`` (PCRE2_ALT_BSUX) - Alternative handling of ``\u``, ``\U``, and ``\x``.
  * ``alt_circumflex`` (PCRE2_ALT_CIRCUMFLEX) - Alternative handling of ``^`` in multiline mode.
  * ``alt_verbnames`` (PCRE2_ALT_VERBNAMES) - Process backslashes in verb names.
  * ``caseless`` (PCRE2_CASELESS) - Same as ``pcre`` and ``ncas`` together.
  * ``dollar_endonly`` (PCRE2_DOLLAR_ENDONLY) - ``$`` not to match newline at end.
  * ``dotall`` (PCRE2_DOTALL) - ``.`` matches anything including newline.
  * ``dupnames`` (PCRE2_DUPNAMES) - Allow duplicate names for subpatterns.
  * ``extended`` (PCRE2_EXTENDED) - Ignore white space and ``#`` comments.
  * ``firstline`` (PCRE2_FIRSTLINE) - Force matching to be before newline.
  * ``match_unset_backref`` (PCRE2_MATCH_UNSET_BACKREF) - Match unset back references.
  * ``multiline`` (PCRE2_MULTILINE) - ``^`` and ``$`` match newlines within data.
  * ``never_backslash_c`` (PCRE2_NEVER_BACKSLASH_C) - Lock out the use of ``\C`` in patterns.
  * ``never_ucp`` (PCRE2_NEVER_UCP) - Lock out PCRE2_UCP.
  * ``never_utf`` (PCRE2_NEVER_UTF) - Lock out PCRE2_UTF.
  * ``no_dotstar_anchor`` (PCRE2_NO_DOTSTAR_ANCHOR) - Disable automatic anchoring for ``.*``.
  * ``no_start_optimize`` (PCRE2_NO_START_OPTIMIZE) - Disable match-time start optimizations.
  * ``ucp`` (PCRE2_UCP) - Use Unicode properties for ``\d``, ``\w``, etc.
  * ``ungreedy`` (PCRE2_UNGREEDY) - Invert greediness of quantifiers.
  * ``utf`` (PCRE2_UTF) - Treat pattern and subjects as UTF strings.
  * ``anchored`` (PCRE2_ANCHORED) - Match only at the first position.
  * ``notbol`` (PCRE2_NOTBOL) - Subject string is not the beginning of a line.
  * ``noteol`` (PCRE2_NOTEOL) - Subject string is not the end of a line.
  * ``notempty`` (PCRE2_NOTEMPTY) - An empty string is not a valid match.
  * ``notempty_atstart`` (PCRE2_NOTEMPTY_ATSTART) - An empty string at the start of the subject is not a valid match.
  * ``no_utf_check`` (PCRE2_NO_UTF_CHECK) - Do not check the subject for UTF validity (only relevant if ``utf`` is also set.


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udbd <udbd.html>`_ - Udb server
* `aq_udb <aq_udb.html>`_ - Udb server interface

