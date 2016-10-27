.. aq_tool documentation master file, created by
   sphinx-quickstart on Thu Feb 26 17:44:44 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

********************
Data Processing Tools
********************

Introduction
============

The *aq_tools* are a collection of data processing tools.
The tool set includes:

* Command line tools that process an input data set into an output set
  according to the command line options. All the tools, except for the sort
  command, operate in stream mode.
* A specialized low level database engine called the
  *user key database* (Udb).
* The rest are support files and helper tools that aid processing in general.

Manuals
=======

Data processing commands:

* `aq_pp <aq_pp.html>`_ - Record preprocessor

  * `aq-emod <aq-emod.html>`_ - aq_tool eval functions
  * `mcc.pmod <mcc.pmod.html>`_ - aq_pp module script compiler

* `aq_udb <aq_udb.html>`_ - Udb server interface

  * `aq-emod <aq-emod.html>`_ - aq_tool eval functions
  * `mcc.umod <mcc.umod.html>`_ - Udb module script compiler

* `aq_cnt <aq_cnt.html>`_ - Data row/key count
* `aq_ord <aq_ord.html>`_ - In-memory record sort
* `aq_cat <aq_cat.html>`_ - Input multiplexer

Common:

* `aq-input <aq-input.html>`_ - aq_tool input specifications
* `aq-output <aq-output.html>`_ - aq_tool output specifications
* `aq-emod <aq-emod.html>`_ - aq_tool eval functions

User key database engine:

* `udbd <udbd.html>`_ - Udb server

  * `udb.spec <udb.spec.html>`_ - Udb spec file

Helpers:

* `loginf <loginf.html>`_ - Log analyzer
.. * `smon <smon.html>`_ - System monitor
.. * `tmon <tmon.html>`_ - Task monitor

Version Changes
===============

* `1.2.4 ChangeLog <ChangeLog.html>`_ [Current]
* `1.2.3 ChangeLog <ChangeLog-1.2.3.html>`_
* `1.2.2 ChangeLog <ChangeLog-1.2.2.html>`_

.. toctree::
   :maxdepth: 1
   :hidden:

   ChangeLog
   aq_pp
   mcc.pmod
   aq_udb
   mcc.umod
   aq_cnt
   aq_ord
   aq_cat
   aq-input
   aq-output
   aq-emod
   udbd
   udb.spec
   loginf
   smon
   tmon
   ChangeLog-1.2.3
   ChangeLog-1.2.2


.. Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

