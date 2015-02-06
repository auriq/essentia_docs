Compression Format Conversion
=============================

Recently we had a client who had thousands of log files in .zip format on an S3 bucket.  They wanted to use EMR
(Amazon's cloud based implementation of Hadoop), but EMR only natively supports gzip, bzip2, and LZO.  We were able to
very quickly handle this task, by simply using Essentia's scalability and stream based processing to uncompress, read,
and recompress all on the fly::

    ess datastore select s3://*YourBucket* --aws_access_key=*AccessKey* --aws_secret_access_key=*SecretAccessKey*
    ess datastore scan
    ess datastore rule add "*.zip" "zipfiles" "YYMMDD.zip" ## rule to change, select the patterns that match your files.
    ess datastore probe zipfiles --apply
    ess datastore summary

    ess task stream zipfiles "*" "*" "gzip -3 -c -" --s3out=s3://*YourBucket*/gz/%path/%file.gz --debug

This trick is also effective for users who simply want to move their raw data onto Redshift, which also cannot handle
zip compression natively.  Assuming the steps above were run, one can simply issue the following SQL command to
Redshift::
        
    COPY tablename FROM 's3://*YourBucket*/gz/'
    WITH CREDENTIALS 'aws_access_key_id=<access-key-id>;aws_secret_access_key=<secret-access-key>'

With a few simple lines in Essentia, you can easily convert any .zip compression files to .gz format and load them into your Redshift table.