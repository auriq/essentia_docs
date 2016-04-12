*************
Tutorial Data
*************

We maintain a `GitHub repository <https://github.com/auriq/EssentiaPublic>`_ that contains test data and source code for
some of the tutorials and usecases you will find in this documentation.  

.. For AWS users, we also have a public S3 bucket (s3://asi-public) that stores the larger and more complex datasets used for training purposes.

To get started, pull the tutorial repository via::

  $ git clone https://github.com/auriq/EssentiaPublic.git

The data and scripts relevant for most of the documentation tutorials are under ``tutorials`` and those relevant for the examples and integrations are under ``case studies``.


Description of Data
===================

For much of the tutorial, we will be using a synthetic set of log files collected from a
fictional DIY woodworking web site.  This web site offers detailed construction plans for many items.  Users can
browse part of the article for free, but must pay to obtain the full plan. It is a new service,
and in order to determine how best to price the items, the site randomized the prices for each
set of plans over a 1 month period (prices range from 1 to 6 dollars).

There are two sets of log files.  The first have a filename in the form of ``browse_YYYYMMDD.csv.gz`` and contain the
browsing records of all users who visited the site on a given day.  The files have three columns of data:

:eventDate:
    timestamp of when the user visited a page.
:userID:
    numerical ID matched to a unique user.
:articleID:
    a unique identifier for each of the articles offered

The data is not clean.  Unfinished articles that are (accidentally) accessible to users yield an articleID of "TBD"
(in other words, a string instead of a number).

The second set of logs record all purchases, and have 5 columns of data:

:purchaseDate:
    time and date article was purchased
:userID:
    User that purchased article
:articleID:
    ID of the article purchased
:price:
    price user paid for the article
:refID:
    ID of the article seen just prior to the one being purchased.


Again, the data have problems.   Due to a glitch in the billing system the articleIDs in all files dated on and after
September 15 are off by one, and we need to add this back to the reported ID.  These data issues are contrived,
but will serve to illustrate some of the Data Processing power of Essentia.

To demonstrate the ``aq_pp`` Data Processing command, we will also use a set of smaller files that help illustrate its usage.
These are found in the ``tutorials/etl-engine`` directory