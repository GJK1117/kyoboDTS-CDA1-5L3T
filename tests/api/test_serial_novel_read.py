import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.serial_novel_read import router
from app.core.s3_config import get_s3_client
import boto3

# FastAPI 앱 생성 및 라우터 추가
app = FastAPI()
app.include_router(router)

client = TestClient(app)  # FastAPI 앱으로 테스트 클라이언트 생성

@pytest.fixture
def s3_client():
    """
    LocalStack S3 클라이언트를 설정하고 테스트 데이터를 업로드합니다.
    """
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:4566",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )

    # 버킷 생성
    s3.create_bucket(Bucket="library")

    # 테스트용 파일 업로드
    s3.put_object(Bucket="library", Key="serial_novels/1/chapter1.epub", Body=b"Chapter 1 content")
    yield s3

@pytest.fixture
def override_dependencies(s3_client):
    """
    의존성 주입을 오버라이드하여 테스트용 S3 클라이언트를 사용합니다.
    """
    def test_s3_client_override():
        return s3_client

    # 의존성 주입
    app.dependency_overrides[get_s3_client] = test_s3_client_override
    yield
    app.dependency_overrides.clear()

def test_valid_presigned_url(override_dependencies):
    """
    정상적으로 프리사인드 URL 반환을 테스트합니다.
    """
    response = client.get("/read/1/1")
    assert response.status_code == 200
    response_data = response.json()
    assert "url" in response_data, "Missing URL in response"
    assert response_data["url"].startswith("http://") or response_data["url"].startswith("https://"), "Invalid URL format"

def test_presigned_url_for_missing_object(override_dependencies):
    """
    S3 객체가 없을 때도 프리사인드 URL을 반환하도록 테스트합니다.
    """
    response = client.get("/read/1/3")  # 존재하지 않는 chapter 호출

    # 프리사인드 URL은 S3 객체 유무와 관계없이 생성 가능하므로, HTTP 200을 기대합니다.
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # 응답 데이터 검증
    response_data = response.json()
    assert "url" in response_data, "Missing URL in response"
    assert response_data["url"].startswith("http://") or response_data["url"].startswith("https://"), "Invalid URL format"