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
   :emphasize-lines: 3,6

   ess datastore select s3://*YourBucket* --aws_access_key=*AccessKey* --aws_secret_access_key=*SecretAccessKey*
   ess datastore scan
   ess datastore rule add "*.zip" "zipfiles" "YYMMDD.zip"
   ess datastore probe zipfiles --apply

   ess task stream zipfiles "*" "*" "gzip -3 -c -" --s3out=s3://*YourBucket*/gz/%path/%file.gz


We have Essentia group all files in an S3 bucket ending with ``.zip`` into a single category (line 3),
and then use the stream command (line 7) to convert the files one by one.

The list of files to process is broken up and shared amongst each worker node.  The scaling is linear: double your
cluster size and the conversion time will be cut in half!
