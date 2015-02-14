========
udb.spec
========

-------------
Udb spec file
-------------

:Copyright: AuriQ Systems Inc.
:Manual group: Udb
:Manual section: 5
:Date: 2015-01-28
:Version: 1.2.1


Description
===========

A Udb spec file holds a Udb database specification.
It contains target server specs that form the server pool and
table/vector/variable specs that form the data definition.
It is used by the Udb client programs `aq_udb <aq_udb.html>`_ and `aq_pp <aq_pp.html>`_ to determine 
which servers to send requests to and what data definition to pass to them.
Recall that an Udb server is not tied to any particular data definition
until instructed by a client; after which the definition remains until
the its database is cleared.

The spec file contains multiple sections.
Each section starts with a keyword (e.g., ``@Server:``)
followed by the relevant spec. The spec can be a single value,
multiple lines, or both. The spec ends when another keyword is encountered
or at the end-of-file.

Basic file format is:

* Line oriented text file.
* Leading spaces on each line are ignored.
  Interpretation starts at the first non-blank character.
* Blank lines are ignored.
* A line starting with a '#' character is a Comment line.
  A comment must be on a line by itself.
* Keywords are case insensitive.

See the sample below for a complete description.


SAMPLE SPEC
===========

::

  #
  # "@Server:" starts a server spec section.
  # o Required.
  # o One or more lines of target server spec.
  # o Each server spec has the form:
  #     IP_or_Domain[|IP_or_Domain_Alt][:Port]
  # o Port is needed when a non-default port is used (see "@Port" below).
  # o The first "IP_or_Domain" is normally used to communicate with the
  #   target server. The "IP_or_Domain_Alt" address is only used if the
  #   "-local" option is set in aq_udb and that "IP_or_Domain_Alt" matches
  #   an local IP.
  #
  # Note: The indentation is optional.
  #
  @Server:
    127.0.0.1
    127.0.0.1:10011
    [::127.0.0.1]:10012
    a.b.com
    a.b.com:10011
    99.1.2.3|10.0.0.2:10013

  #
  # "@Port:port" set the port number for any servers without a port spec.
  # o Optional, default is 10010.
  # o The port number must follow the keyword immediately.
  #
  @Port:10010

  #
  # "@Table:TabName" starts a table spec:
  # o TabName is the name of the table being defined. It must follow the
  #   keyword immediately.
  # o TabName restrictions:
  #   o Case insensitive.
  #   o Up to 31 bytes long.
  #   o Can contain alphanumeric and '_' characters only. The first
  #     character cannot be a digit.
  # o Subsequent lines are column specs in the form "Type[,Atr]:ColName".
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
  # o ColName restrictions:
  #   o Case insensitive.
  #   o Up to 31 bytes long.
  #   o Can contain alphanumeric and '_' characters only. The first
  #     character cannot be a digit.
  # o Up to 256 columns can be specified.
  #
  # Note: Indentation in the spec is optional.
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
  # o Column spec is identical to that of a table except that
  #   "+KEY" is not supported nor necessary since the "merge" operation is
  #   implicit (there is only one data row).
  #
  # Note: Indentation in the spec is optional.
  #
  @Vector:Profile
    s,pkey:user_cookie
    l,+bor:flag_1
    l,+bor:flag_2
    l,+add:sum_1
    l,+add:sum_2

  #
  # "@Var:" starts the Var table spec.
  # o A var table holds a single row of data. The columns (or vars) are
  #   global and NOT bucket specific.
  # o It does not need a name since there can only be one Var table spec.
  # o Var columns can be used in most "aq_udb" operations. See the "aq_udb"
  #   manual for details.
  # o Even though there is no table name in the spec, the Var table can be
  #   referenced using the pseudo table name "var".
  # o Columns in this table are initialized to 0/blank. They can also be
  #   reset to 0/blank at any time using "aq_udb -clr var".
  # o Columns in this table can be set using
  #   "aq_udb -scn var -var ColName ColVal -var ColName ColVal ...".
  # o Columns in this table can be exported using "aq_udb -exp var"
  # o Column spec is identical to that of a table except that
  #   "+KEY" is not supported nor necessary. Also, the "merge" operation
  #   is only done during an export to combine data rows from
  #   multiple Udb servers. There is no "merge" operation on import since
  #   data cannot be imported to this table.
  #
  # Note: Indentation in the spec is optional.
  #
  @Var:
    s:g_str_1
    l,+bor:g_flag_1
    l,+bor:g_flag_2
    l,+add:g_sum_1
    l,+add:g_sum_2

  #
  # Specify more tables/vectors as needed. But there can only be one Var
  # table. The order of the definitions is not important.
  #


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udbd <udbd.html>`_ - User (Bucket) Database server
* `aq_udb <aq_udb.html>`_ - Interface to Udb server

