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
  *user bucket database* (Udb).
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
* `aq_sess <aq_sess.html>`_ - Session count
* `aq_cat <aq_cat.html>`_ - Input multiplexer
* `objcnv <objcnv.html>`_ - XML/JSON Field Extractor

User bucket database engine:

* `udbd <udbd.html>`_ - Udb server

  * `udb.spec <udb.spec.html>`_ - Udb spec file
  * `udb-size <udb-size.html>`_ - Udb database size estimate

Helpers:

* `loginf <loginf.html>`_ - Log analyzer

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
   aq_sess
   aq_cat
   aq-emod
   objcnv
   udbd
   udb.spec
   udb-size
   loginf
   smon
   tmon
   ChangeLog-1.2.2


.. Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

