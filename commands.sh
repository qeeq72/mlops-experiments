# Build MLflow image
docker build -t mlflow .

# Build Test image
docker build -t test .

# s3fs
echo ${MINIO_ACCESS_KEY}:${MINIO_SECRET_KEY} > ${HOME}/.passwd-s3fs
chmod 600 ${HOME}/.passwd-s3fs

s3fs fuse ${MLOPS_PATH}/minio/fuse -o passwd_file=${HOME}/.passwd-s3fs -o use_path_request_style -o url=http://0.0.0.0:${MINIO_API_PORT}
fusermount -u ${MLOPS_PATH}/minio/fuse

# Create buckets
python create_s3_bucket.py --bucket ${MLFLOW_S3_BUCKET_NAME}
python create_s3_bucket.py --bucket ${FUSE_S3_BUCKET_NAME}