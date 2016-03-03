====
udbd
====

Udb server


Synopsis
========

::

  udbd [-h|-v] [-q]
    start|stop|restart|status|cklog|ckmem [PortSpec ...] [WorkDir]


Description
===========

``udbd`` is a Udb server start, stop and maintenance command.
Each operation applys to one or more server instances on the local machine.
Which instances to target depend on the `PortSpec`_ supplied at commandline
(each local Udb server binds to a unique port).

Usually, a machine only runs a single Udb server.
However, multiple servers can be started if there are sufficient memory and
CPU cores. These servers can be used as part of a parallel pool for one
database or as separate pools for independent databases.
More `about Udb server`_ below.


About Udb Server
================

A Udb server is an in-memory database server.
It is designed for *keyed* data such as those associated with an *user key*.
For this reason, Udb is known as the *User (Bucket) Database*.
Udb servers usually work together in a pool to distribute data storage
as well as facilitate parallel processing.

Each server pool holds and processes a single database at a time.
An Udb database is one that contains user buckets with tables and vectors
in each bucket. Technically, all relevant data sharing the same *key* can be
placed in the same database. On the other hand, data that are keyed differently
must be managed by separate pools of Udb servers.
A typical database is stored in this way:

 ::

  Server1                         ...     ServerN

  +------------+------+                   +------------+------+
  | Var vector | cols |           ...     | Var vector | cols |
  +------------+------+                   +------------+------+

  +=================+=======+             +=================+=======+
  | User key (PKEY) | key11 |     ...     | User key (PKEY) | keyN1 |
  +=================+=======+             +=================+=======+
  | +---------+-----------+ |             | +---------+-----------+ |
  | | Table1  | row1 cols | |             | | Table1  | row1 cols | |
  | |         | row2 cols | |             | |         | row2 cols | |
  | |         | ...       | |             | |         | ...       | |
  | +---------+-----------+ |             | +---------+-----------+ |
  | | Table2  | row1 cols | |             | | Table2  | row1 cols | |
  | |         | row2 cols | |             | |         | row2 cols | |
  | |         | ...       | |             | |         | ...       | |
  | +---------+-----------+ |             | +---------+-----------+ |
  | | ...                 | |             | | ...                 | |
  | +---------+-----------+ |             | +---------+-----------+ |
  | +---------+------+      |             | +---------+------+      |
  | | Vector1 | cols |      |             | | Vector1 | cols |      |
  | +---------+------+      |             | +---------+------+      |
  | | Vector2 | cols |      |             | | Vector2 | cols |      |
  | +---------+------+      |             | +---------+------+      |
  | | ...            |      |             | | ...            |      |
  | +---------+------+      |             | +---------+------+      |
  |                         |             |                         |
  +=================+=======+             +=================+=======+
  | User key (PKEY) | key12 |             | User key (PKEY) | keyN2 |
  +=================+=======+             +=================+=======+
  | +---------+-----------+ |             | +---------+-----------+ |
  | | Table1  | row1 cols | |             | | Table1  | row1 cols | |
  | |         | row2 cols | |             | |         | row2 cols | |
  | |         | ...       | |             | |         | ...       | |
  | +---------+-----------+ |             | +---------+-----------+ |
  | | Table2  | row1 cols | |             | | Table2  | row1 cols | |
  | |         | row2 cols | |             | |         | row2 cols | |
  | |         | ...       | |             | |         | ...       | |
  | +---------+-----------+ |             | +---------+-----------+ |
  | | ...                 | |             | | ...                 | |
  | +---------+-----------+ |             | +---------+-----------+ |
  | +---------+------+      |             | +---------+------+      |
  | | Vector1 | cols |      |             | | Vector1 | cols |      |
  | +---------+------+      |             | +---------+------+      |
  | | Vector2 | cols |      |             | | Vector2 | cols |      |
  | +---------+------+      |             | +---------+------+      |
  | | ...            |      |             | | ...            |      |
  | +---------+------+      |             | +---------+------+      |
  |                         |             |                         |
  +=================+=======+             +=================+=======+
  | User key (PKEY) | key13 |             | User key (PKEY) | keyN3 |
  +=================+=======+             +=================+=======+
  | ...                     |             | ...                     |
  |                         |             |                         |
  +-------------------------+             +-------------------------+

In general, data is first imported into the database via client program
`aq_pp <aq_pp.html>`_. If there are multiple data sources and that data
order in the database is not important, import can be done in parallel.
One or more parallel imports per Udb server can often be used
to maximize throughput.

Then the data can be manipulated via client program `aq_udb <aq_udb.html>`_.
Manipulations are usually done sequentially since they involve data
modification. If the server receives multiple manipulation requests at the
same time, it will serialize the requests internally.

Finally, the result can be exported via `aq_udb <aq_udb.html>`_.
This step can also be done in parallel if applicable. For example,
different tables can be exported at the same time by running separate copies
of `aq_udb <aq_udb.html>`_.
Note that an export can also modify the database. In this case, it is
treated like a manipulation step and serialization may occur.

With its parallel import support and in-memory database design,
raw data can be transformed into final or intermediate forms quickly.
There is generally no need to *warehouse* data in the database -
data can be left in their raw form (e.g., compressed log files) and only
loaded on-demand. After processing, the database can simply be destroyed,
releasing memory back to the operating system. Once a server is cleared,
it can be used to handle another database.

The server does not require any configuration to operate.
Its actions are completely controlled by the client programs
`aq_pp <aq_pp.html>`_ and `aq_udb <aq_udb.html>`_.
Even the data definition (table defs) comes from the client.


Options
=======

.. _`PortSpec`:

``PortSpec``
  All options can take one or more port specifications.
  Each ``PortSpec`` has the form:

  ``[PortStart]-PortEnd``
    A range of ports starting at ``PortStart`` (or 10010 if it is not given)
    and ending at ``PortEnd``.

  ``[PortStart]+NumPort``
    A range of ports starting at ``PortStart`` (or 10010 if it is not given)
    and ending at ``PortStart+(NumPort-1)``.


.. _`WorkDir`:

``WorkDir``
  The `start`_ and `restart`_ actions can take an optional
  work directory parameter.
  It is the server's work/runtime directory where its log file and pid file
  are saved.
  The default work directory location is determined in this order:

  1) ``udb/`` under the aq_tool installation directory.
  2) ``../udb/`` from the directory where ``udbd`` is installed.
     This is usually the same as (1).
  3) The directory where ``udbd`` is installed.


.. _`-q`:

``-q``
  Quiet.
  Suppress info level messages that normally go to stdout.


.. _`-mem`:

``-mem KBytes``
  For `start`_ and `restart`_ operations only.
  Set server memory limit in KiloBytes (equivalent to ``ulimit -v KBytes``).
  This limit applies to each Udb server (not the total of all servers started
  by this command).
  If a limit is set, memory allocation will fail when a server used up KBytes
  memory.

  **Note**: A benefit for setting this limit is to allow the server to
  detect the out-of-memory error condition.
  Without this, the operating system may terminate the server before it can
  detect such a condition.


.. _`start`:

``start [PortSpec ...] [WorkDir]``
  Start Udb servers at the given `PortSpec`_.
  `PortSpec`_ determines which server to start.
  If no port is given, a single server will be started at port 10010.
  `WorkDir`_ sets the servers' work/runtime directory.


.. _`stop`:

``stop [PortSpec ...]``
  Stop (kill) Udb servers running at the given ports.
  If no port is given, try to detect and stop all running Udb servers.


.. _`restart`:

``restart [PortSpec ...] [WorkDir]``
  Equivalent to a `stop`_ and `start`_ operation.
  That is, stop Udb servers running at the given `PortSpec`_, then start those
  servers again.
  If no port is given, try to detect and stop all running Udb servers,
  then start the detected servers again.
  `WorkDir`_ sets the servers' work/runtime directory.


.. _`status`:

``status [PortSpec ...]``
  Report the status of Udb servers running at the given `PortSpec`_.
  If no port is given, try to detect and list all running Udb servers.


.. _`cklog`:

``cklog [PortSpec ...]``
  Get error/warning messages from the logs of Udn servers running at the given
  `PortSpec`_.
  If no port is given, action applies to all running Udb servers.


.. _`ckmem`:

``ckmem [PortSpec ...]``
  Get the memory usage of Udn servers running at the given `PortSpec`_.
  If no port is given, action applies to all running Udb servers.


Server Files
============

The Udb server can make use of "modules" (shared objects). These modules must
be installed under the "umod/" directory in the server executable's
installation directory.

Each instant of Udb server is named "udbd-Port" where Port is the port
number it is associated with. There are 3 files associated with each instant:

* udbd-Port - Server executable (usually a symbolic link).
* udbd-Port.log - Server activity log.
* udbd-Port.pid - Server PID file (if it is running).


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `aq_udb <aq_udb.html>`_ - Udb server interface
* `udb.spec <udb.spec.html>`_ - Udb spec file

