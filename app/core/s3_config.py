import os
import boto3

s3_client = None
BUCKET_NAME = os.getenv("BUCKET_NAME")
REGION_NAME = "ap-northeast-2"

def get_s3_client():
    return boto3.client("s3", region_name=REGION_NAME)