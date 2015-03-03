========
udb.spec
========


Description
===========

A Udb spec file holds a Udb database specification.
It contains target server specs that form the server pool and
table/vector/variable specs that form the data definition.
It is used by the Udb client programs `aq_pp <aq_pp.html>`_ and
`aq_udb <aq_udb.html>`_ to determine which servers to send requests to and
what data definition to pass to them.
Recall that an Udb server is not tied to any particular data definition
until instructed by a client; after which the definition remains until
the its database is cleared.

The spec file contains multiple sections.
Each section starts with a keyword followed by the relevant spec.
For example, ``@Server:`` starts a Udb server address section and
``@Table:`` start a table definition section.
A spec section ends when another keyword is encountered
or at the end-of-file.

Basic file format is:

* Line oriented text file.
  The maximum length of a line is 1022 bytes.
* Leading spaces on each line are ignored.
  Interpretation starts at the first non-blank character.
* Blank lines are ignored.
* A line starting with a '#' character is a Comment line.
  A comment must be on a line by itself.
* Keywords and names are case insensitive.

See the sample below for a complete description.
Note that the indentation and blank lines in the sample are optional.


Sample Spec
===========

::

  #
  # "@Server:" starts a server spec section.
  # o Required.
  # o One or more lines of target server spec.
  # o Each server spec has the form:
  #     IP_or_Domain[|IP_or_Domain_Alt][:Port]
  # o Port is needed when a non-default port is used (see "@Port" below).
  # o "IP_or_Domain" is the address used by client programs (aq_pp and
  #   aq_udb) to communicate with the server. "IP_or_Domain_Alt" is the
  #   server's local/private IP; it is only needed if it is different
  #   from the first one.
  #
  @Server:
    127.0.0.1
    127.0.0.1:10011
    [::127.0.0.1]:10012
    a.b.com
    a.b.com:10011
    99.1.2.3|10.0.0.2:10013

  #
  # "@Port:Port" sets the port number for any servers without a port spec.
  # o Optional, default is 10010.
  #
  @Port:10010

  #
  # "@Table:TabName" starts a table spec:
  # o TabName is the name of the table (case insensitive). It can contain
  #   up to 31 alphanumeric and '_' characters. The first character cannot
  #   be a digit.
  # o Subsequent lines are column specs in the form "Type[,Atr]:ColName".
  #   Up to 255 columns can be specified.
  # o Column Types are:
  #   o S - String.
  #   o F - Double precision floating point.
  #   o L - 64-bit unsigned integer.
  #   o LS - 64-bit signed integer.
  #   o I - 32-bit unsigned integer.
  #   o IS - 32-bit signed integer.
  #   o IP - v4/v6 address.
  # o Column Atr's are:
  #   o PKEY - Must be "S" type. Mark the "bucket key". One column in the
  #            table MUST have this attribute.
  #   o TKEY - Mark a single column as the table's default sort key
  #            (e.g., time). This is for convenience only. Sort column(s)
  #            can be selected at run time via aq_udb.
  #   o +KEY - Mark a column as part of a merge key. Merge key is checked
  #            during import. If the key in a pending import row is not
  #            found in any existing row, the row will be added as new.
  #            On the other hand, if the key is found, the pending row will
  #            be "merged" with the existing row. The default per-column
  #            "merge" action is "+LAST". See "+*" below for details.
  #   o +FIRST - Keep the old value.
  #   o +LAST - Use the pending value. This is the default merge action.
  #   o +ADD - Add/append (numeric/string) pending value to existing value.
  #   o +BOR - Bitwise-OR (numeric) pending value with existing value.
  #   o +MIN - Use the lesser (numeric) of pending and existing value.
  #   o +MAX - Use the greater (numeric) of pending and existing value.
  #   o +NOZERO - Do not use pending value if it is 0 (numeric) or blank
  #            (string). Use in conjunction with the above "+*" attributes.
  # o ColName is the name of the column (case insensitive). It can contain
  #   up to 31 alphanumeric and '_' characters. The first character cannot
  #   be a digit.
  #
  @Table:MyTable
    i,tkey:t
    l:c1
    l:c2
    i:c3
    s,pkey:user_cookie
    s:c5
    i:c6
    i:c7
    i:c8
    s:c9
    s:c10
    s:page
    s:query
    s:c13
    s:c14
    s:referrer_site
    s:search_key

  #
  # "@Vector:TabName" starts a vector table spec.
  # o A vector is a table that has only one data row. It is often used to
  #   store bucket level profile data.
  # o Vectors are automatically created when a user bucket is created.
  #   Their columns are initialized to either 0/blank depending on the
  #   data type.
  # o Vector spec is identical to that of a table except that "+KEY" is
  #   not supported nor necessary - the "merge" operation is implicit
  #   since there is only one data row.
  # o The name of the "PKEY" column must be the same as in previously
  #   defined tables/vectors.
  #
  @Vector:Profile
    s,pkey:user_cookie
    l,+bor:flag_1
    l,+bor:flag_2
    l,+add:sum_1
    l,+add:sum_2

  #
  # "@Var:" starts the Var vector spec.
  # o A Var vector holds a single row of data. The columns (or vars) are
  #   global and NOT bucket specific.
  # o It does not need a name since there can only be one Var vector spec.
  #   However, it does have the implicit name "var".
  # o Var columns can be used in most "aq_udb" operations. See the "aq_udb"
  #   manual for details.
  # o Columns in this vector are initialized to 0/blank. They can also be
  #   reset to 0/blank at any time using "aq_udb -clr var".
  # o Columns in this vector can be set using
  #   "aq_udb -scn var -var ColName ColVal -var ColName ColVal ...".
  # o Columns in this vector can be exported using "aq_udb -exp var"
  # o Vector spec is identical to that of a regular vector.
  # o The "merge" operation is done differently from that of a regular
  #   vector - it is done during an export to combine data from separate
  #   Udb servers.
  #
  @Var:
    s:g_str_1
    l,+bor:g_flag_1
    l,+bor:g_flag_2
    l,+add:g_sum_1
    l,+add:g_sum_2

  #
  # Specify more tables/vectors as needed. But there can only be one Var
  # vector. The order of the definitions is not important.
  #


Udb Data Arrangement
====================

An Udb server constructs its database according to the spec in this manner:

 ::

  +------------+------+
  | Var vector | cols |
  +------------+------+

  +=================+=======+
  | User key (PKEY) | key1  |
  +=================+=======+
  | +--------+-----------+  |
  | | Table1 | row1 cols |  |
  | |        | row2 cols |  |
  | |        | ...       |  |
  | +--------+-----------+  |
  | | Table2 | row1 cols |  |
  | |        | row2 cols |  |
  | |        | ...       |  |
  | +--------+-----------+  |
  | | ...                |  |
  | +--------+-----------+  |
  | +---------+------+      |
  | | Vector1 | cols |      |
  | +---------+------+      |
  | | Vector2 | cols |      |
  | +---------+------+      |
  | | ...            |      |
  | +---------+------+      |
  |                         |
  +=================+=======+
  | User key (PKEY) | key2  |
  +=================+=======+
  | +--------+-----------+  |
  | | Table1 | row1 cols |  |
  | |        | row2 cols |  |
  | |        | ...       |  |
  | +--------+-----------+  |
  | | Table2 | row1 cols |  |
  | |        | row2 cols |  |
  | |        | ...       |  |
  | +--------+-----------+  |
  | | ...                |  |
  | +--------+-----------+  |
  | +---------+------+      |
  | | Vector1 | cols |      |
  | +---------+------+      |
  | | Vector2 | cols |      |
  | +---------+------+      |
  | | ...            |      |
  | +---------+------+      |
  |                         |
  +=================+=======+
  | User key (PKEY) | key3  |
  +=================+=======+
  | ...                     |
  |                         |
  +-------------------------+


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udbd <udbd.html>`_ - User (Bucket) Database server
* `aq_udb <aq_udb.html>`_ - Interface to Udb server

