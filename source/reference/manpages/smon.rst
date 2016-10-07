.. |<br>| raw:: html

   <br>

====
smon
====

System monitor


Synopsis
========

::

  smon [-h|-v] [-q]
    start|stop|restart|status|cklog|cksize|cktime|fetch|purge|fg
    [-dt Interval] [-xmem %Usage] [-xdsk %Usage] [-wrn] [-n Count]


Description
===========

``smon`` is a system monitor.
It normally runs as a daemon and collects system statistics at
regular interval in the background.
Collected result is saved in a stats log "smon.out" in the
daemon's runtime directory.

``smon`` can also run in the foreground and output stats as soon as they
are collected.

**Note**: This tool only works under Linux.


Options
=======

.. _`-q`:

``-q``
  Quiet.
  Suppress info level messages that normally go to stdout.


.. _`cpu`:

``cpu``
  Select tasks by top CPU usage. This is the default.


.. _`start`:

``start``
  Start stats collection daemon. The daemon collects system statistics
  every 30 sec and saves result in stats log "smon.out".


.. _`stop`:

``stop``
  Stop the daemon if it is running.


.. _`restart`:

``restart``
  Start daemon if it is not running.
  No action is taken if the daemon is already running.


.. _`status`:

``status``
  Report whether the daemon is running.


.. _`cklog`:

``cklog``
  Retrieve all records from stats log "smon.out" that have the
  warning field set.
  See `-xmem`_ and `-xdsk`_ regarding how warning is set.
  Output goes to stdout.


.. _`cksize`:

``cksize``
  Get the stats log "smon.out" file size.
  Output goes to stdout.


.. _`cktime`:

``cktime``
  Get the beginning and ending time from stats log "smon.out".
  Output goes to stdout.


.. _`fetch`:

``fetch``
  Retrieve all records from stats log "smon.out".
  Output goes to stdout.


.. _`purge`:

``purge``
  Delete stats log "smon.out".


.. _`fg`:

``fg``
  Collect and print stats in the foreground every 5 sec.
  No stats log is generated.


.. _`-dt`:

``-dt Interval``
  For `start`_ and `fg`_ only:
  Collect stats every Interval seconds.
  Default is 30 sec for `start`_ and 5 sec for `fg`_.


.. _`-xmem`:

``-xmem %Usage``
  For `start`_ and `fg`_ only:
  Set the stats warning field if memory usage exceeds the
  %Usage threshold. Default is 94%.


.. _`-xdsk`:

``-xdsk %Usage``
  For `start`_ and `fg`_ only:
  Set the stats warning field if disk usage exceeds the
  %Usage threshold. Default is 94%.


.. _`-wrn`:

``-wrn``
  For `start`_ and `fg`_ only:
  Only save/print stats with a warning set.
  See `-xmem`_ and `-xdsk`_ regarding how warning is set.


.. _`-n`:

``-n Count``
  For `start`_ and `fg`_ only:
  Quit after saving/printing ``Count`` stats records. Default is unlimited.


Stats Log Format
================

The stats log is in CSV format. For example:

 ::

  n3212,1406334500,cpu=4009|1192|29 cpu0=1003|1|0 cpu1=1002|1002|100 cpu2=1002|188|18 cpu3=1003|2|0,mem=6091604|3565476|58 swap=2056312|43732|2,/=9920624|3519880|35 /home/local=18253712|6145392|33,
  n3212,1406334530,cpu=3963|2041|51 cpu0=1003|21|2 cpu1=1003|1003|100 cpu2=975|135|13 cpu3=982|882|89,mem=6091604|5826816|95 swap=2056312|53700|2,/=9920624|3519880|35 /home/local=18253712|6145392|33,mem|95

The format is:

 ::

  label,time,cpu=tot|used|%used cpu0=tot|used|%used ...,mem=tot|used|%used swap=tot|used|%used,directory=tot|used|%used directory=tot|used|%used ...,warnings

Column 1: Label

  A machine spacific label, usually the first part of its domain name.

Column 2: Time

  The time (UNIX seconds) at which the stats are collected.

Column 3: CPU usages

  The column may contain several space separated fields - one for the overall
  system CPU usage, and one for each CPU/core if applicable.
  Each field has the form:

   ::

    cpu[Id]=total|used|percent_used

  The total and used values do not have any particular unit, just use them to
  calculate usage percentage.

Column 4: Memory usages

  The column may contain up to 2 space separated fields - one for the physical
  memory usage and one for the swap usage. Each field has the form:

   ::

    memory_type=total|used|percent_used

  The total and used values are in kilobytes.

Column 5: Disk usages

  The column may contain several space separated fields - one for each mounted
  filesystem. Each field has the form:

   ::

    mount_point=total|used|percent_used

  The total and used values are in kilobytes.

Column 6: Warnings

  This column is usually empty unless either memory or disk usage exceeded
  the `-xmem`_ or `-xdsk`_ threshold (94% by default).
  The warning may contain several space separated fields, one for
  each resource exceeding the threshold. Possible fields are:

   ::

    memory_type=percent_used
    mount_point=percent_used


See Also
========

* `tmon <tmon.html>`_ - Task monitor

