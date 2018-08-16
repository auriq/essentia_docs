.. |<br>| raw:: html

   <br>

========
udb.spec
========

Udb spec file


Description
===========

A Udb spec file holds a Udb database specification.
It contains target server specs that form the server pool and
key/table/vector/variable specs that form the primary key and
associated data definition.
It is used by the Udb client programs `aq_pp <aq_pp.html>`_ and
`aq_udb <aq_udb.html>`_ to determine which servers to send requests to and
what data definition to pass to them. See the commands' documentation on
how to set the spec file for the commands.

The spec file contains multiple sections.
Each section starts with a keyword followed by the relevant spec.
For example, ``@Server:`` starts a Udb server address section and
``@Table:`` start a table definition section.
A spec section ends when another keyword is encountered
or at the end-of-file.

Basic file format is:

* Line oriented text file.
  The maximum length of a line is 2046 bytes.
* Leading spaces on each line are ignored.
  Interpretation starts at the first non-blank character.
* Blank lines are ignored.
* A line starting with a '#' character is a Comment line.
  Comment can also start in the middle of a line as long as the '#' character
  is preceeded by a blank/punctuation.
* Keywords and names are case insensitive.

See the sample below for a complete description.
Note that the indentation and blank lines in the sample are optional.
Line breaks are also optional; however, they are recommended for readability
and to prevent a line from exceeding 2046 bytes.

**Important**: Do not change the database spec after it has been created on
the server side.


Sample Spec
===========

::

  #
  # "@Server:" starts a server spec section.
  # o Required.
  # o One or more target server specs that form the database's server pool.
  # o Each server spec has the form:
  #     IP_or_Domain[|IP_or_Domain_Alt][:Port][*Weight]
  # o "IP_or_Domain" is the address used by client programs (aq_pp and
  #   aq_udb) to communicate with the server. "IP_or_Domain_Alt" is the
  #   server's local/private IP; it is only needed if it is different
  #   from the first one.
  # o Port is needed when a non-default port is used (see "@Port" below).
  # o Weight is an integer that sets the approx. data share of this server.
  #   Default is 1, max is 1000.
  #
  @Server:
    127.0.0.1
    127.0.0.1:10011
    [::127.0.0.1]:10012	# note syntax for v6 address with port
    a.b.com
    a.b.com:10011
    99.1.2.3|10.0.0.2:10013

  #
  # "@Port:Port" sets the port number for any servers without a port spec.
  # o Optional, default is 10010.
  #
  @Port:10010

  #
  # "@PKey:" sets the primary key columns of the database.
  # o Required.
  # o Subsequent lines are key column specs in the form "Type:ColName".
  #   Max columns is 2048.
  # o Column Types are:
  #   o S - String.
  #   o F - Double precision floating point.
  #   o L - 64-bit unsigned integer.
  #   o LS - 64-bit signed integer.
  #   o I - 32-bit unsigned integer.
  #   o IS - 32-bit signed integer.
  #   o IP - v4/v6 address.
  # o ColName is the name of the key column (case insensitive). It can contain
  #   up to 31 alphanumeric and '_' characters. The first character cannot
  #   be a digit.
  #
  @PKey:
    s:KeyStr
    i:KeyNum

  #
  # "@Table:TabName" starts a table spec:
  # o TabName is the name of the table (case insensitive). It can contain
  #   up to 31 alphanumeric and '_' characters. The first character cannot
  #   be a digit.
  # o Subsequent lines are column specs in the form "Type[,Atr]:ColName".
  #   Do not include the PKey columns here. Max columns is (2048 - #Pkeys).
  # o Column Types are:
  #   o S - String.
  #   o F - Double precision floating point.
  #   o L - 64-bit unsigned integer.
  #   o LS - 64-bit signed integer.
  #   o I - 32-bit unsigned integer.
  #   o IS - 32-bit signed integer.
  #   o IP - v4/v6 address.
  # o Column Atr's are:
  #   o +KEY - Mark a column as part of a merge key. Merge key is checked
  #            during import. If the key in a pending import row is not
  #            found in any existing row, the row will be added as new.
  #            On the other hand, if the key is found, the pending row will
  #            be "merged" with the existing row. The default per-column
  #            "merge" action is "+LAST". See "+*" below for details.
  #   o +FIRST - Keep the old value.
  #   o +LAST - Use the pending value. This is the default merge action.
  #   o +ADD - Add (numeric) pending value to existing value.
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
    i:Time
    s:Page
    s:Query
    s:Referrer
    s:SearchKey

  #
  # "@Vector:TabName" starts a vector spec.
  # o A vector has only one data row. It is often used to store key specific
  #   profile data.
  # o Vectors are automatically created when a key is created.
  #   Their columns are initialized to either 0/blank depending on the
  #   data type.
  # o Vector spec is identical to that of a table except that "+KEY" is
  #   not supported nor necessary - the "merge" operation is implicit
  #   since there is only one data row.
  #
  @Vector:Profile
    l,+bor:flag_1
    l,+bor:flag_2
    l,+add:sum_1
    l,+add:sum_2

  #
  # Specify more tables and vectors as needed.
  #

  #
  # "@Var:" starts the Var vector spec.
  # o Var holds a single row of data like a vector.
  # o Only one such definition can be specified.
  # o The spec is identical to that of a vector except that a name can not be
  #   specified - its name is always "var".
  # o Var columns are NOT key specific. They work like database specific
  #   global variables in each server instance (i.e., each server in a
  #   database pool has its own set of Var values).
  # o Var columns are initialized to 0/blank. They can also be reset to
  #   0/blank at any time using "aq_udb -clr var".
  # o Var columns can be set using:
  #     $ aq_udb -scn var -var VarName VarVal -var VarName VarVal ...
  #   They can also be imported with:
  #     $ aq_pp -f var_val.csv -imp my_db:var
  # o Var columns can be used in most "aq_udb" operations.
  # o Var columns can be exported using "aq_udb -exp var".
  # o Since each server in a database pool has its own set of Var values, a
  #   "merge" operation (based on the "+FIRST", "+LAST", ..., "+NOZERO" setting)
  #   is done at export to produce a single set of values.
  # o Even tough an export shows a single set of merged result, individual
  #   servers in a database pool still maintain their own values. To set every
  #   server to the exported result, import the result back to the servers.
  #
  @Var:
    s:g_str_1
    l,+bor:g_flag_1
    l,+bor:g_flag_2
    l,+add:g_sum_1
    l,+add:g_sum_2


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udbd <udbd.html>`_ - Udb server
* `aq_udb <aq_udb.html>`_ - Udb server interface

