import pulumi

import json
from pulumi_aws import s3, cloudfront, acm, Provider
from pulumi import Output

bucket = s3.Bucket("beginworld.exchange", force_destroy=True)

module_name = "beginworld-exchange"
s3_origin_id = module_name

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


# This Needs to be in us-east-1
cert = acm.Certificate("cert",
    domain_name="beginworld.exchange",
    tags={
        "Environment": "test",
    },
    validation_method="DNS")



s3_distribution = cloudfront.Distribution("s3Distribution",
    # aliases=[
    #     "beginworld.exchange",
    #     "www.beginworld.exchange"
    # ],
    default_cache_behavior={
        "allowedMethods": [
            "GET",
            "HEAD",
            "OPTIONS",
        ],
        "cachedMethods": [
            "GET",
            "HEAD",
        ],
        "defaultTtl": 3600,
        "forwardedValues": {
            "cookies": {
                "forward": "none",
            },
            "queryString": False,
        },
        "maxTtl": 86400,
        "minTtl": 0,
        "targetOriginId": s3_origin_id,
        "viewerProtocolPolicy": "allow-all",
    },
    default_root_object="index.html",
    enabled=True,
    is_ipv6_enabled=True,
    # logging_config={
    #     "bucket": "mylogs.s3.amazonaws.com",
    #     "includeCookies": False,
    #     "prefix": "myprefix",
    # },
    ordered_cache_behaviors=[
        {
            "allowedMethods": [
                "GET",
                "HEAD",
                "OPTIONS",
            ],
            "cachedMethods": [
                "GET",
                "HEAD",
                "OPTIONS",
            ],
            "compress": True,
            "defaultTtl": 86400,
            "forwardedValues": {
                "cookies": {
                    "forward": "none",
                },
                "headers": ["Origin"],
                "queryString": False,
            },
            "maxTtl": 31536000,
            "minTtl": 0,
            "pathPattern": "/content/immutable/*",
            "targetOriginId": s3_origin_id,
            "viewerProtocolPolicy": "redirect-to-https",
        },
        {
            "allowedMethods": [
                "GET",
                "HEAD",
                "OPTIONS",
            ],
            "cachedMethods": [
                "GET",
                "HEAD",
            ],
            "compress": True,
            "defaultTtl": 3600,
            "forwardedValues": {
                "cookies": {
                    "forward": "none",
                },
                "queryString": False,
            },
            "maxTtl": 86400,
            "minTtl": 0,
            "pathPattern": "/content/*",
            "targetOriginId": s3_origin_id,
            "viewerProtocolPolicy": "redirect-to-https",
        },
    ],
    origins=[{
        "domain_name": bucket.bucket_regional_domain_name,
        "originId": s3_origin_id,
        # "s3OriginConfig": {
        #     "originAccessIdentity": "origin-access-identity/cloudfront/ABCDEFG1234567",
        # },
    }],
    # price_class="PriceClass_200",
    restrictions={
        "geoRestriction": {
            # "locations": [
            #     "US",
            #     "CA",
            #     "GB",
            #     "DE",
            # ],
            # "restrictionType": "whitelist",
            "restrictionType": "none",
        },
    },
    # tags={
    #     "Environment": "production",
    # },
    viewer_certificate={
        # "acmCertificateArn": cert.arn
        # "acmCertificateArn": "6baa0ec0-3774-4e3e-8611-7f2cb912e58b"
        # beginworld.exchange (6baa0ec0-3774-4e3e-8611-7f2cb912e58b)
        # "acmCertificateArn": "arn:aws:acm:us-west-2:851075464416:certificate/e0fe3065-bde6-4c1c-976a-936b085c3a49" => "6baa0ec0-3774-4e3e-8611-7f2cb912e58b"
    })
