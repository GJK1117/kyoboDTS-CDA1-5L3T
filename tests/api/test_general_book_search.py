import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.general_book_search import router  # FastAPI 라우터 가져오기
from app.core.s3_config import get_s3_client  # FastAPI 의존성 가져오기
import boto3
import json

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
        endpoint_url="http://localhost:4566",  # LocalStack 엔드포인트
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )

    # 버킷 생성
    s3.create_bucket(Bucket="library")

    # 테스트용 메타데이터 업로드
    metadata = {"title": "1984", "author": "George Orwell"}
    s3.put_object(
        Bucket="library", Key="general_books/1/metadata.json", Body=json.dumps(metadata)
    )
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
    # 오버라이드 해제
    app.dependency_overrides.pop(get_s3_client, None)


def test_valid_metadata_returned(override_dependencies):
    """
    정상적인 메타데이터 반환을 테스트합니다.
    """
    # API 호출 테스트
    response = client.get("/search/1")  # FastAPI 엔드포인트 호출
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    expected_data = {"title": "1984", "author": "George Orwell"}
    assert response_data == expected_data, f"Metadata mismatch: {response_data}"


def test_missing_metadata(override_dependencies):
    """
    존재하지 않는 메타데이터 반환을 테스트합니다.
    """
    response = client.get("/search/999")  # 존재하지 않는 book_id 호출
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"  # 상태 코드는 404이어야 함
    response_data = response.json()
    assert response_data == {"detail": "Metadata not found."}, "Error response mismatch"