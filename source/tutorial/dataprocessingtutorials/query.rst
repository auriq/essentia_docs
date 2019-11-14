********************
SQL Query: Categories
********************

For times when very basic data inspection is required, the ``query`` command can be useful.  It allows SQL like queries
directly on your data sources.  For instance, if we are interested in the number of sales and number of unique purchases
over a 10 day span from our woodworking data, we can execute::

  $ ess query "select count(distinct userID) FROM purchase:2014-09-01:2014-09-10"
  "row","k_userID"
  13618,4929

Be sure to run this AFTER defining the datastore from the earlier tutorial.
We can filter using the WHERE clause::

  $ ess query "select count(*) FROM purchase:2014-09-01:2014-09-10 WHERE articleID >20"
  "row"
  7818


This is much simpler than loading data into a database or other system and obtaining the result. The price for this
convenience is that the query command does not support many SQL keywords.  A future update will expand the
functionality of this interface.

To see more examples of the types of queries we allow and work with some sample queries of our public data, please go through our 

* :doc:`../../dlv/direct-query-examples`
* `Essentia-Playground Notebooks <essentia-playground>`_
