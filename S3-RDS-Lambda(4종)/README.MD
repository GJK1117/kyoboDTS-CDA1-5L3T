# Lambda 함수 설명
> 파일별 상세 기능은 위 [함수개요]파일들 참고하도록 

## 개요

이 프로젝트는 4개의 Lambda 함수를 사용하여 S3와 RDS 간의 데이터 동기화를 자동화하고 e-Book 플랫폼의 핵심 기능을 지원합니다. 각 Lambda 함수는 특정 S3 이벤트에 의해 트리거되며, 데이터 처리 및 데이터베이스 업데이트를 수행합니다.

## Lambda 함수 목록

### 1. `datasync_general_books_metadata`

*   **트리거:** S3 `general_books` 버킷에 `metadata.json` 파일이 업로드 또는 수정될 때 (`ObjectCreated`, `ObjectModified`)
*   **기능:**
    *   `metadata.json` 파일에서 도서 메타데이터 (제목, 저자, 출판일 등) 추출
    *   RDS `Book` 테이블에 해당 도서 정보 업데이트 또는 추가
*   **목적:** 일반 도서의 메타데이터를 RDS와 동기화

### 2. `datasync_serial_novels_metadata`

*   **트리거:** S3 `serial_novels` 버킷에 `metadata.json` 파일이 업로드 또는 수정될 때 (`ObjectCreated`, `ObjectModified`)
*   **기능:**
    *   `metadata.json` 파일에서 연재 소설 메타데이터 (제목, 저자, 연재 요일, 썸네일 등) 추출
    *   RDS `Series` 테이블에 해당 연재 소설 정보 업데이트 또는 추가
*   **목적:** 연재 소설의 메타데이터를 RDS와 동기화

### 3. `datasync_S3toRDS_updates`

*   **트리거:** S3 `serial_novels` 버킷에 `.epub` 파일이 업로드될 때 (`ObjectCreated`)
*   **기능:**
    *   `.epub` 파일 이름에서 에피소드 ID 및 제목 추출
    *   RDS `Content` 테이블에 해당 에피소드 정보 업데이트 또는 추가
*   **목적:** 연재 소설의 에피소드 정보를 RDS와 동기화

### 4. `generate_presigned_url_for_s3_upload`

*   **트리거:** API Gateway를 통한 HTTP 요청
*   **기능:**
    *   요청 본문에서 `book_id` 및 메타데이터 추출
    *   S3 버킷에 `metadata.json` 파일 업로드
    *   EPUB 파일 및 썸네일 이미지 업로드를 위한 Pre-signed URL 생성
*   **목적:**  API를 통해 S3에 파일 업로드를 위한 Pre-signed URL 제공

## 추가 정보

*   각 Lambda 함수는 CloudWatch를 통해 로그를 기록하며, 오류 발생 시 상세 정보를 확인할 수 있습니다.
*   Lambda 함수는 IAM 역할을 통해 S3 및 RDS에 대한 접근 권한을 관리합니다.
*   보안을 위해 API Gateway는 HTTPS 연결을 사용하며, AWS Certificate Manager를 통해 인증서를 관리합니다.

## 참고

*   [Lambda 함수 코드](./lambda_functions)
*   [API Gateway 설정](./api_gateway)
*   [AWS Lambda 개발자 가이드](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
