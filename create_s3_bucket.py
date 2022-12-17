from minio import Minio
from minio.error import InvalidResponseError
import json
import os

MINIO_API_PORT = os.environ['MINIO_API_PORT']
MINIO_ACCESS_KEY = os.environ['MINIO_ACCESS_KEY']
MINIO_SECRET_KEY = os.environ['MINIO_SECRET_KEY']
MLFLOW_S3_BUCKET_NAME = os.environ['MLFLOW_S3_BUCKET_NAME']

minioClient = Minio(f"http://localhost:{MINIO_API_PORT}".split('//')[1],
                  access_key=MINIO_ACCESS_KEY,
                  secret_key=MINIO_SECRET_KEY,
                  secure=False)

minioClient.list_buckets()

try:
    minioClient.make_bucket(MLFLOW_S3_BUCKET_NAME)
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
            "Resource":f"arn:aws:s3:::{MLFLOW_S3_BUCKET_NAME}"
            },
            {
            "Sid":"",
            "Effect":"Allow",
            "Principal":{"AWS":"*"},
            "Action":"s3:ListBucket",
            "Resource":f"arn:aws:s3:::{MLFLOW_S3_BUCKET_NAME}"
            },
            {
            "Sid":"",
            "Effect":"Allow",
            "Principal":{"AWS":"*"},
            "Action":"s3:GetObject",
            "Resource":f"arn:aws:s3:::{MLFLOW_S3_BUCKET_NAME}/*"
            },
            {
            "Sid":"",
            "Effect":"Allow",
            "Principal":{"AWS":"*"},
            "Action":"s3:PutObject",
            "Resource":f"arn:aws:s3:::{MLFLOW_S3_BUCKET_NAME}/*"
            }

        ]}

minioClient.set_bucket_policy(MLFLOW_S3_BUCKET_NAME, json.dumps(policy))

# List all object paths in bucket that begin with my-prefixname.
objects = minioClient.list_objects(MLFLOW_S3_BUCKET_NAME, prefix='my',
                              recursive=True)
for obj in objects:
    print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
          obj.etag, obj.size, obj.content_type)