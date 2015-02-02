Data Organization
-----------------

Essentia defines a resource that contains data a 'datastore'.  Current datastore types that are supported by Essentia
include a local disk drive, and an AWS S3 store (cloud based storage).  Regardless of the source,
Essentia can scan the files to organize them, allowing users to quickly process only the data they need to.


Features of the Essentia Scanner include:

1. Rule based grouping of files.  Rules are glob based pattern matching, allowing considerable freedom in selecting
data categories.

2. File scanner.  Essentia will scan the files to determine their common attributes, such as column names, number,
data type, file compression, field delimiter, and so on.  For log data, it also determines the date range that the file
covers.

3. Data summary.  Once rules are established, Essentia will update a master file list each time a scan is run,
and update the category summaries.  These include number of files, combined size in MB, date range covered, and so on.

4. Smart file select.  With files categorized and scanned, it is straightforward to select a subset of the data to
process.  In particular with log data, the user only needs to provide the date range of interest.  No need to provide
full filenames.


