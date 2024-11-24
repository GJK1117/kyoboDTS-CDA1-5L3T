import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.general_book_read import router
from app.core.s3_config import get_s3_client  # FastAPI 의존성 가져오기
import boto3

# FastAPI 앱 생성 및 라우터 추가
app = FastAPI()
app.include_router(router)

# FastAPI TestClient 생성
client = TestClient(app)

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
    s3.put_object(Bucket="library", Key="general_books/1/book.epub", Body=b"test content")
    yield s3


@pytest.fixture
def override_dependencies(s3_client):
    """
    FastAPI 의존성 주입을 테스트용으로 오버라이드합니다.
    """
    def test_s3_client_override():
        return s3_client

    # 의존성 오버라이드
    app.dependency_overrides[get_s3_client] = test_s3_client_override
    yield
    # 의존성 오버라이드 해제
    app.dependency_overrides.pop(get_s3_client, None)


def test_valid_presigned_url(override_dependencies):
    """
    정상적으로 프리사인드 URL 반환을 테스트합니다.
    """
    response = client.get("/read/1")  # FastAPI 엔드포인트 호출
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    assert "url" in response_data, "Missing URL in response"
    assert response_data["url"].startswith("http://") or response_data["url"].startswith("https://"), "Invalid URL format"


def test_presigned_url_for_missing_object(override_dependencies):
    """
    S3 객체가 없을 때도 프리사인드 URL을 반환하도록 테스트합니다.
    """
    response = client.get("/read/999")  # 존재하지 않는 book_id 호출
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"  # URL은 정상적으로 반환되어야 함
    response_data = response.json()
    assert "url" in response_data, "Missing URL in response"
    assert response_data["url"].startswith("http://") or response_data["url"].startswith("https://"), "Invalid URL format"