#################################
The Essentia Documentation Portal
#################################

We wrote Essentia to help solve the day-to-day 'big data' analysis problems we faced
when processing different types of logs from different types of users.  
Specifically, we needed a framework that would allow us to quickly:

* Determine the data types stored in the data
* Organize the data into a catalog that could be used to lookup exactly
  the data we needed.
* Clean the data to enable analytics.

Essentia combines scalable, fast, ETL operations with an in-memory NoSQL database to
simplify many common problems encountered by data engineers and
scientists. The documentation in these pages is meant to train users on how to use
and integrate Essentia into their data processing workflow. Another useful resource and
supplement to this documentation are the `Essentia Forums <http://forum.auriq.com>`_.

*****************
Intended Audience
*****************

Data scientists and engineers are specifically targeted here, but anyone with
a technical background that needs to deal with data will have no trouble
understanding the material.  Assumed skillset:

* Decent understanding of the Unix command line
* shell scripting (bash for example)
* General understanding of the map/reduce approach and key-value pair databases.

*****************
Intended Platform
*****************

While we do offer a single node version that can be run from a desktop, the power of Essentia lies in the cloud.
There we can spin up as many worker nodes as needed to scale to difficult problems.  Currently Amazon and Microsoft
clouds are supported.  Essentia can also be used for an on premise cluster; `contact us <mailto:essentia@auriq.com>`_
for details.

.. toctree::
   :hidden:
   :maxdepth: 3

   source/install/index
   source/tutorial/index
   source/usecases/index
   source/reference/index




