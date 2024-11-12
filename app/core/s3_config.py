import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
import boto3

s3_client = None
BUCKET_NAME = os.getenv("BUCKET_NAME")
REGION_NAME = "ap-northeast-2"

@asynccontextmanager
async def lifespan(app: FastAPI):
    global s3_client
    # 앱 시작 시점에서 S3 클라이언트 초기화
    s3_client = boto3.client("s3", region_name=REGION_NAME)
    yield  # 앱이 실행되는 동안
    # 앱 종료 시점에서 S3 클라이언트 해제 (필요 시)
    s3_client = None