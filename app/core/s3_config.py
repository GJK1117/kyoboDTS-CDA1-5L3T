from contextlib import asynccontextmanager
from fastapi import FastAPI
import boto3

s3_client = None
BUCKET_NAME="test"

@asynccontextmanager
async def lifespan(app: FastAPI):
    global s3_client
    # 앱 시작 시점에서 S3 클라이언트 초기화
    s3_client = boto3.client("s3") or get_s3_client()
    yield  # 앱이 실행되는 동안
    # 앱 종료 시점에서 S3 클라이언트 해제 (필요 시)
    s3_client = None

def get_s3_client(
    endpoint_url=None,
    aws_access_key_id=None,
    aws_secret_access_key=None,
    region_name=None
):
    # 환경 변수에서 값을 가져오거나 기본값을 사용하여 S3 클라이언트 생성
    return boto3.client(
        "s3",
        endpoint_url=endpoint_url or "http://localhost:4566",
        aws_access_key_id=aws_access_key_id or "test",
        aws_secret_access_key=aws_secret_access_key or "test",
        region_name=region_name or "us-east-1"
    )