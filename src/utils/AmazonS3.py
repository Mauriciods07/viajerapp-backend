import boto3
from decouple import config
from werkzeug.utils import secure_filename
import uuid

s3 = boto3.client(
    service_name=config('SERVICE_NAME'),
    region_name=config('REGION_NAME'),
    aws_access_key_id=config('AWS_ACCESS_KEY'),
    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
)


def upload_file_to_s3(file, new_name, acl="public-read"):
    filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(
            file,
            config('AWS_BUCKET_NAME'),
            new_name,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        return e
    
    return file.filename


def delete_file_from_s3(file):
    try:
        s3.delete_object(
            Bucket=config('AWS_BUCKET_NAME'),
            Key=file
        )
    except Exception as e:
        return e
    
    return "OK"