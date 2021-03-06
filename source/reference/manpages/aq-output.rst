.. |<br>| raw:: html

   <br>

=========
aq-output
=========

aq_tool output specifications


Synopsis
========

::

  aq_command ...
    ...
    -o[,AtrLst] File
    ...


Description
===========

Most aq_tool commands produce one or more outputs. Specification of the
output destination is generally done using the `-o <#output-file-option>`_
option. Besides the destination, the option also has
output attributes that control the ouput behavior.

Note that certain aq_tools can produce multiple outputs. For example,
`aq_pp <aq_pp.html>`_ has a ``-ovar`` option that takes the same
output attributes.
The description below applies to those output specs well.


Output File Option
==================

``-o[,AtrLst] File``

The ``-o`` option sets the output attributes (``AtrLst``) and destination
(``File``).
The destination can be a regular file or a stream:

* For a regular file, specify the file's path as ``File``.
* For a stream to the standard output, specify a ``-`` (a single dash) as
  ``File``.
* For a stream to a named pipe, specify ``fifo@PipeName`` as ``File``
  where ``PipeName`` is the named pipe's path. The program will create the
  pipe if it does not exist or just use it if it does.
  If the named pipe is known to exist already, ``PipeName`` alone also works.
* For a stream obtained from connecting to a listener, specify
  ``connect@DomainName:Port`` or ``connect@IP4:Port`` or ``connect@[IP6]:Port``
  as ``File``. ``DomainName``/``IP4``/``IP6`` and ``Port`` are the address and
  port to connect to.
* For a stream obtained from accepting a connection, specify
  ``listen@DomainName:Port`` or ``listen@IP4:Port`` or ``listen@[IP6]:Port`` or
  ``listen@Port``
  as ``File``. ``DomainName``/``IP4``/``IP6`` and ``Port`` are the address and
  port to listen at.

Optional ``AtrLst`` defines the output's data format and handling
characteristics. It is a list of comma separated attributes containing:

* Output format selection:

  These attributes are mutually exclusive except for
  ``sep`` and ``csv`` that can be used together.
  If no output format attribute is given, ``csv`` is assumed.

  * ``csv`` - Output in CSV format. This is the default output format.
    Although CSV implies *comma separated*, ``sep=c`` can be used to select
    a different separator.
  * ``sep=c`` or ``sep=\xHH`` - Output in 'c' (single byte) separated value
    format. ``\xHH`` is a way to specify 'c' via its HEX value ``HH``.
  * ``jsn`` - Output each record as an JSON object as in
    ``{ "ColName":Value,...}<newline>``.
  * ``bin`` - Output in aq_tool's internal binary format.
  * ``aq`` - Output in a special aq_tool internal format that contains
    an embedded column spec. The output is intended for use by another
    aq_tool inputting in ``aq`` format.

* Output characteristic modifiers:

  These attributes are for ``sep`` and ``csv`` formats only.
  The other formats (e.g., ``jsn``) have their own specifications that
  cannot be modified.

  * ``notitle`` - Suppress the column name label row from the output.
    A label row is normally included by default.
  * ``fmt_g`` - Use "%g" as print format for ``F`` type columns. Only use this
    to aid data inspection (e.g., during integrity check or debugging).
    The default is to print up to 17 digits (the minimum precision needed to
    preserve the value of a ``F`` type column).
  * ``esc`` - Use a '\\' to escape the field separator, '"' and '\\' characters.

* Miscellaneous output controls:

  * ``app`` - When outputting to a file, append to it instead of overwriting.
  * ``nodelay`` - Output records as soon as possible. Otherwise, up to 16KB
    of data may be buffered before an output occurs.


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `aq_cnt <aq_cnt.html>`_ - Data row/key count
* `aq_ord <aq_ord.html>`_ - In-memory record sort
* `aq_cat <aq_cat.html>`_ - Input multiplexer
* `aq-input <aq-input.html>`_ - aq_tool input specifications

