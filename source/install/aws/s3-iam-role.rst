**************************************
IAM Role: Accessing or Writing S3 Data
**************************************

This IAM role provides full access to S3 and allows accessing or writing S3 data::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:*"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }

