.. |<br>| raw:: html

   <br>

====
udbd
====

Udb server


Synopsis
========

::

  udbd [-h|-v] [-q]
    [-mem LimitEach | -memx LimitTotal] [-maxfd]
    start|stop|restart|status|ckmem [PortSpec ...] [RunDir]


Description
===========

``udbd`` is used to manage (start, stop, check, etc) local Udb servers.
Usually, one Udb server per machine is sufficient because each server can
manage multiple databases. Then, multiple machines can be combined to form a
server pool for the databases
(see `udb.spec <udb.spec.html>`_ on how to define a database).

``udbd`` can also manage multiple local servers.
Which servers to target depends on the `PortSpec`_ - each port in the
spec corresponds to a separate server.


About Udb
=========

Udb stands for *User Key Database*. It is an in-memory database designed to
group user specific data together into small keyed units.
In this arrangement, each key has a set of associated data:

* The key itself. It can contain one or more columns.
* Mini tables (multi-row). The table rows are specific to the key.
* Vectors (single row). The vectors are specific to the key.

See `udb.spec <udb.spec.html>`_ on how to define a database.

Udb servers usually work together in a pool to distribute the keyed units
for storage consideration as well as to facilitate parallel processing.
Each server pool can hold and process one or more databases.
Technically, all relevant data sharing the same *key* can be placed in the
same database. Data that are keyed differently can be managed in separate
databases.

The server does not require any configuration to operate.
Its actions are completely controlled by the client programs
`aq_pp <aq_pp.html>`_ and `aq_udb <aq_udb.html>`_.
Even the database definition comes from the clients.

In general, data is first imported into one or more databases via client program
`aq_pp <aq_pp.html>`_. If there are multiple data sources, a parallel import
can be done by running multiple `aq_pp <aq_pp.html>`_ concurrently.
The `aq_pp <aq_pp.html>`_ import can run on any machines, including the Udb
machines. After all the data has been imported, the databases can be further
processed or counted/exported using client program `aq_udb <aq_udb.html>`_.

Udb can be used in serveral ways:

* On-demand - Data are left in their raw forms (e.g., compressed log files),
  then only loaded, processed, counted/exported and cleared as needed.
* Long term storage - For example, a database can be used to store a
  moving window set of data by importing live data streams into the database
  continuously and deleting old data from the database periodically.
* A combination of on-demand and long term storage - In this case, on-demand
  databases are used in conjunction with long term databases to perform
  transient processing. The same Udb server pool can manage all the
  databases as appropriate.

Databases can be cleared individually to release their associated resources
when they are no longer needed.


Options
=======

.. _`-q`:

``-q``
  Quiet.
  Suppress info level messages that normally go to stdout.


.. _`-mem`:

``-mem LimitEach``, ``-memx LimitTotal``
  Limit the memory usage of each server to be started by this command to
  ``LimitEach`` or ``LimitTotal / NumServer`` KiloBytes.
  For `start`_ and `restart`_ operations only.

  If ``LimitEach`` or ``LimitTotal`` is negative, the actual limit will be
  the system's total memory minus the given amount.

  If no limit is given, a default ``LimitTotal`` of system total minus
  500 MB will be applied.

  **Note**: The command does not take the memory usage of other running
  applications (e.g., previously started Udb servers) on the system into
  account.


.. _`maxfd`:

``-maxfd``
  Set the file descriptor limit of each server to be started to the maximum
  number allowed (usually the value of ``ulimit -Hn``).


.. _`start`:

``start [PortSpec ...] [RunDir]``
  Start Udb servers at the given `PortSpec`_.
  If no port is given, a single server will be started at port 10010.
  `RunDir`_ sets a custom server directory.


.. _`stop`:

``stop [PortSpec ...]``
  Stop (kill) Udb servers running at the given ports.
  If no port is given, the command will try to detect and stop all running
  Udb servers.


.. _`restart`:

``restart [PortSpec ...] [RunDir]``
  Equivalent to a `stop`_ and `start`_ operation.
  That is, stop Udb servers running at the given `PortSpec`_, then start those
  servers again.
  If no port is given, the command will try to detect and stop all running
  Udb servers, then start the detected servers again.
  `RunDir`_ sets a custom server directory.


.. _`status`:

``status [PortSpec ...]``
  Report the status of Udb servers running at the given `PortSpec`_.
  If no port is given, the command will try to detect and list all running
  Udb servers.


.. _`ckmem`:

``ckmem [PortSpec ...]``
  Check the memory usages of Udb servers running at the given `PortSpec`_.
  If no port is given, the command will try to detect and check all running
  Udb servers.


.. _`PortSpec`:

``PortSpec``
  Ports are used to identify the target servers to apply the action to
  (each port is tied to a separate server).
  All options can take one or more port specifications.
  Each ``PortSpec`` has the form:

  ``[PortStart]-PortEnd``
    A range of ports starting at ``PortStart`` (or 10010 if it is not given)
    and ending at ``PortEnd``.

  ``[PortStart]+NumPort``
    A range of ports starting at ``PortStart`` (or 10010 if it is not given)
    and ending at ``PortStart+(NumPort-1)``.


.. _`RunDir`:

``RunDir``
  The `start`_ and `restart`_ actions can take an optional
  runtime directory parameter. It is only needed when starting Udb in a custom
  location. If given, the `server files`_ will be stored in the given
  ``RunDir``.


Environments
============

Udb makes use of these environments:

* ``UDBD_MEM=KiloBytes`` - The same as the `-mem`_ Udb start/restart parameter.
  However, `-mem`_ takes precedence over the environment.
* ``UDBD_MAXFD=y`` - The same as the `maxfd`_ Udb start/restart parameter if
  it is set to ``y``..
* ``UDBD_MEM_MARGIN=KiloBytes`` - This tells the server to leave the given
  amount of free memory on the system during imports. An import will be aborted
  with an ``out of memory`` error if the system's free memory drops below
  this limit.


Server Files
============

Each Udb server is named "``udbd-Port``" where ``Port`` is the port
number it binds to. There are 3 files associated with each server:

* ``udbd-Port`` - Server executable (usually a symbolic link).
* ``udbd-Port.log`` - Server activity log.
* ``udbd-Port.pid`` - Server PID file (if it is running).

Server files are kept in the server's runtime directory.
By default, the runtime directory is one of these locations:

1) ``/opt/aq_tool/udb/``
2) ``../udb/`` from the directory where ``udbd`` is installed.

The location can be overriden by the `RunDir`_ option.


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `aq_udb <aq_udb.html>`_ - Udb server interface
* `udb.spec <udb.spec.html>`_ - Udb spec file

