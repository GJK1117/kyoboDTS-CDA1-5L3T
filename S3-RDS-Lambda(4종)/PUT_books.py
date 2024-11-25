# PUT Triggered Lambda Function: 일반소설 <datasync_general_book>

import boto3
import json
from sqlmodel import create_engine, Session, SQLModel, Field, select
from typing import Optional
import os

# RDS Connection String (environment variables)
RDS_CONNECTION_STRING = f"mysql+pymysql://{os.environ['RDS_USER']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOST']}/ebook"
engine = create_engine(RDS_CONNECTION_STRING)

# Create S3 client
s3 = boto3.client('s3')


# Book model definition
class Book(SQLModel, table=True):
    __tablename__ = "Book"
    book_id: Optional[int] = Field(default=None, primary_key=True)
    book_name: str = Field(index=True, nullable=False)
    book_author: Optional[str] = Field(default=None)
    thumbnail: Optional[str] = Field(default=None)


# Lambda Handler
def lambda_handler(event, context):
    try:
        records = event.get('Records', [])
        if not records:
            raise ValueError("No records found in the event")

        for record in records:
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']

            # Log event details
            print(f"Processing S3 event: Bucket={bucket_name}, Key={object_key}")

            # Extract book_name from object key
            parts = object_key.split('/')
            if len(parts) < 2 or parts[0] != "general_books":
                raise ValueError(f"Invalid S3 key format for general_books: {object_key}")

            book_name = parts[1].replace(".epub", "").replace(".json", "")

            # Retrieve S3 object metadata or file content (if JSON)
            if object_key.endswith(".json"):
                process_json_metadata(bucket_name, object_key, book_name)
            elif object_key.endswith(".epub"):
                print(f"Skipping .epub file for now: {object_key}")
            else:
                print(f"Unsupported file type: {object_key}")
                continue

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Event processed successfully"})
        }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error processing event", "error": str(e)})
        }


def process_json_metadata(bucket_name, object_key, book_name):
    """Processes metadata from a JSON file."""
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        json_data = json.loads(response['Body'].read().decode('utf-8'))

        author = json_data.get('author')
        thumbnail_url = json_data.get('thumbnail')

        if not author and not thumbnail_url:
            print(f"JSON metadata for {object_key} contains no useful data. Skipping.")
            return

        # Database operation
        with Session(engine) as session:
            existing_book = session.exec(select(Book).where(Book.book_name == book_name)).first()

            if existing_book:
                print(f"Updating book: {book_name}")
                existing_book.book_author = author or existing_book.book_author
                existing_book.thumbnail = thumbnail_url or existing_book.thumbnail
                session.commit()
                print(f"Book {book_name} updated successfully.")
            else:
                print(f"Adding new book: {book_name}")
                new_book = Book(
                    book_name=book_name,
                    book_author=author,
                    thumbnail=thumbnail_url
                )
                session.add(new_book)
                session.commit()
                print(f"Book {book_name} added successfully.")

    except Exception as e:
        print(f"Error processing JSON metadata for {object_key}: {str(e)}")
        raise
