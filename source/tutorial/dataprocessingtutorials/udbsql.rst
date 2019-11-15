******************************************
SQL Query: UDB Databases
******************************************

Overview
========

``udbsql`` is a method of quering the data in any of your UDB databases. 
It allows you to quickly and efficiently explore data that has been loaded into and distributed in a UDB database, and is written in a user friendly, SQL-like language.

The ``udbsql`` command structure consists of a select statement to define which columns are desired and what operations you want to perform on them, 
a from statement telling ``udbsql`` which UDB database and table|vector|variable to pull the data from, and a series of filtering and ordering options to modify how the data is output.

``udbsql`` supports the following types of sql statements:

* **Select Statement Specifications:** *column_name(s), \*, count(column_name), count(\*), count(distinct column_name)*
* **From Statement Specifications:** *database_name:table_name|vector_name|variable_name*
* **Output Modification Options:** *where column_name operator value, limit number, group by column_name, order by column_name*

**Syntax:**

.. csv-table::
    :header: "Command", "Arguments", "Description"
    :widths: 10, 15, 40

    udbsql,"| ``[--help || -h]``
    | ``[--verbose || -v]`` 
    | ``[--list || -l]``","Query data in a UDB database using simple sql-like statements"

**Options:**

| 
|   ``-v, --verbose``  verbosely list aq_udb command to execute
|   ``-l, --list``     list aq_udb command without execution
| 

Types of Queries
================
There are 2 types of queries, *select* and *count*. Each supports unique set of statements, and has some roles. We'll take a look at basic query format and roles for both types.
Interactive example for ``udbsql`` is also available on `Essentia-Playground <https://essentia-playground.auriq.com>`_

Select
------

Query Format::

    select [column_name] | [*] from [database_name]:[table_name | vector_name | variable_name] where ... order by ... limit ...

Examples::

    select * from udb_databasename:tablename
    select count(*) from udb_databasename:tablename
    SELECT ... FROM database:tableA WHERE pkey_A IN (SELECT pkey_B FROM [database:]tableB WHERE ...) ...
    
**Rules:**
Only restriction is that ``GroupBy`` operation is not supported in select type of statement.

Count
-----

Query Format::

    select count(distinct [column_name] | [*]) from [database_name]:[table_name | vector_name | variable_name] where ...

    select [column_name], count(*) from [database_name]:[table_name | vector_name | variable_name] where ... group by [column_name]

Examples::

    select count(distinct col1), count(distinct col2), count(*) from udb_databasename:tablename

    select count(*) from udb_databasename:tablename group by col1 col2


    
**Rules:**
``Order By``, ``Group By`` and ``Limit`` are not supported by Count query, unless used with ``DISTINCT`` statement.



Examples by statement types
---------------------------

LIMIT::

    select * from udb_databasename:tablename limit 10

WHERE::

    select * from udb_databasename:tablename where filterspec

ORDER BY::

    select * from udb_databasename:tablename order by col

DISTINCT::

    select count(distinct col1), count(distinct col2), count(*) from udb_databasename:tablename

GROUP BY::

    select count(*) from udb_databasename:tablename group by col1 col2

