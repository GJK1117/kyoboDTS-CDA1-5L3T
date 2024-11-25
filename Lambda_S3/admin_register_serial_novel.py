import boto3
import json
import os

# S3 ��������������� ������
s3 = boto3.client('s3')

# ������ ������������ S3 ������ ������ ������������
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        # ������ ������������������ book_id ������
        book_id = event['pathParameters']['book_id']

        # ������ ������������ metadata ������
        body = json.loads(event['body'])
        metadata = body.get('metadata')

        if not metadata:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # ������ ��������� ������
                    "Access-Control-Allow-Methods": "OPTIONS,POST",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": json.dumps({"message": "Missing metadata in request body"})
            }

        # S3��� metadata.json ������
        metadata_path = f"serial_novels/{book_id}/metadata.json"
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=metadata_path,
            Body=json.dumps(metadata),
            ContentType='application/json'
        )

        # Pre-Signed URL ������ (epub ��� thumbnail)
        epub_path = f"serial_novels/{book_id}/chapter1.epub"
        thumbnail_path = f"thumbnail/{book_id}.webp"

        epub_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': epub_path, 'ContentType': 'application/epub+zip'},
            ExpiresIn=300,  # URL ������ ������ 5���
            HttpMethod='PUT'
        )

        thumbnail_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': thumbnail_path, 'ContentType': 'image/webp'},
            ExpiresIn=300,  # URL ������ ������ 5���
            HttpMethod='PUT'
        )

        # ������ ������
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # ������ ��������� ������
                "Access-Control-Allow-Methods": "OPTIONS,POST",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "message": "Metadata saved successfully",
                "epub_upload_url": epub_url,
                "thumbnail_upload_url": thumbnail_url
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # ������ ��������� ������
                "Access-Control-Allow-Methods": "OPTIONS,POST",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"message": "Error processing request", "error": str(e)})
        }

