import boto3
import json
import os

# S3 ÌÅ¥ÎùºÏù¥Ïñ∏Ìä∏ ÏÉùÏÑ±
s3 = boto3.client('s3')

# ÌôòÍ≤Ω Î≥ÄÏàòÏóêÏÑú S3 Î≤ÑÌÇ∑ Ïù¥Î¶Ñ Í∞ÄÏ†∏Ïò§Í∏∞
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        # Í≤ΩÎ°ú ÌååÎùºÎØ∏ÌÑ∞ÏóêÏÑú book_id Ï∂îÏ∂ú
        book_id = event['pathParameters']['book_id']

        # ÏöîÏ≤≠ Î≥∏Î¨∏ÏóêÏÑú metadata Ï∂îÏ∂ú
        body = json.loads(event['body'])
        metadata = body.get('metadata')

        if not metadata:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # Î™®Îì† ÎèÑÎ©îÏù∏ ÌóàÏö©
                    "Access-Control-Allow-Methods": "OPTIONS,POST",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": json.dumps({"message": "Missing metadata in request body"})
            }

        # S3Ïóê metadata.json Ï†ÄÏû•
        metadata_path = f"serial_novels/{book_id}/metadata.json"
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=metadata_path,
            Body=json.dumps(metadata),
            ContentType='application/json'
        )

        # Pre-Signed URL ÏÉùÏÑ± (epub Î∞è thumbnail)
        epub_path = f"serial_novels/{book_id}/chapter1.epub"
        thumbnail_path = f"thumbnail/{book_id}.webp"

        epub_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': epub_path, 'ContentType': 'application/epub+zip'},
            ExpiresIn=300,  # URL Ïú†Ìö® ÏãúÍ∞Ñ 5Î∂Ñ
            HttpMethod='PUT'
        )

        thumbnail_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': thumbnail_path, 'ContentType': 'image/webp'},
            ExpiresIn=300,  # URL Ïú†Ìö® ÏãúÍ∞Ñ 5Î∂Ñ
            HttpMethod='PUT'
        )

        # ÏùëÎãµ Î∞òÌôò
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Î™®Îì† ÎèÑÎ©îÏù∏ ÌóàÏö©
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
                "Access-Control-Allow-Origin": "*",  # Î™®Îì† ÎèÑÎ©îÏù∏ ÌóàÏö©
                "Access-Control-Allow-Methods": "OPTIONS,POST",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"message": "Error processing request", "error": str(e)})
        }

