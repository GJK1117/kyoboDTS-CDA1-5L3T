import boto3
import os
import json

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        # book_id Í∞ÄÏ†∏Ïò§Í∏∞
        book_id = event.get('pathParameters', {}).get('book_id')
        if not book_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'book_id' in pathParameters"})
            }
        
        # ÏÇ≠Ï†úÌï† Í≤ΩÎ°ú ÏÑ§Ï†ï
        prefix = f"general_books/{book_id}/"
        thumbnail_path = f"thumbnail/{book_id}.webp"

        # S3ÏóêÏÑú ÏÇ≠Ï†úÌï† Í∞ùÏ≤¥ Î™©Î°ù Í∞ÄÏ†∏Ïò§Í∏∞
        objects_to_delete = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        delete_keys = []

        if 'Contents' in objects_to_delete:
            delete_keys.extend([{'Key': obj['Key']} for obj in objects_to_delete['Contents']])

        # Ïç∏ÎÑ§Ïùº ÌååÏùºÎèÑ Ï∂îÍ∞Ä
        delete_keys.append({'Key': thumbnail_path})

        if not delete_keys:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": f"No objects found for {prefix} or {thumbnail_path}"})
            }

        # S3 Í∞ùÏ≤¥ ÏÇ≠Ï†ú
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
