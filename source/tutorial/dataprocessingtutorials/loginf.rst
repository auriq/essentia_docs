*************
File Analyzer
*************

It is not uncommon for data scientists to spend a significant amount of time determining properties about a data set.
``loginf`` was developed to assist in the process.  It scans a file and determines:

* column names
* type of each column (string, int, etc)
* number of records
* estimate of the number of unique values in the column

``loginf`` uses an O(N) algorithm to determine these properties.  In particular the uniqueness estimate is based on an
algorithm which results in an answer that is accurate to within a few percent.

Usage
=====

.. :download:`donations.csv<data/donations.csv>`

We will look at a simple 3 column file called ``donations.csv`` that can be found under ``tutorials/etl-engine`` in the git repository. It records
the last
name, city,
and amount donated
to a fictional charity.  In the rawest form, one can execute the following to get the full output in json format::

  loginf -f donations.csv
  {
    "Process Time" : 0.000,
    "Report String Encoding" : false,
    "Source Files" : 1,
    "Has BOM" : 0,
    "Bytes" : {
      "Source" : 228,
      "Count" : 205,
      "Percent" : 89.9123
    },
    "Lines" : {
      "Source" : 11,
      "Count" : 10,
      "Percent" : 90.9091
    },
    "Rows" : {
      "Count" : 10,
      "Length" : {
        "Min" : 15,
        "Max" : 31,
        "Avg" : 20.5
      }
    },
    "Columns" : {
      "Min" : 3,
      "Max" : 3,
      "Avg" : 3
    },
    "Column" : [
      {
        "Index" : 1,
        "Label" : "lastname",
        "pp-Type" : "S",
        "pp-Attr" : "",
        "pp-Name" : "lastname",
        "pp-Sample" : "Henderson",
        "Bytes" : {
          "Count" : 64,
          "Percent" : 31.2195
        },
        "Rows" : {
          "Count" : 10,
          "Percent" : 100
        },
        "Length" : {
          "Min" : 4,
          "Max" : 9,
          "Avg" : 6.4
        },
        "Unique Estimate" : 10,
        "Type-String" : {
          "Rows" : {
            "Count" : 10,
            "Percent" : 100
          },
          "Sample" : [
            "Henderson",
            "Long",
            "Alexander",
            "Bailey"
          ]
        }
      },
      {
        "Index" : 2,
        "Label" : "city",
        "pp-Type" : "S",
        "pp-Attr" : "",
        "pp-Name" : "city",
        "pp-Sample" : "Ngou",
        "Bytes" : {
          "Count" : 91,
          "Percent" : 44.3902
        },
        "Rows" : {
          "Count" : 10,
          "Percent" : 100
        },
        "Length" : {
          "Min" : 4,
          "Max" : 18,
          "Avg" : 9.1
        },
        "Unique Estimate" : 10,
        "Type-String" : {
          "Rows" : {
            "Count" : 10,
            "Percent" : 100
          },
          "Sample" : [
            "Ngou",
            "Lendangara Satu",
            "Carazinho",
            "Pedro Leopoldo"
          ],
          "Sample-Has binary" : "Oborniki Śląskie"
        }
      },
      {
        "Index" : 3,
        "Label" : "donation",
        "pp-Type" : "I",
        "pp-Attr" : "",
        "pp-Name" : "donation",
        "pp-Sample" : "26",
        "Bytes" : {
          "Count" : 20,
          "Percent" : 9.7561
        },
        "Rows" : {
          "Count" : 10,
          "Percent" : 100
        },
        "Length" : {
          "Min" : 2,
          "Max" : 2,
          "Avg" : 2
        },
        "Unique Estimate" : 9,
        "Type-Integer" : {
          "Rows" : {
            "Count" : 10,
            "Percent" : 100
          },
          "Value" : {
            "Min" : 25,
            "Max" : 50
          },
          "Sample" : [
            "26",
            "27",
            "31",
            "35"
          ]
        }
      }
    ]
  }


``loginf`` breaks down each column.  Note column three which is the numerical column.  Since at first ``loginf`` does
not know if there is a header line, it identifies that 1/11 entries are strings, while the other 10/11 are integers.
If you know in advance how many lines to skip at the start of a file, can can use the `-f,
+n` attribute to skip the first n lines.

This is used for determining the column specification used in other AQ commands::

  loginf -f donations.csv -o_pp_col -

  S:lastname
  S:city
  I:donation

It is extremely helpful when integrating new datasets with the AQ tools.

Other Notes
===========

This utility also has the ability to store the output in a raw form that can be used to merge results from several
files.  This is most useful when an estimate of uniqueness is needed from a column in a set of log files that span a
length of time.  Refer to the ``../../reference/manpages/loginf`` manual for the full syntax.
