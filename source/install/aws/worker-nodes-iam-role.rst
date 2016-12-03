***********************************************
IAM Role: Creating Worker Nodes for Scalability
***********************************************

This IAM role provides full access to EC2 and allows worker nodes to obtain their own IAM role::

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
            }
        ]
    }

