import pulumi

import json
from pulumi_aws import s3
from pulumi import Output

bucket = s3.Bucket("beginworld.exchange", force_destroy=True)


def allow_s3_bucket_access(s3_bucket, roles, lamda_function_arn):
    role_arns = [role.arn for role in roles]

    bucket_policy = Output.all(s3_bucket.arn, role_arns).apply(
        lambda args: json.dumps(
            {
                "Version": "2012-10-17",
                "Id": "MorgueFileBucketPolicy",
                "Statement": [
                    {
                        "Sid": "AllowThingsInTheBucket",
                        "Effect": "Allow",
                        "Principal": {"AWS": args[1]},
                        "Action": "s3:*",
                        "Resource": f"{args[0]}/*",
                    },
                ],
            }
        )
    )

    s3.BucketPolicy(
        "morgue-file-bucket-policy", bucket=s3_bucket.id, policy=bucket_policy
    )
