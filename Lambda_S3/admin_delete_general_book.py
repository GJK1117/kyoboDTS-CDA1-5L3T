import boto3
import os
import json

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        # book_id ������������
        book_id = event.get('pathParameters', {}).get('book_id')
        if not book_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'book_id' in pathParameters"})
            }
        
        # ��������� ������ ������
        prefix = f"general_books/{book_id}/"
        thumbnail_path = f"thumbnail/{book_id}.webp"

        # S3������ ��������� ������ ������ ������������
        objects_to_delete = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        delete_keys = []

        if 'Contents' in objects_to_delete:
            delete_keys.extend([{'Key': obj['Key']} for obj in objects_to_delete['Contents']])

        # ��������� ��������� ������
        delete_keys.append({'Key': thumbnail_path})

        if not delete_keys:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": f"No objects found for {prefix} or {thumbnail_path}"})
            }

        # S3 ������ ������
        s3.delete_objects(Bucket=BUCKET_NAME, Delete={'Objects': delete_keys})
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Successfully deleted folder {prefix} and thumbnail {thumbnail_path}"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
