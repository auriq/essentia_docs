*************************
IAM Role: Redshift Access
*************************

This IAM role provides full access to Redshift::

    {
        "Version": "2012-10-17",
        "Statement": [
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
                    "redshift:*"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }
