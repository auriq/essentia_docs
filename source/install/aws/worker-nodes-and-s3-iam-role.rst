********************************************************************************
IAM Role: Creating Worker Nodes for Scalability and Accessing or Writing S3 Data
********************************************************************************

This IAM role provides full access to EC2, allows worker nodes to obtain their own IAM role, and provides full access to S3 and
accessing or writing S3 data::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:*"
                ],
                "Resource": [
                    "*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "iam:PassRole"
                ],
                "Resource": [
                    "*"
                ]
            },
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

