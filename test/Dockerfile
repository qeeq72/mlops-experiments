FROM python:3.10-slim

RUN apt update && \
    apt install s3fs -y && \
    mkdir /mnt/s3

WORKDIR /mnt/scripts

ENTRYPOINT echo ${ACCESS_KEY_ID}:${SECRET_ACCESS_KEY} > ${HOME}/.passwd-s3fs && \
            chmod 600 ${HOME}/.passwd-s3fs && \
            s3fs ${S3_BUCKET} /mnt/s3 -o passwd_file=${HOME}/.passwd-s3fs -o use_path_request_style -o url=${S3_URL} && \
            python main.py

CMD []