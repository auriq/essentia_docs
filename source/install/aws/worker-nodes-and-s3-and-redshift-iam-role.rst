****************************************
IAM Role: Worker Nodes, S3, and Redshift
****************************************

This IAM role provides full access to EC2, S3, and Redshift as well as allows worker nodes to obtain their own IAM role::

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
            },
            {
                "Effect": "Allow",
                "Action": [
                    "redshift:*"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }
