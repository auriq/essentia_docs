#################################
The Essentia Documentation Portal
#################################

We wrote Essentia to help solve the day-to-day 'big data' analysis problems we faced
when processing different types of data from different types of users.  
Specifically, we needed a framework that would allow us to quickly:

* Determine the data types stored in the data
* Organize the data into a catalog that could be used to lookup exactly
  the data we needed.
* Clean the data to enable analytics.

Essentia combines scalable, fast, Data Processing operations with an in-memory NoSQL database to
simplify many common problems encountered by data engineers and
scientists. The documentation in these pages is meant to train users on how to use
and integrate Essentia into their data processing workflow. Another useful resource and
supplement to this documentation are the `Essentia Forums <http://forum.auriq.com>`_.

*************
Tutorial Data
*************

We maintain a `GitHub repository <https://github.com/auriq/EssentiaPublic>`_ that contains test data and source code for
some of the tutorials and usecases you will find in this documentation.  

.. For AWS users, we also have a public S3 bucket (s3://asi-public) that stores the larger and more complex datasets used for training purposes.

To get started, pull the tutorial repository via::

  $ git clone https://github.com/auriq/EssentiaPublic.git

The data and scripts relevant for most of the documentation tutorials are under ``tutorials`` and those relevant for the examples and integrations are under ``case studies``.

To get started, go to :doc:`source/tutorial/essentiatutorials/index`. 

..  comment::

    *****************
    Intended Audience
    *****************
    
    Data scientists and engineers are specifically targeted here, but anyone with
    a technical background that needs to deal with data will have no trouble
    understanding the material.  Assumed skillset:
    
    * Decent understanding of the Unix command line
    * shell scripting (bash for example)
    * General understanding of the map/reduce approach and key-value pair databases.

********************
The Essentia Platform
********************

Essentia is made to be run on the cloud, where we can spin up as many worker nodes as needed to scale to difficult problems.  
Currently the Amazon cloud is supported.  
Essentia can also be used for an on premise cluster; `contact us <mailto:essentia@auriq.com>`_
for details. We do offer a single node version that can be run from a desktop; however, the power of Essentia lies in the cloud. 
You can install this single node version of Essentia on an Azure Linux VM if you want to run Essentia on the Microsoft cloud.

.. toctree::
   :hidden:
   :maxdepth: 2

   source/dlv/index
   source/tutorial/essentiatutorials/index
   source/integrations/index

..   source/tutorial/dataprocessingtutorials/index
..   :ref:`Public Github Repository <https://github.com/auriq/EssentiaPublic>`_
..   :ref:`Essentia Forums <http://forum.auriq.com>`_

.. toctree::
   :hidden:
   :maxdepth: 2
   
   source/reference/index

..   source/reference/manuals/index
..   source/reference/tables/index

.. toctree::
   :maxdepth: 1

   source/install/index
   
.. toctree::
   :hidden:
   :maxdepth: 2
   
   updateddate

| 

.. note::

   The tutorials assume you are using the ``bash`` shell.

.. .. note::
.. 
..    The Azure version does not support worker nodes.  A release in the near future will sync up all the capabilities of
..    both the Azure and Amazon versions of Essentia.
