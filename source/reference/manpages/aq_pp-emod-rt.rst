=====
rt.so
=====


Description
===========

``rt.so`` is a module for `aq_pp <aq_pp.html>`_'s ``-emod`` option.
It provides callable RT functions for `aq_pp <aq_pp.html>`_'s evaluation options.


Synopsis
========

The module is loaded by `aq_pp <aq_pp.html>`_ in this way:

 ::

  aq_pp -emod rt ... -eval ...

The module loading syntax is "``-emod ModSpec``" where
``ModSpec`` is simply "rt", no module argument is necessary.
The module file is "rt.so". It is usually supplied and installed along with
`aq_pp <aq_pp.html>`_.
The module requires some support files to operate. A set of default support
files are supplied along with the module.


Module functions
================

The evaluation functions supplied by this module are:

``SearchKey(Url)``

  * Extract search key from the given Url (string).
  * Return the extracted search key (string). A blank is returned if the Url
    does not match that of any known search engine. A "-" is returned if the
    Url matches that of a search engine but there is no seach key.
  * Url can be a string column's name, a literal quoted with double quotes
    or an expression that evaluates to a string.
  * The value of Url must be in the form "domain/[path[?query]]".

``SearchKey2(Site, Path)``

  * Same as ``SearchKey(Url)`` except that the Url argument is separated into
    site and path (i.e., ``Site+Path=Url``).
  * Site is the site's domain. Path is "/[path[?query]]".

``IpToCountry(Ip)``

  * Lookup and return "country_code[:region_code]" info (string) for the given
    Ip.
  * Ip can be a IP column's name, a literal IP or an expression that evaluates
    to an IP.

``AgentParse(Agent)``

  * Parse the given user-agent string and return a
    "browser[:OS[:DeviveType:DeviceName]]" string.
  * Agent can be a string column's name, a literal quoted with double quotes
    or an expression that evaluates to a string.

``AgentParse2(Agent, Ip)``
  * Same as "AgentParse(Agent)" except for an additional source IP argument.
    The source IP is used in crawler matching, it can help improve crawler
    match accuracy.
  * Ip can be a IP column's name, a literal IP or an expression that evaluates
    to an IP.


See Also
========

* `aq_pp <aq_pp.html>`_ - Record preprocessor
* `udbd <udbd.html>`_ - User (Bucket) Database server
* `aq_udb <aq_udb.html>`_ - Interface to Udb server

