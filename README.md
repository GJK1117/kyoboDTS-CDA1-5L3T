# kyoboDTS-CDA1-5L3T
교보DTS-Cloud architecture DX Academy(CDA) 최종 프로젝트 Backend 저장소

# 최종프로젝트 주제: e-Book API 프로젝트
e-Book 서비스를 운영하는 고객사의 요구사항에 따라 AWS 아키텍처를 구성 및 이에 따라 기존 Back-end code를 리팩토링하는 프로젝트

## 디렉토리 구조
```
kyoboDTS-CDA1-5L3T
├── Dockerfile
├── Lambda_S3
│   ├── README.MD
│   ├── admin_delete_general_book.py
│   ├── admin_delete_serial_novel.py
│   ├── admin_register_general_book.py
│   ├── admin_register_serial_novel.py
│   └── admin_search_ebook.py
├── README.md
├── S3-RDS-Lambda(4종)
│   ├── EDIT_books.py
│   ├── EDIT_series.py
│   ├── PUT_books.py
│   ├── PUT_series.py
│   ├── README.MD
│   ├── [함수개요]datasync_general_book.MD
│   ├── [함수개요] datasync_S3toRDS_updates.MD
│   ├── [함수개요]datasync_S3toRDS_generalbooks.MD
│   └── [함수개요]datasync_serial_novels.MD
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── general_book_read.py
│   │   ├── general_book_search.py
│   │   ├── list_ebook.py
│   │   ├── search_ebooks.py
│   │   ├── serial_novel_read.py
│   │   └── serial_novel_search.py
│   ├── core
│   │   ├── config.py
│   │   ├── rds_config.py
│   │   └── s3_config.py
│   ├── data
│   │   ├── README.MD
│   │   └── metadata.json
│   ├── main.py
│   └── schema
│       └── mysql_schema.py
├── data
│   ├── README.MD
│   └── metadata.json
├── pytest.ini
├── requirements.txt
└── tests
    └── api
        ├── test_general_book_read.py
        ├── test_general_book_search.py
        ├── test_list_ebooks.py
        ├── test_search_ebooks.py
        ├── test_serial_novel_read.py
        └── test_serial_novel_search.py
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

빈칸

## API Route 설명

### 일반 도서 eBook 검색 API(임시)

- **경로**: `/general_book/search`
- **메서드**: `GET`
- **파일위치**: `/app/api/general_book_search.py`
- **설명**: 제목, 저자 등을 기준으로 일반 도서 eBook을 검색
- **요청 파라미터**:
  - `query` (string, 필수): 검색어
  - `page` (integer, 선택): 페이지 번호, 기본값은 1
- **응답**:
  - **200 OK**: 검색된 도서 목록 (책 ID, 제목, 저자, 요약 등 포함)

### 일반 도서 eBook 열람 API(임시)

- **경로**: `/general_book/read/{book_id}`
- **메서드**: `POST`
- **파일위치**: `/app/api/general_book_read.py`
- **설명**: 특정 도서 ID에 해당하는 일반 도서 eBook을 열람
- **요청 경로 변수**:
  - `book_id` (integer, 필수): 열람할 도서의 ID
- **응답**:
  - **200 OK**: 도서의 상세 정보 및 본문 내용
  - **404 Not Found**: 해당 ID의 도서가 존재하지 않을 때 반환

### 연재 소설 eBook 검색 API(임시)

- **경로**: `/serial_novel/search`
- **메서드**: `GET`
- **파일위치**: `/app/api/serial_novel_search.py`
- **설명**: 제목, 저자 등을 기준으로 연재 소설 eBook을 검색
- **요청 파라미터**:
  - `query` (string, 필수): 검색어
  - `page` (integer, 선택): 페이지 번호, 기본값은 1
- **응답**:
  - **200 OK**: 검색된 연재 소설 목록 (소설 ID, 제목, 작가, 요약 등 포함)

### 연재 소설 eBook 열람 API(임시)

- **경로**: `/serial-novels/read/{book_id}`
- **메서드**: `POST`
- **파일위치**: `/app/api/serial_novel_read.py`
- **설명**: 특정 연재 소설 ID에 해당하는 eBook을 열람
- **요청 경로 변수**:
  - `novel_id` (integer, 필수): 열람할 소설의 ID
- **응답**:
  - **200 OK**: 소설의 상세 정보 및 본문 내용
  - **404 Not Found**: 해당 ID의 소설이 존재하지 않을 때 반환
