# kyoboDTS-CDA1-5L3T
교보DTS-Cloud architecture DX Academy(CDA) 최종 프로젝트 Backend 저장소

# 최종프로젝트 주제: e-Book API 프로젝트
e-Book 서비스를 운영하는 고객사의 요구사항에 따라 AWS 아키텍처를 구성 및 이에 따라 기존 Back-end code를 리팩토링하는 프로젝트

## 디렉토리 구조
```
/kyoboDTS-CDA1-5L3T
    /app
        /api
            __init__.py
            general_book_search.py
            general_book_read.py
            serial_novel_search.py
            serial_novel_read.py
        /core
            config.py
        main.py
    /tests
    .dockerignore
    .gitignore
    Dockerfile
    README.md
    requirements.txt
```

## 디렉토리 및 파일 설명

### `/`

프로젝트의 루트 디렉토리로, 프로젝트 설정 파일 및 주요 문서가 포함

- **`.dockerignore`**: Docker image에 제외시킬 파일 정의
- **`.gitignore`**: Git에서 무시할 파일 및 디렉토리를 지정
- **`Dockerfile`**: Docker image를 생성 설정 파일
- **`README.md`**: 프로젝트의 개요 및 문서
- **`requirements.txt`**: 필요 라이브러리 설치 리스트

### `/app`

주요 애플리케이션 디렉토리로, 핵심 API 구성 요소와 설정 파일이 포함

#### `/app/api`

eBook 서비스와 관련된 각 API 모듈이 포함된 디렉토리

- **`__init__.py`**: `api` 패키지를 초기화하여 모듈을 애플리케이션 전반에서 가져올 수 있도록 설정
- **`general_book_search.py`**: 일반 도서 검색 API 엔드포인트를 정의
- **`general_book_read.py`**: 일반 도서 열람 API 엔드포인트를 정의
- **`serial_novel_search.py`**: 연재 소설 검색 API 엔드포인트를 정의
- **`serial_novel_read.py`**: 연재 소설 열람 API 엔드포인트를 정의

#### `/app/core`

애플리케이션의 주요 설정 및 환경 구성이 포함된 디렉토리

- **`config.py`**: AWS 및 프로젝트 환경 변수, 데이터베이스 설정, API 키와 같은 애플리케이션 설정을 정의

#### `/app/main.py`

FastAPI 애플리케이션의 진입점으로, 앱을 초기화하고 `api` 모듈의 라우터를 등록하여 애플리케이션을 실행하는 파일

### `/tests`

테스트 파일을 저장하기에 적합한 디렉토리. 테스트 코드는 `/app/api` 디렉토리 구조에 맞춰서 배치하면 관리하기 용이

- 테스트 파일 예시:
  - `/tests/api/test_general_book_search.py`
  - `/tests/api/test_general_book_read.py`
  - `/tests/api/test_serial_novel_search.py`
  - `/tests/api/test_serial_novel_read.py`

## 사용법

### 필요 라이브러리

- **FastAPI**: Back-end 핵심 웹 프레임워크로, 빠르고 효율적인 API 구축 지원
- **Uvicorn**: FastAPI 애플리케이션을 ASGI 서버로 실행하기 위한 ASGI server
- **pytest**: 테스트 작성 및 실행을 위한 프레임워크

#### 설치 방법

```bash
pip install -r requirements.txt
```

### 애플리케이션 실행

FastAPI 애플리케이션을 실행하려면, 프로젝트의 루트 디렉토리에서 다음 명령어를 사용:

```bash
uvicorn app.main:app --reload
```

### 테스트 실행

## 추가 참고 사항