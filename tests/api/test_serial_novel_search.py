import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.serial_novel_search import router  # FastAPI 라우터 가져오기
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
    metadata = {"title": "Serial Novel", "author": "Test Author"}
    s3.put_object(
        Bucket="library", Key="serial_novels/1/metadata.json", Body=json.dumps(metadata)
    )

    # 테스트용 에피소드 파일 업로드
    for i in range(1, 4):  # 1화 ~ 3화 업로드
        s3.put_object(
            Bucket="library", Key=f"serial_novels/1/chapter{i}.epub", Body=f"Content of Chapter {i}"
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


def test_valid_metadata_and_chapters(override_dependencies):
    """
    정상적으로 메타데이터와 회차 정보 반환을 테스트합니다.
    """
    response = client.get("/search/1")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_data = response.json()

    # 기대하는 메타데이터와 에피소드 정보
    expected_data = {
        "title": "Serial Novel",
        "author": "Test Author",
        "episodes": [
            {"episode_id": 1, "episode_title": "1화"},
            {"episode_id": 2, "episode_title": "2화"},
            {"episode_id": 3, "episode_title": "3화"},
        ]
    }
    assert response_data == expected_data, f"Metadata mismatch: {response_data}"


def test_missing_metadata(override_dependencies):
    """
    S3에서 메타데이터 파일이 누락된 경우를 테스트합니다.
    """
    response = client.get("/search/999")  # 존재하지 않는 소설 ID 호출
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    assert response_data == {"detail": "Metadata not found in S3."}, f"Unexpected error message: {response_data}"


def test_missing_chapters(override_dependencies, s3_client):
    """
    S3에 에피소드(chapter) 파일이 없는 경우를 테스트합니다.
    """
    # S3에 메타데이터만 업로드
    metadata = {"title": "Serial Novel", "author": "Test Author"}
    s3_client.put_object(
        Bucket="library", Key="serial_novels/1/metadata.json", Body=json.dumps(metadata)
    )
    
    response = client.get("/search/2")
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    assert response_data == {"detail": "Metadata not found in S3."}, f"Unexpected error message: {response_data}"


def test_empty_s3_folder(override_dependencies):
    """
    S3에 데이터가 전혀 없는 경우를 테스트합니다.
    """
    response = client.get("/search/empty")  # 비어있는 폴더 호출
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    assert response_data == {"detail": "Metadata not found in S3."}, f"Unexpected error message: {response_data}"