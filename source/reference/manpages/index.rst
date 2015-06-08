.. aq_tool documentation master file, created by
   sphinx-quickstart on Thu Feb 26 17:44:44 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

aq_tool manuals
===============

*aq_tool* is a collection of data processing tools.
Most are command line tools that operate on an input data set according
to the command line options and produce an output data set.
One is a specialized low level database server called the
*user bucket database*.
The rest are helper tools that aid processing in general.

Data processing commands:

* `aq_pp <aq_pp.html>`_ - Record preprocessor

  * `rt.so <aq_pp-emod-rt.html>`_ - aq_pp RT module

* `aq_udb <aq_udb.html>`_ - Udb server interface
* `aq_cnt <aq_cnt.html>`_ - Data row/key count
* `aq_ord <aq_ord.html>`_ - In-memory record sort
* `aq_sess <aq_sess.html>`_ - Session count
* `logcnv <logcnv.html>`_ - CLF log converter
* `jsncnv <jsncnv.html>`_ - JSON log converter

User bucket database server:

* `udbd <udbd.html>`_ - Udb server

  * `udb.spec <udb.spec.html>`_ - Udb spec file
  * `udb-size <udb-size.html>`_ - Udb database size estimate

Helpers:

* `loginf <loginf.html>`_ - Log analyzer
* `prtrng <prtrng.html>`_ - File/stream data range dump
* `smon <smon.html>`_ - System monitor
* `tmon <tmon.html>`_ - Task monitor

.. toctree::
   :maxdepth: 1
   :hidden:

   aq_pp
   aq_pp-emod-rt
   aq_udb
   aq_cnt
   aq_ord
   aq_sess
   logcnv
   jsncnv
   udbd
   udb.spec
   udb-size
   loginf
   prtrng
   smon
   tmon


.. Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

