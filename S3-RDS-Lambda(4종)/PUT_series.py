# PUT Triggered Lambda Function: 연재소설 <datasync_general_book>

import boto3
import json
from sqlmodel import create_engine, Session, SQLModel, Field, select
import os

# RDS Connection String
RDS_CONNECTION_STRING = f"mysql+pymysql://{os.environ['RDS_USER']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOST']}/ebook"
engine = create_engine(RDS_CONNECTION_STRING)

# S3 Client
s3 = boto3.client("s3")


# ORM Model for Series Table
class Series(SQLModel, table=True):
    __tablename__ = "Series"
    series_id: int = Field(primary_key=True)
    series_name: str
    series_author: str = None
    upload_day: str
    thumbnail: str = None


def lambda_handler(event, context):
    try:
        records = event.get('Records', [])
        for record in records:
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']
            event_name = record['eventName']

            print(f"Bucket: {bucket_name}, Key: {object_key}, Event: {event_name}")

            # Handle events for metadata JSON files
            if object_key.endswith(".json"):
                handle_update_event(bucket_name, object_key)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Event processed successfully"})
        }
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error processing S3 event", "error": str(e)})
        }


def handle_update_event(bucket_name, object_key):
    """Handles updates to S3 metadata JSON files."""
    # Ensure the file is in the serial_novels directory and is a .json file
    parts = object_key.split('/')
    if len(parts) < 3 or parts[0] != "serial_novels":
        print(f"Skipping invalid or non-metadata file: {object_key}")
        return

    series_name = parts[1]

    try:
        # Fetch and parse JSON metadata
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        json_data = json.loads(response['Body'].read().decode('utf-8'))

        # Extract relevant fields from the JSON file
        title = json_data.get("title")  # Maps to `series_name`
        author = json_data.get("author")  # Maps to `series_author`
        upload_day = json_data.get("upload_day")  # Maps to `upload_day`
        thumbnail = json_data.get("thumbnail")  # Maps to `thumbnail`

        # Debugging logs
        print(
            f"Debug: Parsed fields - title='{title}', author='{author}', upload_day='{upload_day}', thumbnail='{thumbnail}'")

        # Validate required fields
        if not title or not upload_day:
            print(f"Missing required fields in metadata: title={title}, upload_day={upload_day}. Skipping.")
            return

        with Session(engine) as session:
            # Check if the series exists
            series = session.exec(select(Series).where(Series.series_name == title)).first()

            if series:
                # Update existing series metadata
                series.series_author = author if author else series.series_author
                series.upload_day = upload_day or series.upload_day
                series.thumbnail = thumbnail or series.thumbnail
                session.commit()
                print(f"Updated metadata for series '{title}'")
            else:
                # Insert a new series entry
                new_series = Series(
                    series_name=title,
                    series_author=author,
                    upload_day=upload_day,
                    thumbnail=thumbnail
                )
                session.add(new_series)
                session.commit()
                print(f"Added new series '{title}'")
    except Exception as e:
        print(f"Error processing metadata file {object_key}: {str(e)}")
