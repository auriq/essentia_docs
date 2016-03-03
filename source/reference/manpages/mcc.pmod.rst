========
mcc.pmod
========

aq_pp module script compiler


Synopsis
========

::

  mcc.pmod in_script [out.c|out.cpp] [out.so]


Description
===========

This is the ``aq_pp`` module script compiler.
It converts a script written in C/C++ and `module commands`_
into a dynamic module for ``aq_pp``.

This compiler is normally used internally by `aq_pp -pmod <aq_pp.html#pmod>`_
for on-the-fly module generation. However, it can also be used to develop
modules manually.
Simply install the manually created module (the ``.so`` file) in the
appropriate location and `aq_pp -pmod <aq_pp.html#pmod>`_ will be able
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
`processing function <processing functions_>`_ specifications and
`module helpers`_.
They tell the module compiler what code to generate
before building the final dynamic module.


Module Script Syntax
====================

A module script is primarily a C/C++ source with certain embedded
`module commands`_.
This is a sample script that does row filtering:

 ::

  DECL_LANG(C);
  DECL_COLUMN(ColName_1, S);
  DECL_COLUMN(ColName_2, I);
  DECL_COLUMN_DYNAMIC(Col_3, S);
  DECL_END;
  MOD_INIT_FUNC()
  {
    if (arg_n != 1) return 0;
    if (!MOD_COLUMN_BIND(Col_3, arg[0])) return 0;
    return 1;
  }
  MOD_PROC_FUNC()
  {
    CDAT_I_T col_i;
    col_i = $ColName_2;
    if (ModDifHStr($ColName_1, $Col_3, DIF_A_NCAS) == 0 &&
        col_i >= 100  && col_i <= 199) return MOD_A_TRUE;
    return MOD_A_FALSE;
  }


Column Datatypes
================

Columns are type specific. Column types are defined in the data spec.
In the module script, a C/C++ variable of the appropriate type must
be used when copying or manipulating column values.
These are the ``aq_pp`` column types and their corresponding module
types/*typedefs*:

  +-----------+-----------+-----------+----------------------------------------------+
  | Spec      | Program   | Module    | Description                                  |
  | type      | typedef   | typedef   |                                              |
  +-----------+-----------+-----------+----------------------------------------------+
  | S         | HStr *    | CDAT_S_T  | A pointer to a hash string data structure.   |
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

``DECL_COLUMN(ColName, ColType);``
  Declare a column for use in the script.

  * ``ColName`` is a column in the data spec.
    The given name and type will be verified at run time
    during module initialization to ensure that the spec is valid.
  * Although column names are normally case insensitive, they are
    *case sensitive* within the script. This is because column names
    are used to compose variable names in the generated code.
    For example, if "MyColumn" is a valid column, any case insensitive
    forms of the name (e.g., "mycolumn") can be used to reference it in the
    script. However, once a form is chosen, no other forms should be used
    to reference the same column.
  * Use multiple declarations as needed.

  Example:

   ::

    DECL_COLUMN(ColName_1, S);

  * ``ColName_1`` is an actual column name.
    It is specified as-is, like a variable (not a string).


.. _`DECL_COLUMN_DYNAMIC()`:

``DECL_COLUMN_DYNAMIC(ColName, ColType);``
  Declare a column for the script just like `DECL_COLUMN()`_, except that the
  actual target column name is not known until run time
  (hence, *dynamic*).

  * This statement essentially declares a column variable.
    `MOD_COLUMN_BIND()`_ must be called at run time to bind the
    column variable to the desired column by name.
  * Use multiple declarations as needed.

  Example:

   ::

    DECL_COLUMN_DYNAMIC(Col_3, S);
    MOD_INIT_FUNC()
    {
      if (!MOD_COLUMN_BIND(Col_3, "ColName_3")) return 0;
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
  first `processing function <processing functions_>`_.


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
  described below (and in "``etc/include/pmod.h``").


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
    * 0 - Failure. ``aq_pp`` will terminate.

  Example:

   ::

    MOD_INIT_FUNC()
    {
      if (arg_n != 1) return 0;
      if (!MOD_COLUMN_BIND(Col_3, arg[0])) return 0;
      return 1;
    }

  * Bind the dynamic column``Col_3`` to the column name given as the
    first argument to the module (recall that ``arg`` and ``arg_n``
    are implicit variables in the function).


.. _`MOD_PROC_FUNC()`:

``MOD_PROC_FUNC()``
  Define a function for data row processing.
  This function must be defined.

  * It is called for each data row being processed.
  * Use it to examine and/or modify column values.
  * It is called with this implicit argument:

    * ``ModCntx *mod`` - A module instance handle. Pass this to any support
      functions that use `module helpers`_.

  * It must return a enumerated return code that tells ``aq_pp`` what to do:

    * MOD_A_TRUE - True. ``aq_pp`` will continue processing or take "if"
      statement dependent actions if the module is used as an "if" condition.
    * MOD_A_FALSE - False. ``aq_pp`` will skip any remaining processing on the
      current row or take "if" statement dependent actions if the module is
      used as an "if" condition.
    * MOD_A_QNOW - Quit now. ``aq_pp`` will stop processing immediately.
    * MOD_A_QAFT - Like MOD_A_TRUE, but the call will stop processing after
      finishing the current row.
    * MOD_A_REPT - Like MOD_A_TRUE, but ``aq_pp`` will call the module again
       with the current row until a different code is returned.

  Example:

   ::

    MOD_PROC_FUNC()
    {
      CDAT_I_T col_i;
      col_i = $ColName_2;
      if (ModDifHStr($ColName_1, $Col_3, DIF_A_NCAS) == 0 &&
          col_i >= 100  && col_i <= 199) return MOD_A_TRUE;
      return MOD_A_FALSE;
    }

  * This implements a simple filtering logic - true if ``ColName_1``
    and ``Col_3``'s values are the same (case insensitive) and
    ``ColName_2``'s value is between 100 and 199, false otherwise.
  * Note the use of ``$ColName`` (or `MOD_CDAT()`_) to address
    column values.
  * Note the use of support function `ModDifHStr()`_ for string column
    comparison.


.. _`MOD_DONE_FUNC()`:

``MOD_DONE_FUNC()``
  Define a function that performs module wrap up related tasks.

  * It is called once right before ``aq_pp`` exits.
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

  * Print a message to stderr at module completion.


Module Helpers
==============

These are helpers that are designed specifically for module processing tasks.
They can be used in any `processing functions`_ or subroutines called
from these functions (these subroutines must be given a ``ModCntx *mod`` 
argument).


.. _`MOD_COLUMN_BIND()`:

``int MOD_COLUMN_BIND(ColName, const char *real_name)``
  Dynamic column setup function.

  * ``ColName`` must ba a column declared via `DECL_COLUMN_DYNAMIC()`_.
  * ``real_name`` is a C string buffer containing the actual name of the column.
  * Returns 1 if successful, 0 otherwise.
  * It should be called before the desired column is used,
    usually during module initialization.
  * See `MOD_INIT_FUNC()`_ for an usage example.


.. _`MOD_CDAT()`:

``CDAT_*_T MOD_CDAT(ColName)``, ``CDAT_*_T $ColName``
  Use either form like a program variable to address the value of a column
  declared via `DECL_COLUMN()`_ or `DECL_COLUMN_DYNAMIC()`_.

  * The variable will have a ``CDAT_*_T`` type (see `column datatypes`_)
    derived from the ``ColType`` in the declaration.

  Example:

   ::

    DECL_COLUMN(InNumColumn, I);
    DECL_COLUMN_DYNAMIC(OutNumColumn, I);
    MOD_INIT_FUNC()
    {
      MOD_COLUMN_BIND(OutNumColumn, "RealColumn");
      ...
    }
    MOD_PROC_FUNC()
    {
      if ($InNumColumn == 4321) $OutNumColumn += 1;
      ...
    }

  * Examine and change column values.


.. _`MOD_CDAT_S_SET()`:

``void MOD_CDAT_S_SET(ColName, CDAT_S_T hs)``
  Set the value of a string column represented by ``ColName``
  to hash string ``hs``.

  * ``hs`` can be the value of another string column (e.g., ``$StrColumn``)
    or a hash string created using `HStrNAdd()`_.

  Example:

   ::

    DECL_COLUMN(StrColumn_1, S);
    DECL_COLUMN(StrColumn_2, S);
    DECL_COLUMN(StrColumn_3, S);
    MOD_PROC_FUNC()
    {
      CDAT_S_T str;
      str = HStrNAdd("abc", 3);
      MOD_CDAT_S_SET(StrColumn_1, str);
      MOD_CDAT_S_SET(StrColumn_2, $StrColumn_3);
      ...
    }

  * Alter the value of two string columns.


.. _`MOD_CDAT_S_NADD()`:

``void MOD_CDAT_S_NADD(ColName, const char *b, unsigned int n)``
  Set the value of a string column represented by ``ColName``
  to a hash string based on string buffer ``b`` of length ``n``.

  Example:

   ::

    DECL_COLUMN(StrColumn_1, S);
    MOD_PROC_FUNC()
    {
      MOD_CDAT_S_NADD(StrColumn_1, "abc", 3);
      ...
    }

  * Alter the value of a string column.


.. _`MOD_CDEF()`:

``const ColDefn *MOD_CDEF(ColName)``
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
  Same as `ModLog()`_.


General Helpers
===============

Generic programming supports and convenient functions for module specific
datatype handling.


.. _`ModDifHStr()`:

``int ModDifHStr(const CDAT_S_T hs1, const CDAT_S_T hs2, int dif_flag)``
  Compare the values of 2 hash strings.

  * Returns 0 if they are the same, 1 if ``hs1`` is greater, and -1 otherwise.
  * ``dif_flag`` is either 0 (case sensitive comparision) or
    DIF_A_NCAS (case insensitive comparison).

  Example:

   ::

    DECL_COLUMN(StrColumn_1, S);
    DECL_COLUMN(StrColumn_2, S);
    MOD_PROC_FUNC()
    {
      if (ModDifHStr($StrColumn_1, $StrColumn_2, 0) == 0) ...
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

    DECL_COLUMN(StrColumn_1, S);
    MOD_PROC_FUNC()
    {
      if (ModDifHStrStr($StrColumn_1, "abc", 3, 0) == 0) ...
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

    DECL_COLUMN(StrColumn_1, S);
    MOD_PROC_FUNC()
    {
      if (ModDifHStrPat($StrColumn_1, "a*c", 3, 0) == 0) ...
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

    DECL_COLUMN(IPColumn_1, IP);
    DECL_COLUMN(IPColumn_2, IP);
    MOD_PROC_FUNC()
    {
      if (ModDifIp(&$IPColumn_1, &$IPColumn_2) == 0) ...
      ...
    }

  * Compare the values of two IP columns.
    Note that pointers to the column values are passed to the function.


.. _`ModLog()`:

``void ModLog(const char *format, ...)``
  Print a message to stderr.

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

  * Report error during module initialization.


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


.. _`HStrNAdd()`:

``CDAT_S_T HStrNAdd(const char *b, unsigned int n)``
  Create/retrieve a hash string based on string buffer ``b`` of length ``n``.

  * Use this to initialize program variables only (e.g., during module
    initialization in `MOD_INIT_FUNC()`_).
  * To set a string column's value during row processing,
    use `MOD_CDAT_S_SET()`_ or `MOD_CDAT_S_NADD()`_ instead.

  Example:

   ::

    DECL_DATA(CDAT_S_T my_str);
    MOD_INIT_FUNC()
    {
      MOD_DATA(my_str) = HStrNAdd("abc", 3);
      ...
    }

  * Set a global variable's value to a hash string.


Additional Supports
===================

Additional resources can be found in the low level include file
"``etc/include/pmod.h``".


Name versus $Name
=================

The ability to address columns by their names is a key feature of
the module script support. Both ``ColName`` and ``$ColName``
are designed to address columns, but they differ in these ways:

* ``ColName`` (without the leading dollar sign) refers to an
  abstract column reference.
  It is only valid in `module helpers`_.

* ``$ColName`` (with the leading dollar sign) is a shorthand for
  ``MOD_CDAT(ColName)``. It refers to a column's value.
  It acts like a program variable of type ``CDAT_*_T``
  (see `column datatypes`_). It can be used anywhere
  program variables are appropriate.


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor

