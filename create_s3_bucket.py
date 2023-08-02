from minio import Minio
from minio.error import InvalidResponseError
import json
from dotenv import load_dotenv
import os
import argparse

load_dotenv()
MINIO_API_PORT = os.environ['MINIO_API_PORT']
MINIO_ACCESS_KEY = os.environ['MINIO_ACCESS_KEY']
MINIO_SECRET_KEY = os.environ['MINIO_SECRET_KEY']

parser = argparse.ArgumentParser()
parser.add_argument("--bucket", help="Bucket name to be created")
args = parser.parse_args()
bucket_name = args.bucket

minioClient = Minio(f"http://localhost:{MINIO_API_PORT}".split('//')[1],
                  access_key=MINIO_ACCESS_KEY,
                  secret_key=MINIO_SECRET_KEY,
                  secure=False)

minioClient.list_buckets()

try:
    minioClient.make_bucket(bucket_name)
except InvalidResponseError as err:
    print(err)

buckets = minioClient.list_buckets()
for bucket in buckets:
    print(bucket.name, bucket.creation_date)

policy = {"Version":"2012-10-17",
        "Statement":[
            {
            "Sid":"",
            "Effect":"Allow",
            "Principal":{"AWS":"*"},
            "Action":"s3:GetBucketLocation",
            "Resource":f"arn:aws:s3:::{bucket_name}"
            },
            {
            "Sid":"",
            "Effect":"Allow",
            "Principal":{"AWS":"*"},
            "Action":"s3:ListBucket",
            "Resource":f"arn:aws:s3:::{bucket_name}"
            },
            {
            "Sid":"",
            "Effect":"Allow",
            "Principal":{"AWS":"*"},
            "Action":"s3:GetObject",
            "Resource":f"arn:aws:s3:::{bucket_name}/*"
            },
            {
            "Sid":"",
            "Effect":"Allow",
            "Principal":{"AWS":"*"},
            "Action":"s3:PutObject",
            "Resource":f"arn:aws:s3:::{bucket_name}/*"
            }

        ]}

minioClient.set_bucket_policy(bucket_name, json.dumps(policy))

# List all object paths in bucket that begin with my-prefixname.
objects = minioClient.list_objects(bucket_name, prefix='my',
                              recursive=True)
for obj in objects:
    print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
          obj.etag, obj.size, obj.content_type)