====
tmon
====

------------
Task monitor
------------

:Copyright: AuriQ Systems Inc.
:Manual group: Utility Command
:Manual section: 1
:Date: 2015-01-28
:Version: 1.2.1


Synopsis
========

::

  tmon [-h|-v] [cpu|mem] [-task Num] [-dt Interval] [-n Count]


Description
===========

``tmon`` is a task monitor.
It is a ``top`` command wrapper that returns the top CPU or
memory consuming tasks at regular interval.

**Note**: This tool only works under Linux.


Options
=======

.. _`cpu`:

``cpu``
  Select tasks by top CPU usage. This is the default.


.. _`mem`:

``mem``
  Select tasks by top memory usage.


.. _`-task`:

``-task Num``
  Set the number of tasks to show. Default is 8.


.. _`-dt`:

``-dt Interval``
  Set the time interval (sec) between reports.


.. _`-n`:

``-n Count``
  Set the number of cycles to run. Default is unlimited.


Output Format
=============

The output contains blocks of task info in this form:

 ::

  n3212: 2014/07/31 14:43:28 PDT
    PID  VIRT %MEM    TIME+  %CPU COMMAND
   3343  494m  2.3   1:58.10  1.4 firefox
    849     0  0.0   0:02.94  0.2 usb-storage
      1  2160  0.0   0:07.14  0.0 init
      2     0  0.0   0:00.00  0.0 migration/0
      3     0  0.0   0:00.00  0.0 ksoftirqd/0
      4     0  0.0   0:00.00  0.0 watchdog/0


The first line contains a *marker* in this form:

 ::

  label: date

where column 1 is a label that identifies the originating machine
(usually the first part of its domain name);
column 2 is a date in the machine's local timezone.

The second line contains the column labels for the task info.
The third line and up (until the next *marker* line) contain the task info.


See Also
========

* `smon <smon.html>`_ - System monitor

