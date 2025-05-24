import boto3
from botocore.exceptions import ClientError
from config import aws_access_key, aws_secret_key

def s3_upload_file(file_path, bucket, object_name=None):
    from utils.logger import log_info, log_error
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    try:
        s3_client.upload_file(file_path, bucket, object_name or file_path)
        print(f"File {file_path} uploaded successfully to AWS S3 bucket:- {bucket} object:-/{object_name}")
        log_info(f"File {file_path} uploaded successfully to AWS S3 bucket:- {bucket} object:-/{object_name}")
        return True
    except ClientError as e:
        print(f"Error uploading file: {e}")
        log_error(f"Error uploading file: {e}")
        return False
    
