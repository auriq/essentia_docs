The Benefit of Using aq_pp
==========================

To demonstrate the utility of ``aq_pp``, lets look at the following problem:

We have sales data from a fictional store that caters to international clients.  We record the amount spent for each
purchase and the currency it was purchased with.  We wish to compute the total sales in US Dollars.
We have 2 files to process.  The first contains the time, currency type, and amount spent, and the second is a lookup
table that has the country code and USD exchange rate:

.. csv-table:: sales data
   :header: "transaction_date","currency","amount"
   :widths: 30, 10, 10

   2013-08-01T07:50:00,USD,81.39
   2013-08-01T08:22:00,USD,47.96
   2013-08-01T08:36:00,CAD,62.59


.. csv-table:: Exchange rate
   :header: "currency","rate"
   :widths: 10,10

   EUR,1.34392
   CAD,0.91606
   USD,1.00000

Lets compare 2 solutions against ``aq_pp``

**SQL**::

  select ROUND(sum(sales.amount*money.rate),2) AS total from sales INNER JOIN exchange ON sales.currency = exchange.currency;

SQL is straightforward and generally easy to understand.  It will execute this query very quickly,
but this overlooks the hassle of actually importing it into the database.

**AWK**::

  awk 'BEGIN {FS=OFS=","} NR==1 { next } FNR==NR { a[$1]=$2; next } $2 in a { $2=a[$2]; sum += $2*$3} END {print sum}' exchange.csv sales.csv

AWK is an extremely powerful text processing language, and has been a part of Unix for about 40 years.  This legacy
means that it is stress tested and has a large user base.  But it is also not very user friendly in some
circumstances.  The language
complexity scales with the difficulty of the problem you are trying to solve.  Also, referencing the columns by
positional identifiers ($1, $2 etc) makes AWK code more challenging to perfect.


**AQ_PP**::

  aq_pp -f,+1 sales.csv -d s:date s:currency f:amount -cmb,+1 exchange.csv s:currency f:rate -var f:sum 0.0 -evlc 'sum' 'sum+(amount*rate)' -ovar -

The AuriQ preprocessor is similar in spirit to AWK, but it simplifies many issues that are complex in ``awk``.
We'll detail the specifics in the rest of the documentation, but even without knowing all of the syntax, the
intent of the command is fairly easy to discern. Instead of positional arguments, columns
are named, therefore making an ``aq_pp`` command more human readable.
Additionally, it is very fast, in fact an order of magnitude faster in this example.

In the `aq_pp Tutorial <http://vm146.auriq.net/documentation/source/tutorial/aqtools/aq_pp/aq_pp\ tutorial.html>`_ that follows, we will expand on how this and other Essentia tools can simplify and empower your data
processing workflow.