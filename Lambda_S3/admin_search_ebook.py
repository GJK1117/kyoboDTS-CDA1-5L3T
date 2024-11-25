import os
import boto3
import json
from botocore.exceptions import ClientError

# ÌôòÍ≤ΩÎ≥ÄÏàòÏóêÏÑú S3 Î≤ÑÌÇ∑ Ïù¥Î¶Ñ Í∞ÄÏ†∏Ïò§Í∏∞
BUCKET_NAME = os.getenv("BUCKET_NAME")

# S3 ÌÅ¥ÎùºÏù¥Ïñ∏Ìä∏ ÏÉùÏÑ±
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    book_id = event['pathParameters']['book_id']
    
    # Í≤ÄÏÉâÌï† Í≤ΩÎ°ú Î¶¨Ïä§Ìä∏
    paths = [
        f"general_books/{book_id}/metadata.json",
        f"serial_novels/{book_id}/metadata.json"
    ]

    for path in paths:
        try:
            # S3ÏóêÏÑú metadata.json Í∞ÄÏ†∏Ïò§Í∏∞
            response = s3_client.get_object(Bucket=BUCKET_NAME, Key=path)
            metadata_content = response['Body'].read().decode('utf-8')
            metadata = json.loads(metadata_content)
            
            # ÏÑ±Í≥µ ÏùëÎãµ Î∞òÌôò
            return {
                "statusCode": 200,
                "body": json.dumps(metadata)
            }
        except ClientError as e:
            # NoSuchKey Ïò§Î•òÏù∏ Í≤ΩÏö∞, Îã§Ïùå Í≤ΩÎ°úÎ°ú ÏßÑÌñâ
            if e.response['Error']['Code'] == "NoSuchKey":
                continue
            # Í∏∞ÌÉÄ ÏóêÎü¨Îäî 500 Î∞òÌôò
            return {
                "statusCode": 500,
                "body": json.dumps({"detail": "Internal server error."})
            }
    
    # Îëê Í≤ΩÎ°ú Î™®ÎëêÏóêÏÑú ÌååÏùºÏùÑ Ï∞æÏßÄ Î™ªÌïú Í≤ΩÏö∞
    return {
        "statusCode": 404,
        "body": json.dumps({"detail": "Metadata not found in any path."})
    }
