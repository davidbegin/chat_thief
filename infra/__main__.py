import pulumi

import json
from pulumi_aws import s3
from pulumi import Output

bucket = s3.Bucket("beginworld.exchange", force_destroy=True)

# acl: "public-read",

def allow_s3_bucket_access(s3_bucket):
    bucket_policy = Output.all(s3_bucket.arn).apply(
        lambda args: json.dumps(
            {
                "Version": "2012-10-17",
                "Id": "BeginWorldExchange",
                "Statement": [
                    {
                        "Sid": "PublicAccess",
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": "s3:Get*",
                        "Resource": f"{args[0]}/*",
                    },
                    {
                        "Sid": "BeginWriteAccess",
                        "Effect": "Allow",
                        "Principal": {"AWS": "arn:aws:iam::851075464416:root" },
                        "Action": "s3:Put*",
                        "Resource": f"{args[0]}/*",
                    },
                ],
            }
        )
    )

    s3.BucketPolicy(
        "beginworld-exchange-bucket-policy", bucket=s3_bucket.id, policy=bucket_policy
    )

allow_s3_bucket_access(bucket)
