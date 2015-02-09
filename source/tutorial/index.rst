Tutorials
=========

The following tutorials provide a solid background on most of Essentia's capabilities.
They are meant to be followed in order.

The AQ tools, which are the heart of the Essentia suite of tools, are unix command line tools, and we highlight use
cases where they can be used more efficiently than the common text processing commands already available.

Tutorials under the Essentia classification focus on how these AQ commands are efficiently scaled up to handle large
numbers of files and volume of data.

In both cases, AWS cloud services are not required for learning the Essentia basics.  Therefore the desktop version
can be used easily.  This version cannot showcase the power of Essentia at scale, but the :doc:`../usecases/index`
section includes examples and scripts that can.

**Resources**

We main a `GitHub repository <https://github.com/auriq/EssentiaPublic>`_ that contains test data and source code for
the tutorials and usecases you will find in this documentation.

For AWS users, we have a public S3 bucket (s3://asi-public) that stores the larger and more complex datasets used for
training purposes.

**Available Tutorials**

* :doc:`aqtools/index`: Command line based text processing tools
* :doc:`essentia/index`: Scaling for "big data"


.. toctree::
   :hidden:
   :titlesonly:

   aqtools/index
   essentia/index

