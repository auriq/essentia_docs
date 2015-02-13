*********
Tutorials
*********

The following tutorials provide a solid background on most of Essentia's capabilities.  They do not require significant
computational resources, and therefore the desktop version or the AWS free tier of instances is sufficient to get
started.  The more intensive examples are reserved for the :doc:`../usecases/index` section.

We maintain a `GitHub repository <https://github.com/auriq/EssentiaPublic>`_ that contains test data and source code for
some of the tutorials and usecases you will find in this documentation.  For AWS users, we also have a public S3
bucket (s3://asi-public) that stores the larger and more complex datasets used for training purposes.

Both the Essentia and AQ Tool commands can be run sequentially on the command line. However, we recommend using the Bash scripting language so that you can execute entire sets of commands in order and in quick succession.

AQ Tools
========

The AQ suite of programs, which are the heart of Essentia, are unix command line tools.
Unix users familiar with the raw text processing commands ``sed`` , ``awk``, etc should find the aq commands to be
relatively straightforward to learn, and we highlight how the aq commands can significantly
ease the burden of many problems encountered in a typical data processing workflow.

* :doc:`aqtools/aq_pp/index` : the text pre-processor
* :doc:`aqtools/udb` : the in-memory database
* :doc:`aqtools/logcnv` : the log file parser/converter

.. toctree::
   :titlesonly:
   :hidden:

   aqtools/aq_pp/index
   aqtools/udb
   aqtools/logcnv


Essentia
========

Tutorials under the Essentia classification focus on how these AQ commands are efficiently scaled up to handle large
numbers of files and volume of data.  The two main components include *data management* and *resource management*.
By abstracting out classes of data that share the same properties (i.e. log data from a web server with one file per
day), we can concentrate less on where the data is, and focus on analyzing it.  The resource manager is used to scale
the processing to handle large groups of files.


.. toctree::

   essentia/data_organization
   essentia/ess_on_aws
   essentia/scaling_aqpp
   essentia/scaling_udb
   essentia/query
   essentia/redshift



