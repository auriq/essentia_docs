====
udbd
====

----------
Udb server
----------

:Copyright: AuriQ Systems Inc.
:Manual group: Udb
:Manual section: 1
:Date: 2015-01-28
:Version: 1.2.1


Synopsis
========

::

  udbd [-h|-v] [-q]
    start|stop|restart|status|cklog|ckmem [PortSpec ...] [WorkDir]


Description
===========

The ``udbd`` command is used to perform Udb server start, stop and
maintenance operations.
Each operation applys to one or more servers running on the local machine.
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
It is designed for *keyed* data such as those associated with an user ID.
For this reason, Udb is known as the *User (Bucket) Database*.
Udb servers usually work together in a pool to distribute data storage
as well as facilitate parallel processing.
 
Each server pool can hold and process a single database at a time.
An Udb database is one that contains user buckets with tables and vectors
in each bucket. Technically, all relevant data sharing the same *key* can be
placed in the same database. But if data using a different key is needed
at the same time, it must be placed in another pool of Udb servers.

In general, data is first imported into the database via client program
`aq_pp <aq_pp.html>`_. If there are multiple data sources and that data order in the
database is not important, import can be done in parallel. To maximize
throughput, one or more parallel imports per Udb server can be used. 

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

Note that the server does not require any configuration to operate.
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

  * It sets the server work/runtime directory.
  * By default, the work directory is udbd's installation directory.
  * The work directory is where the log file and pid file are saved.
  * The work directory is where udb modules (if any) are installed.


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
be installed under the "mod/" directory in the server work/runtime directory.

Each instant of Udb server is named "udbd-Port" where Port is the port
number it is associated with. There are 3 files associated with each instant:

* udbd-Port - Server executable (usually a symbolic link).
* udbd-Port.log - Server activity log.
* udbd-Port.pid - Server PID file (if it is running).


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `aq_udb <aq_udb.html>`_ - Interface to Udb server

