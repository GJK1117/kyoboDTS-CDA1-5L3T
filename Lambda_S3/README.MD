# 관리자 API Lambda 함수 설명

---
## 개요

이 프로젝트는 5개의 Lambda 함수를 사용하여 관리자가 e-Book 플랫폼에 새로운 도서를 등록하고 관리할 수 있는 API를 제공합니다. 각 Lambda 함수는 API Gateway를 통해 HTTP 요청을 처리하며, S3 버킷과 상호 작용하여 파일 업로드 및 메타데이터 관리 기능을 수행합니다.

## Lambda 함수 목록

### 1. `admin_register_general_book`

*   **HTTP 메서드:** POST
*   **경로:** `/general_books/{book_id}`
*   **기능:**
    *   요청 본문에서 `book_id` 및 도서 메타데이터 추출
    *   S3 `general_books` 버킷에 `metadata.json` 파일 업로드
    *   EPUB 파일 및 썸네일 이미지 업로드를 위한 Pre-signed URL 생성
*   **목적:** 일반 도서 등록 및 파일 업로드를 위한 Pre-signed URL 제공

### 2. `admin_register_serial_novel`

*   **HTTP 메서드:** POST
*   **경로:** `/serial_novels/{book_id}`
*   **기능:**
    *   요청 본문에서 `book_id` 및 연재 소설 메타데이터 추출
    *   S3 `serial_novels` 버킷에 `metadata.json` 파일 업로드
    *   EPUB 파일 및 썸네일 이미지 업로드를 위한 Pre-signed URL 생성
*   **목적:** 연재 소설 등록 및 파일 업로드를 위한 Pre-signed URL 제공

### 3. `admin_delete_general_book`

*   **HTTP 메서드:** DELETE
*   **경로:** `/general_books/{book_id}`
*   **기능:**
    *   `book_id`를 기반으로 S3 `general_books` 버킷에서 해당 도서의 모든 파일 및 폴더 삭제
    *   S3 `thumbnail` 버킷에서 해당 도서의 썸네일 이미지 삭제
*   **목적:** 일반 도서 삭제

### 4. `admin_delete_serial_novel`

*   **HTTP 메서드:** DELETE
*   **경로:** `/serial_novels/{book_id}`
*   **기능:**
    *   `book_id`를 기반으로 S3 `serial_novels` 버킷에서 해당 연재 소설의 모든 파일 및 폴더 삭제
    *   S3 `thumbnail` 버킷에서 해당 연재 소설의 썸네일 이미지 삭제
*   **목적:** 연재 소설 삭제

### 5. `admin_search_ebook`

*   **HTTP 메서드:** GET
*   **경로:** `/ebook/{book_id}`
*   **기능:**
    *   `book_id`를 기반으로 S3 `general_books` 및 `serial_novels` 버킷에서 `metadata.json` 파일 검색
    *   검색된 메타데이터 파일 내용 반환
*   **목적:**  `book_id`를 사용하여 도서 정보 검색

## 추가 정보

*   각 Lambda 함수는 API Gateway와 통합되어 있으며, HTTP 요청을 통해 호출됩니다.
*   Pre-signed URL은 제한된 시간 동안 유효하며, 해당 URL을 통해 S3에 파일을 업로드할 수 있습니다.
*   모든 Lambda 함수는 CloudWatch를 통해 로그를 기록하며, 오류 발생 시 상세 정보를 확인할 수 있습니다.
*   Lambda 함수는 IAM 역할을 통해 S3에 대한 접근 권한을 관리합니다.
*   보안을 위해 API Gateway는 HTTPS 연결을 사용하며, AWS Certificate Manager를 통해 인증서를 관리합니다.

## 참고

*   [Lambda 함수 코드](./lambda_functions)
*   [API Gateway 설정](./api_gateway)
*   [AWS Lambda 개발자 가이드](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
