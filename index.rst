.. Essentia documentation master file, created by
   sphinx-quickstart on Wed Jan 28 15:51:12 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome
=======
We wrote Essentia to help solve the 'big data' day-to-day data analysis problems we faced
when processing different types of logs from different types of users.  
Specifically, we needed a framework that would allow us to quickly:

* Determine the data types stored in the data
* Organize the data into a catalog that could be used to lookup exactly
  the data we needed.
* Clean the data to enable analytics.


Essentia can be used to simplify many common problems involved with data engineering and
data analysis. The documentation in these pages is meant to train users on how to use
and integrate Essentia into their data analysis workflows.

Intended Audience
~~~~~~~~~~~~~~~~~
Data scientists and engineers are specifically targeted here, but anyone with
a technical background that needs to deal with data will have no trouble
understanding the material.

**Prequisite skillset**

* Decent understanding of the Unix command line
* shell scripting (bash for example)

**Also useful**

* General understanding of the map/reduce approach
* Cloud computing, in particular Amazon Web Services (AWS)

.. toctree::
   :hidden:
   :glob:
   :maxdepth: 6
   :titlesonly:

   source/install
   source/overview/index
   source/tutorial/index
   source/usecases/index
   source/manpages/index



