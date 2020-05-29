import boto3
from pprint import pprint
AWS_KEY_ID = 'AKIATPZTS3RW53DJBFDU'
AWS_SECRET = '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'

s3 = boto3.client("s3",
                  region_name="us-east-1",
                  aws_access_key_id=AWS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET)

#create bucket
response = s3.create_bucket(Bucket='yuchio')

#bucket list
bucket_response=s3.list_buckets()
pprint(bucket_response)
