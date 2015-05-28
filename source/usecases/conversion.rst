*****************************
Compression Format Conversion
*****************************


Amazon's managed services (Redshift, EMR, etc) are able to read compressed data from S3 stores as long as they are
gzip, bz2, or lzo files.  Zip files however are incredibly common, therefore we built Essentia to handle them.

Although our interest in doing this was to stream data into our analytics backend, the feature also enables users to
use Essentia for mass conversion of files from one format into another.

The following code block shows how simple this is:

.. code-block:: sh
   :linenos:
   :emphasize-lines: 3,5

   ess datastore select s3://my-gz-data --credentials=mycreds.csv
   ess datastore select s3://my-zip-data --credentials=my-other-creds.csv
   ess datastore category add zipfiles "*.zip" --dateformat="YYMMDD.zip"

   ess task stream zipfiles "*" "*" "gzip -3 -c -" --s3out=s3://my-gz-data/converted/%path/%file.gz


Each time we 'register' a datastore with the ``select`` command, Essentia remembers it.  In the above example,
we register an bucket that we will use to store output.   Next we register the input bucket (my-zip-data).

We have Essentia group all ``.zip`` files in the 'my-zip-data' bucket into a single category (line 3),
and then use the stream command (line 5) to convert the files one by one, pushing the converted files into
a different bucket.  We could have used the same bucket for input or output, and we could have mixed local and s3
stores for either or both of the input and output.

The list of files to process is broken up and shared amongst each worker node.  The scaling is linear: double your
cluster size and the conversion time will be cut in half!
