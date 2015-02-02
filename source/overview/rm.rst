Resource Management
-------------------

Essentia leverages the power of the cloud to scale analyses as needed.  One major advantage to using Amazon S3 as a
datastore is that the data is redundantly stored on multiple disks.  This enables multiple files to be read without
being I/O bound.

To harness that, Essentia can launch worker nodes based on AWS EC2 instances.  The master node then coordinates which
files each worker node should process.  This allows for near linear scalability in the processing of many files.