import os
import boto3
import json
from botocore.exceptions import ClientError

# ������������������ S3 ������ ������ ������������
BUCKET_NAME = os.getenv("BUCKET_NAME")

# S3 ��������������� ������
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    book_id = event['pathParameters']['book_id']
    
    # ��������� ������ ���������
    paths = [
        f"general_books/{book_id}/metadata.json",
        f"serial_novels/{book_id}/metadata.json"
    ]

    for path in paths:
        try:
            # S3������ metadata.json ������������
            response = s3_client.get_object(Bucket=BUCKET_NAME, Key=path)
            metadata_content = response['Body'].read().decode('utf-8')
            metadata = json.loads(metadata_content)
            
            # ������ ������ ������
            return {
                "statusCode": 200,
                "body": json.dumps(metadata)
            }
        except ClientError as e:
            # NoSuchKey ��������� ������, ������ ��������� ������
            if e.response['Error']['Code'] == "NoSuchKey":
                continue
            # ������ ��������� 500 ������
            return {
                "statusCode": 500,
                "body": json.dumps({"detail": "Internal server error."})
            }
    
    # ��� ������ ������������ ��������� ������ ������ ������
    return {
        "statusCode": 404,
        "body": json.dumps({"detail": "Metadata not found in any path."})
    }
