.. |<br>| raw:: html

   <br>

========
mcc.umod
========

Udb module script compiler


Synopsis
========

::

  mcc.umod in_script [out.c|out.cpp] [out.so]


Description
===========

This is the Udb module script compiler.
It converts a script written in C/C++ and `module commands`_
into a dynamic module for Udb.

This compiler is normally used internally by `aq_udb -mod <aq_udb.html#mod>`_
for on-the-fly module generation. However, it can also be used to develop
modules manually.
Simply install the manually created module (the ``.so`` file) in the
appropriate location and `Udb <udbd.html#server-files>`_ will be able
to use it.


Options
=======

.. _`in_script`:

``in_script``
  Required. The module script to compile.
  If the script come from stdin, set ``in_script`` to '-' (a single dash).


.. _`out.c`:

``out.c|out.cpp``
  Save the intermediate source to an output file. This is a C/C++ source file
  generated based on the input module script. It closely ressembles the
  original script except for some added support/interface code.

  The output file must have a ``.c`` or ``.cpp`` extension.
  Only one of the two can be specified.
  Whether to save this output is optional. Use it for debugging
  or to help module development as needed.


.. _`out.so`:

``out.so``
  Save the final module to an output file. It is the compiled result of the
  intermediate source. The output file must have a ``.so`` extension.


Module Commands
===============

Module commands abstract and hide most of the module API details.
They resemble C macros, as in ``COMMAND(parameters)``.
The commands consist of `declaration statements`_,
`processing function <#processing-functions>`_ specifications and
`module helpers`_.
They tell the module compiler what code to generate
before building the final dynamic module.


Module Script Syntax
====================

A module script is primarily a C/C++ source with certain embedded
`module commands`_.
This is a sample script that normalizes a column:

 ::

  DECL_LANG(C);
  DECL_COLUMN_DYNAMIC(Tab.Col_in_out, F);
  DECL_END;
  MOD_INIT_FUNC()
  {
    if (arg_n != 1) return 0;
    if (!MOD_COLUMN_BIND(Tab.Col_in_out, arg[0])) return 0;
    return 1;
  }
  MOD_KEY_FUNC()
  {
    CDAT_F_T sum;
    sum = 0;
    MOD_TABLE_SCAN(Tab) {
      sum += $Tab.Col_in_out;
    }
    if (sum != 0) {
      MOD_TABLE_SCAN(Tab) {
        $Tab.Col_in_out /= sum;
      }
    }
    return 1;
  }


Column Datatypes
================

Columns are type specific. Column types are defined in the data spec.
In the module script, a C/C++ variable of the appropriate type must
be used when copying or manipulating column values.
These are the Udb column types and their corresponding module
types/*typedefs*:

  +-----------+-----------+-----------+----------------------------------------------+
  | Spec      | Program   | Module    | Description                                  |
  | type      | typedef   | typedef   |                                              |
  +-----------+-----------+-----------+----------------------------------------------+
  | S         | HStr *    | CDAT_S_T  | A pointer to a hash string data structure.   |
  |           |           |           | It represents a stored string value.         |
  +-----------+-----------+-----------+----------------------------------------------+
  | F         | double    | CDAT_F_T  | A double precision floating point number.    |
  +-----------+-----------+-----------+----------------------------------------------+
  | L         | u_int64_t | CDAT_L_T  | An unsigned (always positive) 64bit integer. |
  +-----------+-----------+-----------+----------------------------------------------+
  | LS        | int64_t   | CDAT_LS_T | A 64bit integer.                             |
  +-----------+-----------+-----------+----------------------------------------------+
  | I         | u_int32_t | CDAT_I_T  | An unsigned (always positive) 32bit integer. |
  +-----------+-----------+-----------+----------------------------------------------+
  | IS        | int32_t   | CDAT_IS_T | A 32bit integer.                             |
  +-----------+-----------+-----------+----------------------------------------------+
  | IP        | NetIp     | CDAT_IP_T | An IP address data structure.                |
  +-----------+-----------+-----------+----------------------------------------------+


Declaration Statements
======================

Declaration statements are used to declare variables and options. The compiler
interprets these declarations and determines what code to generate.
For example, column declarations will result in column handling code,
variable declarations will result in variable handling code, and so on.

* Each declaration must start at the *beginning of a line*.
* Each declaration must be given on a single line.
* One declaration per line.


.. _`DECL_LANG()`:

``DECL_LANG(Lang);``
  Tell the compiler what programming language is being used in the script.
  ``Lang`` can either be ``C`` or ``CPP``. Default is ``C``.

  Example:

   ::

    DECL_LANG(C);

  * Specify that C code is being used in the script. ``C`` is the default,
    so this declaration is not strictly necessary.


.. _`DECL_BUILD_OPT()`:

``DECL_BUILD_OPT(Arguments);``
  Supply custom command line arguments for the compiler. Use cases are:

  * Add a custom include path; e.g., ``-Imy_include_directory``.
  * Add a custom ``define``; e.g., ``-DMY_DEF=1``.
  * Link a custom library with the module; e.g., ``my_dir/my_lib.a``.
  * Add a required runtime library; e.g., ``-lm`` for the math library.

  Example:

   ::

    DECL_BUILD_OPT(-DMY_VERSION_STRING='"1.1.1"' -lm);

  * Define the value of "MY_VERSION_STRING".
  * Indicate the need for the math library.


.. _`DECL_COLUMN()`:

``DECL_COLUMN(TabName.ColName, ColType);``
  Declare a column for use in the script.

  * ``TabName.ColName`` is a column in the database.
    The given name and type will be verified at run time
    during module initialization to ensure that the spec is valid.
  * To declare a column from the ``Var`` table, set ``TabName`` to ``Var``.
  * To declare a key column, set ``TabName`` to the special name ``PKEY``
    (all uppercase).
  * Although table and column names are normally case insensitive, they are
    *case sensitive* within the script. This is because table and column names
    are used to compose variable names in the generated code.
    For example, if "MyTable" is a valid table, any case insensitive
    forms of the name (e.g., "mytable") can be used to reference it in the
    script. However, once a form is chosen, the same form should be used
    throughout the script.
  * Use multiple declarations as needed.

  Example:

   ::

    DECL_COLUMN(TabName_1.ColName_1, I);

  * ``TabName_1`` and ``ColName_1`` are actual table and column names.
    They are specified as-is, like a variable (not a string).


.. _`DECL_COLUMN_DYNAMIC()`:

``DECL_COLUMN_DYNAMIC(TabName.ColName, ColType);``
  Declare a column for the script just like `DECL_COLUMN()`_, except that the
  actual target table and column names are not known until run time
  (hence, *dynamic*).

  * This statement essentially declares a column variable.
    `MOD_COLUMN_BIND()`_ must be called at run time to bind the
    column variable to the desired column by name.
  * Use multiple declarations as needed.

  Example:

   ::

    DECL_COLUMN_DYNAMIC(Tab.Col_in_out, F);
    MOD_INIT_FUNC()
    {
      if (!MOD_COLUMN_BIND(Tab.Col_in_out, "RealTable.RealColumn")) return 0;
      ...
    }

  * Declare a dynamic column. Then resolve it at run time during module
    initialization.


.. _`DECL_DATA()`:

``DECL_DATA(VarDecl);``
  Declare one or more variables as the module's *instance specific* data.
  Unlike global variables which are *shared* between concurrent instances
  of the same module, variables declared this way are *instance specific*
  (i.e., each instance has its own copies of the variables).
  This is the recommended way of managing module data.

  * ``VarDecl`` is a variable declaration like ``int num1, num2``.
  * Declared variables can later be referenced useing the `MOD_DATA()`_
    macro; e.g., ``MOD_DATA(num1)`` and ``MOD_DATA(num2)`` will access
    the values of those integers.
  * Declared variables are automatically initialized to 0.
    Initialize them manually in `MOD_INIT_FUNC()`_ if a different initial
    value is desired.
  * Use multiple declarations as needed.

  Example:

   ::

    DECL_DATA(int flag);
    DECL_DATA(int num1, num2);
    MOD_INIT_FUNC()
    {
      if (...) MOD_DATA(flag) = 1; else MOD_DATA(flag) = 2;
      ...
    }
    MOD_ROW_FUNC(TabName_1)
    {
      if (MOD_DATA(flag) == 1) MOD_DATA(num1) += 1;
      else if (MOD_DATA(flag) == 2) MOD_DATA(num2) += 1;
      ...
    }

  * Declare 3 instance variables. ``flag`` is conditionally initialized to
    1 or 2 during module initialization. ``num1`` and ``num2`` are already
    initialized to 0 automatically.
  * The variables are then used in a row function.


.. _`DECL_END`:

``DECL_END;``
  Mark the end of module declarations. The compiler will generated and
  insert the module data declaration code.
  If this is not given, declaration code will be inserted in front of the
  first `processing function <#processing-functions>`_.


Processing Functions
====================

The processing functions carry out the intended task of a module.
There are several predefined module functions - one optional initialization
function, one or more processing functions and one optional wrap up function.
If any of them are defined, the compiler will generate code that call these
function automatically.

A module function is defined like a C function:

 ::

  PREDEFINED_FUNCTION_NAME(function_dependent_argument)
  {
    code_block
    ...
  }

* The first line is the function name (one of the ``MOD_*_FUNC()``)
  and argument (function dependent) specification.
* The function name must start at the *beginning of a line*.
* A code block enclosed in "{ ... }" must follow the specification line.
* The code block can be written in C/C++. It can make use of the helpers
  described below (and in "``etc/include/umod.h``").


.. _`MOD_INIT_FUNC()`:

``MOD_INIT_FUNC()``
  Define a function for module initialization.

  * It is called once during module preparation.
  * It is called with these implicit arguments:

    * ``ModCntx *mod`` - A module instance handle. Pass this to any support
      functions that use `module helpers`_.
    * ``const char *const *arg, int arg_n`` - The parameters passed to the
      module when it was called on the command line is available here as a
      string array. Use them to set up run time parameters as necessary.

  * It must return an integer:

    * 1 - Success.
    * 0 - Failure. The relevant Udb action will terminate.

  Example:

   ::

    MOD_INIT_FUNC()
    {
      if (arg_n != 1) return 0;
      if (!MOD_COLUMN_BIND(Tab.Col_in_out, arg[0])) return 0;
      return 1;
    }

  * Bind the dynamic column``Tab.Col_in_out`` to the name given as the
    first argument to the module (recall that ``arg`` and ``arg_n``
    are implicit variables in the function).


.. _`MOD_KEY_FUNC()`:

``MOD_KEY_FUNC()``
  Define a function for key-level processing
  during an Udb export/count/scan operation.

  * It is called as each key is processed.
  * Use it to scan tables associated with the current key, examine and/or modify
    column values, and so on.
  * It is called with this implicit argument:

    * ``ModCntx *mod`` - A module instance handle. Pass this to any support
      functions that use `module helpers`_.

  * It must return an integer that tells Udb what to do:

    * 1 - Success. Udb will continue normal processing.
    * 0 - Failure. Udb will stop processing the current key
      and skip to the next one.

  Example:

   ::

    MOD_KEY_FUNC()
    {
      CDAT_F_T sum;
      sum = 0;
      MOD_TABLE_SCAN(Tab) {
        sum += $Tab.Col_in_out;
      }
      if (sum != 0) {
        MOD_TABLE_SCAN(Tab) {
          $Tab.Col_in_out /= sum;
        }
      }
      return 1;
    }

  * Convert the value of numeric column ``Tab.Col_in_out`` to a per-key
    average.
  * Note the use of ``$TabName.ColName`` (or `MOD_CDAT()`_) to address a
    column's value.


.. _`MOD_ROW_FUNC()`:

``MOD_ROW_FUNC(TabName)``
  Define a function for row processing during
  an Udb export/count/scan operation on ``TabName``.

  * It is called for each row of ``TabName`` for each key.
  * Use it examine and/or modify column values of the row being
    exported/counted/scanned.
  * Within the processing code, tables can be scanned, column values can be
    examined and/or modified, and so on.
  * On each call, the row iterator of ``TabName`` is automatically set to the
    relevant row. For this reason, do not use `MOD_TABLE_SCAN()`_ or
    `MOD_TABLE_SET()`_ on ``TabName``. If a ``TabName`` scan is needed,
    use `DECL_COLUMN_DYNAMIC()`_ and `MOD_COLUMN_BIND()`_ to bind the same
    table to another name and scan using that name instead.
  * It is called with this implicit argument:

    * ``ModCntx *mod`` - A module instance handle. Pass this to any support
      functions that use `module helpers`_.

  * It must return an integer that tells Udb what to do:

    * 1 - Success. Udb will continue normal processing.
    * 0 - Failure. Udb will stop processing the current row
      and skip to the next one.

  Example:

   ::

    MOD_ROW_FUNC(TabName_1)
    {
      if ($TabName_1.ColName_1 >= 100 &&
          $TabName_1.ColName_1 <= 199) return 1;
      return 0;
    }

  * This demonstrates a simple filter on a column value - keep row if
    ``ColName_1`` is between 100 and 199, discard otherwise.
  * Note the use of ``$TabName.ColName`` (or `MOD_CDAT()`_) to address a
    column's value.


.. _`MOD_VALUE_FUNC()`:

``MOD_VALUE_FUNC(TabName)``
  Define a function that checks whether to import the input values
  of a new row during an Udb import operation on ``TabName``.

  * It is called *before* a new row is added to ``TabName`` for a key.
  * Use it to examine the new input values and determine whether to add a
    new row.
    The input values are available via the `MOD_IMP_CDAT()`.
    These values should be considered *readonly*.
  * Within the processing code, tables can be scanned, column values can be
    examined and/or modified, and so on.
    However, table access is not applicable if:

    * The key corresponding to the input does not yet exist.
      This can be determined using `MOD_HAS_KEY`_.
    * The import is being done on the global ``Var`` table.

  * It is called with this implicit argument:

    * ``ModCntx *mod`` - A module instance handle. Pass this to any support
      functions that use `module helpers`_.

  * It must return an integer that tells Udb what to do:

    * 1 - Success. Udb will continue with the import operation.
    * 0 - Reject. Udb will discard the new values.

  Example:

   ::

    MOD_VALUE_FUNC(TabName_1)
    {
      if (MOD_IMP_CDAT(TabName_1.ColName_1) >= 100 &&
          MOD_IMP_CDAT(TabName_1.ColName_1) <= 199) return 1;
      return 0;
    }

  * This demonstrates a simple filter on an input value - keep new values if
    ``ColName_1`` is between 100 and 199, discard otherwise.
  * Note the use of `MOD_IMP_CDAT()`_ to address a column's input value.


.. _`MOD_MERGE_FUNC()`:

``MOD_MERGE_FUNC(TabName)``
  Define a function that checks whether to merge the input values
  of a new row into an existing data row during an Udb import operation on
  ``TabName``.

  * It is called *before* the input values are merged into an existing row
    in ``TabName`` for a key.
  * Use it to examine the new input values as well as existing column values
    and determine whether to merge in the new values.
    The input values are available via `MOD_IMP_CDAT()`.
    These values should be considered *readonly*.
    The existing column values are available via `MOD_CDAT()`_.
  * Within the processing code, tables can be scanned, column values can be
    examined and/or modified, and so on.
  * On each call, the row iterator of ``TabName`` is automatically set to the
    existing row. For this reason, do not use `MOD_TABLE_SCAN()`_ or
    `MOD_TABLE_SET()`_ on ``TabName``. If a ``TabName`` scan is needed,
    use `DECL_COLUMN_DYNAMIC()`_ and `MOD_COLUMN_BIND()`_ to bind the same
    table to another name and scan using that name instead.
  * It is called with this implicit argument:

    * ``ModCntx *mod`` - A module instance handle. Pass this to any support
      functions that use `module helpers`_.

  * It must return an integer that tells Udb what to do:

    * 1 - Success. Udb will proceed with the merge operation.
    * 0 - No further action needed. This could mean that the function has
      performed the merge by itself or that the input values are not desired.

  Example:

   ::

    MOD_MERGE_FUNC(TabName_1)
    {
      if (MOD_IMP_CDAT(TabName_1.ColName_1) == $TabName_1.ColName_1) return 1;
      return 0;
    }

  * This demonstrates a simple test - keep new values if
    the new ``ColName_1`` is the same as the existing one, discard otherwise.
  * Note the use of `MOD_IMP_CDAT()`_ to address a column's input value
    and ``$TabName.ColName`` (or `MOD_CDAT()`_) to address a column's
    existing value.


.. _`MOD_DONE_FUNC()`:

``MOD_DONE_FUNC()``
  Define a function that performs module wrap up related tasks.
  Udb unloads the module.

  * It is called once right before Udb unloads the module.
  * Use it for reporting and data cleanup.
  * It is called with this implicit argument:

    * ``ModCntx *mod`` - A module instance handle. Pass this to any support
      functions that use `module helpers`_.

  * This is a void function, no return value is needed.

  Example:

   ::

    MOD_DONE_FUNC()
    {
      ModLog("%s done\n", MOD_NAME);
    }

  * Print a message to the Udb server log at module completion.


Module Helpers
==============

These are helpers that are designed specifically for module processing tasks.
They can be used in any `processing functions`_ or subroutines called
from these functions (these subroutines must be given a ``ModCntx *mod``
argument).


.. _`MOD_COLUMN_BIND()`:

``int MOD_COLUMN_BIND(TabName.ColName, const char *real_name)``
  Dynamic column setup function.

  * ``TabName.ColName`` must ba a column declared via `DECL_COLUMN_DYNAMIC()`_.
  * ``real_name`` is a C string containing the actual table dot column name.
  * Returns 1 if successful, 0 otherwise.
  * It should be called before the desired column is used,
    usually during module initialization.
  * See `MOD_INIT_FUNC()`_ for an usage example.


.. _`MOD_TABLE_SCAN()`:

``MOD_TABLE_SCAN(TabName) { ... }``
  A macro that expands to a ``for`` loop over all rows of the given table.

  * ``TabName`` must be a table declared via `DECL_COLUMN()`_ or
    `DECL_COLUMN_DYNAMIC()`_.
  * There is an implicit row iterator. References to any column values
    within the loop implicitly refer to the row iterator's values.
  * Usually followed by the loop content - a code block enclosed in "{ ... }".
  * See `MOD_KEY_FUNC()`_ for an usage example.


.. _`MOD_TABLE_SET()`:

``MOD_TABLE_SET(TabName)``
  A macro that sets the row iterator of the given table to the first
  row of the table. No return value.

  * ``TabName`` must be a table declared via `DECL_COLUMN()`_ or
    `DECL_COLUMN_DYNAMIC()`_.
  * This is often used to access a vector where scanning (a ``for`` loop)
    is not necessary.

  Example:

   ::

    DECL_COLUMN(TabName_1.ColName_1, I);
    DECL_COLUMN(VecName_2.ColName_1, I);
    MOD_KEY_FUNC()
    {
      CDAT_I_T sum;
      sum = 0;
      MOD_TABLE_SCAN(TabName_1) {
        sum += $TabName_1.ColName_1;
      }
      MOD_TABLE_SET(VecName_2);
      $VecName_2.ColName_1 = sum;
      ...
    }

  * Save the sum of ``TabName_1.ColName_1`` over all rows of ``TabName_1``
    to vector column ``VecName_2.ColName_1``.


.. _`MOD_ROW()`:

``RowData *MOD_ROW(TabName)``
  A macro that returns the current row iterator of the given table.

  * ``TabName`` must be a table declared via `DECL_COLUMN()`_ or
    `DECL_COLUMN_DYNAMIC()`_.
  * It can be used after calling `MOD_TABLE_SCAN()`_ or
    `MOD_TABLE_SET()`_ on the desired table.
  * It can also be used in `MOD_ROW_FUNC()`_ and `MOD_MERGE_FUNC()`_
    to address the row being exported/counted/scanned/merged
    without calling `MOD_TABLE_SCAN()`_ or `MOD_TABLE_SET()`_.

  Example:

   ::

    DECL_COLUMN(TabName_1.ColName_1, I);
    MOD_KEY_FUNC()
    {
      MOD_TABLE_SET(TabName_1);
      if (!MOD_ROW(TabName_1)) return 0;
      ...
    }

  * With this logic, a key is skipped if it's ``TabName_1`` is empty.


.. _`MOD_CDAT()`:

``CDAT_*_T MOD_CDAT(TabName.ColName)``, ``CDAT_*_T $TabName.ColName``
  Use either form like a program variable to address the value of a column
  declared via `DECL_COLUMN()`_ or `DECL_COLUMN_DYNAMIC()`_.

  * The variable will have a ``CDAT_*_T`` type (see `column datatypes`_)
    derived from the ``ColType`` in the declaration.
  * Applicable after calling `MOD_TABLE_SCAN()`_ or
    `MOD_TABLE_SET()`_ on the relevant table.
  * Also applicable in `MOD_ROW_FUNC()`_ and `MOD_MERGE_FUNC()`_
    to address columns of the row being exported/counted/scanned/merged
    without calling `MOD_TABLE_SCAN()`_ or `MOD_TABLE_SET()`_.

  Example:

   ::

    DECL_COLUMN(TabName_1.InNumColumn, I);
    DECL_COLUMN_DYNAMIC(TabName_1.OutNumColumn, I);
    MOD_INIT_FUNC()
    {
      MOD_COLUMN_BIND(TabName_1.OutNumColumn, "TabName_1.RealColumn");
      ...
    }
    MOD_ROW_FUNC(TabName_1)
    {
      if ($TabName_1.InNumColumn == 4321) $TabName_1.OutNumColumn += 1;
      ...
    }

  * Examine and change column values.


.. _`MOD_IMP_CDAT()`:

``CDAT_*_T MOD_IMP_CDAT(TabName.ColName)``
  Use this like a program variable to address the input value of a column
  declared via `DECL_COLUMN()`_ or `DECL_COLUMN_DYNAMIC()`_.

  * The variable will have a ``CDAT_*_T`` type (see `column datatypes`_)
    derived from the ``ColType`` in the declaration.
  * Only applicable within `MOD_VALUE_FUNC()`_ and `MOD_MERGE_FUNC()`_.

  Example:

   ::

    MOD_VALUE_FUNC(TabName_1)
    {
      if (MOD_IMP_CDAT(TabName_1.ColName_1) < 100) return 0;
      ...
    }

  * Test an input column value to determine whether to import.


.. _`MOD_HAS_KEY`:

``int MOD_HAS_KEY``
  A marco that evaluates to 1 if a relevant key exists, 0 otherwise.


.. _`MOD_CDAT_S_NSET()`:

``void MOD_CDAT_S_NSET(TabName.ColName, const char *b, unsigned int n)``
  Set the value of a string column represented by ``TabName.ColName`` to a
  hash string based on string buffer ``b`` and length ``n``.

  Example:

   ::

    DECL_COLUMN(TabName_1.StrColumn_1, S);
    MOD_ROW_FUNC(TabName_1)
    {
      MOD_CDAT_S_NSET(TabName_1.StrColumn_1, "abc", 3);
      ...
    }

  * Alter the value of a string column.


.. _`MOD_CDAT_S_SET()`:

``void MOD_CDAT_S_SET(TabName.ColName, CDAT_S_T hs)``
  Set the value of a string column represented by ``TabName.ColName`` to a
  copy of hash string ``hs``.

  * ``hs`` is an existing hash string (e.g., the value of another string
    column).

  Example:

   ::

    DECL_COLUMN(TabName_1.StrColumn_1, S);
    DECL_COLUMN(TabName_1.StrColumn_2, S);
    MOD_ROW_FUNC(TabName_1)
    {
      MOD_CDAT_S_SET(TabName_1.StrColumn_1, $TabName_1.StrColumn_2);
      ...
    }

  * Alter the value of a string column.


.. _`MOD_CDAT_S_DEL()`:

``void MOD_CDAT_S_DEL(TabName.ColName)``
  Set the value of a string column represented by ``TabName.ColName`` to a
  generic *blank* hash string.


.. _`MOD_CDEF()`:

``const ColDefn *MOD_CDEF(TabName.ColName)``
  A macro that returns the column definition of the given column.


.. _`MOD_DATA()`:

``MOD_DATA(variable)``
  Access a variable previously defined with `DECL_DATA()`_.
  See `DECL_DATA()`_ for an usage example.


.. _`MOD_NAME`:

``const char *MOD_NAME``
  A marco respresenting the module name string.
  See `ModLog()`_ for an usage example.


.. _`MOD_LOG_ERR()`:

``MOD_LOG_ERR(const char *format, ...)``
  Print a message to the Udb server log.
  If it is called during module initialization, the same message will be
  returned to the client.

  Example:

   ::

    MOD_INIT_FUNC()
    {
      if (arg_n != 1) {
        MOD_LOG_ERR("missing module argument");
        return 0;
      }
      ...
    }

  * Report module initialization error to the server log and client.


General Helpers
===============

Generic programming supports and convenient functions for module specific
datatype handling.
Note that any memory allocated by the module must be deallocated with
``free()`` before the module is unloaded (see `MOD_DONE_FUNC()`_).


.. _`ModDifHStr()`:

``int ModDifHStr(const CDAT_S_T hs1, const CDAT_S_T hs2, int dif_flag)``
  Compare the values of 2 hash strings.

  * Returns 0 if they are the same, 1 if ``hs1`` is greater, and -1 otherwise.
  * ``dif_flag`` is either 0 (case sensitive comparision) or
    DIF_A_NCAS (case insensitive comparison).

  Example:

   ::

    DECL_COLUMN(TabName_1.StrColumn_1, S);
    DECL_COLUMN(TabName_1.StrColumn_2, S);
    MOD_ROW_FUNC(TabName_1)
    {
      if (ModDifHStr($TabName_1.StrColumn_1, $TabName_1.StrColumn_2, 0) == 0) ...
      ...
    }

  * Compare (case sensitive) the values of 2 string columns.


.. _`ModDifHStrStr()`:

``int ModDifHStrStr(const CDAT_S_T hs, const char *b, int n, int dif_flag)``
  Compare the value of hash string ``hs`` to string buffer ``b`` of
  length ``n``.

  * Returns 0 if they are the same, 1 if ``hs`` is greater, and -1 otherwise.
  * ``dif_flag`` is either 0 (case sensitive comparision) or
    DIF_A_NCAS (case insensitive comparison).

  Example:

   ::

    DECL_COLUMN(TabName_1.StrColumn_1, S);
    MOD_ROW_FUNC(TabName_1)
    {
      if (ModDifHStrStr($TabName_1.StrColumn_1, "abc", 3, 0) == 0) ...
      ...
    }

  * Compare (case sensitive) the value of a string column to a known value.


.. _`ModDifHStrPat()`:

``int ModDifHStrPat(const CDAT_S_T hs, const char *pat, int n, int dif_flag)``
  Compare the value of hash string ``hs`` to pattern buffer ``pat`` of
  length ``n``.

  * ``pat`` may contain '*' (for any number of bytes) and '?'
    (for any 1 byte). Use a '\' to escape literal '*', '?' and '\\' in the
    pattern. If the pattern is given as a literal, any backslashes in it
    must be backslash escaped one more time for the C/C++ interpreter.
  * Returns 0 if they matches, non-zero otherwise.
  * ``dif_flag`` can have these values:

    * DIF_A_NCAS - Do case insensitive instead of case sensitive comparison.
    * DIF_A_LIKE - Use '%' and '_' instead of '*' and '?' as the wildcard
      characters.

  Example:

   ::

    DECL_COLUMN(TabName_1.StrColumn_1, S);
    MOD_ROW_FUNC(TabName_1)
    {
      if (ModDifHStrPat($TabName_1.StrColumn_1, "a*c", 3, 0) == 0) ...
      ...
    }

  * Compare (case sensitive) the value of a string column to a pattern.


.. _`ModDifIp()`:

``int ModDifIp(const CDAT_IP_T *ip1, const CDAT_IP_T *ip2)``
  Compare the values of 2 IP addresses.
  Note that the arguments are pointers to IP address structures.

  * Returns 0 if they are the same, 1 if ``ip1`` is greater, and -1 otherwise.

  Example:

   ::

    DECL_COLUMN(TabName_1.IPColumn_1, IP);
    DECL_COLUMN(TabName_1.IPColumn_2, IP);
    MOD_ROW_FUNC(TabName_1)
    {
      if (ModDifIp(&$TabName_1.IPColumn_1, &$TabName_1.IPColumn_2) == 0) ...
      ...
    }

  * Compare the values of two IP columns.
    Note that pointers to the column values are passed to the function.


.. _`ModLog()`:

``void ModLog(const char *format, ...)``
  Print a message to the Udb server log.

  Example:

   ::

    MOD_INIT_FUNC()
    {
      if (arg_n != 1) {
        ModLog("%s: missing module argument\n", MOD_NAME);
        return 0;
      }
      ...
    }

  * Report a message to server log during module initialization.


.. _`ZAlloc()`:

``void *ZAlloc(size_t size)``
  Allocate ``size`` bytes of memory. This is the same as the C function
  ``malloc()`` except that the returned memory is initialized to zero.


.. _`ZALLOC_TYPE()`:

``Type *ZALLOC_TYPE(Type)``
  Allocate an object of type ``Type``. This is a macro based on
  `ZAlloc()`_.


.. _`ZALLOC_TYPE_N()`:

``Type *ZALLOC_TYPE_N(Type, int num)``
  Allocate ``num`` object of type ``Type``. This is a macro based on
  `ZAlloc()`_.


.. _`ReAlloc()`:

``int ReAlloc(void *orig_mem, size_t new_size)``
  This function works like a combination of the C functions
  ``malloc()`` and ``realloc()`` - it allocates ``new_size`` bytes if the
  original memory address is NULL or reallocates to ``new_size`` otherwise.

  * ``orig_mem`` is the *address* of the original memory address
    (i.e., an address of an address).
  * Returns 1 if successful, 0 otherwise.
    The original memory is not altered on failure.


.. _`StrNDup()`:

``char *StrNDup(const char *b, int n)``
  Duplicate a data buffer ``b`` of length ``n`` (i.e., allocate memory and
  copy data).

  * The resulting string is null terminated.
  * Special cases:

    * If ``b`` is NULL, NULL is returned regardless of the value of ``n``.
    * If ``n`` is greater than or equal to 0, ``b`` needs not be null
      terminated.
    * If ``n`` is less than 0, ``b`` must be null terminated. The string length
      of ``b`` will be used as the data length.


.. _`BUF_INIT()`:

``BUF_INIT(BufData *buf)``
  This is a macro that initializes (i.e., zeroes out) a ``BufData`` structure.
  This should be done on any uninitialized ``BufData`` structure before it is
  used for the first time.


.. _`BUF_CLEAR()`:

``BUF_CLEAR(BufData *buf)``
  This is a macro that clears (i.e., frees) the memory used by the buffer in
  a ``BufData`` structure. Do this before destroying a ``BufData`` structure.


.. _`BufNCat()`:

``int BufNCat(BufData *buf, const char *b, int n)``
  Append data buffer ``b`` of length ``n`` to the buffer in
  ``BufData`` structure ``buf``.

  * Returns 1 if successful, 0 otherwise.
  * The resulting ``buf->s`` string is null terminated.
  * Special cases:

    * If ``b`` is NULL, the size of ``buf->s`` will be increased by ``n``
      (if necessary), but no data will be copied. In other words,
      ``buf->s`` and ``buf->z`` may change, but ``buf->n`` will not.
    * If ``n`` is greater than or equal to 0, ``b`` needs not be null
      terminated.
    * If ``n`` is less than 0, ``b`` must be null terminated. The string length
      of ``b`` will be used as the data length.


.. _`HStrNSet()`:

``void HStrNSet(const ColDefn *col, CDAT_S_T *hs, const char *b, unsigned int n)``
  Replace hash string ``hs`` with one based on string buffer ``b`` and
  length ``n``.

  * ``hs`` must have a value on input - either a valid hash string or 0.
  * If ``hs`` is the value of a column, specify the relevant column definition
    as ``col``. This is similar to what `MOD_CDAT_S_NSET()`_ does.
  * If ``hs`` is not the value of a column, set ``col`` to 0.
  * Use `HStrSet()`_ and `HStrDel()`_ for further hash string operations.

  Example:

   ::

    DECL_DATA(CDAT_S_T my_str);
    MOD_INIT_FUNC()
    {
      HStrNSet(0, &MOD_DATA(my_str), "abc", 3);
      ...
    }
    ...
    MOD_DONE_FUNC()
    {
      HStrDel(0, &MOD_DATA(my_str));
      ...
    }

  * Initialize a global variable's value to a hash string. Then delete at the
    end.


.. _`HStrSet()`:

``void HStrSet(const ColDefn *col, CDAT_S_T *hs, CDAT_S_T s)``
  Replace hash string ``hs`` with a copy of ``s``.

  * ``hs`` must have a value on input - either a valid hash string or 0.
  * If ``hs`` is the value of a column, specify the relevant column definition
    as ``col``. This is similar to what `MOD_CDAT_S_SET()`_ does.
  * If ``hs`` is not the value of a column, set ``col`` to 0.
  * Use `HStrNSet()`_ and `HStrDel()`_ for further hash string operations.


.. _`HStrDel()`:

``void HStrDel(const ColDefn *col, CDAT_S_T *hs)``
  Delete (dereference) hash string ``hs``. ``hs`` will be set to a generic
  *blank* hash string on return.

  * ``hs`` must have a value on input - either a valid hash string or 0.
  * If ``hs`` is the value of a column, specify the relevant column definition
    as ``col``. This is similar to what `MOD_CDAT_S_DEL()`_ does.
  * If ``hs`` is not the value of a column, set ``col`` to 0.
  * Use `HStrNSet()`_ and `HStrSet()`_ for further hash string operations.


Additional Supports
===================

Additional resources can be found in the low level include file
"``etc/include/umod.h``".


Name versus $Name
=================

The ability to address columns by their names is a key feature of
the module script API. Both ``TabName.ColName`` and ``$TabName.ColName``
are designed to address columns, but they differ in these ways:

* ``TabName.ColName`` (without the leading dollar sign) refers to an
  abstract column reference.
  It is only valid in `module helpers`_.

* ``$TabName.ColName`` (with the leading dollar sign) is a shorthand for
  ``MOD_CDAT(TabName.ColName)``. It refers to a column's value.
  It acts like a program variable of type ``CDAT_*_T``
  (see `column datatypes`_). It can be used anywhere
  program variables are appropriate.


See Also
========

* `udbd <udbd.html>`_ - Udb server
* `aq_udb <aq_udb.html>`_ - Udb server interface

