# Metadata 저장 및 Pre-Signed URL 생성

## 기능 개요

이 Lambda 함수는 API Gateway를 통해 요청을 받아 S3 버킷에 메타데이터를 저장하고, EPUB 파일 및 썸네일 이미지를 업로드할 수 있는 Pre-Signed URL을 생성합니다.

## 주요 기능

1. **S3에 메타데이터 저장**
    * API 요청에서 전달된 `metadata.json` 파일을 S3 버킷의 다음 경로에 저장합니다:

      ```
      serial_novels/{book_id}/metadata.json
      ```

2. **Pre-Signed URL 생성**
    * EPUB 파일과 썸네일 이미지를 업로드할 수 있도록 5분 동안 유효한 Pre-Signed URL을 생성합니다.
    * 생성된 URL의 경로는 다음과 같습니다:
        * EPUB 파일: `serial_novels/{book_id}/chapter1.epub`
        * 썸네일 이미지: `thumbnail/{book_id}.webp`

3. **입력 데이터 검증**
    * `metadata` 필드가 요청에 포함되지 않은 경우, HTTP 상태 코드 400을 반환합니다.

4. **에러 처리**
    * S3 업로드 또는 URL 생성 중 오류 발생 시, 상태 코드 500과 함께 상세 오류 메시지를 반환합니다.

## 작동 방식

1. **API 요청 처리**
    * 요청 경로 (`pathParameters`) 에서 `book_id` 값을 추출합니다.
    * 요청 본문 (`body`) 에서 metadata JSON 데이터를 추출합니다.

2. **메타데이터 업로드**
    * JSON 데이터를 `metadata.json` 파일로 변환하여 S3 버킷의 적절한 경로에 업로드합니다.

3. **Pre-Signed URL 생성**
    * S3 버킷에 EPUB 파일과 썸네일 이미지를 업로드할 수 있는 Pre-Signed URL을 생성하여 반환합니다.

4. **응답 반환**
    * 성공 시, 다음 정보를 포함하는 HTTP 상태 코드 200 응답을 반환합니다:
        * 성공 메시지
        * EPUB 및 썸네일 업로드를 위한 Pre-Signed URL

## 예시 응답

### 성공 시

```json
{
  "message": "Metadata saved successfully",
  "epub_upload_url": "<pre-signed-epub-url>",
  "thumbnail_upload_url": "<pre-signed-thumbnail-url>"
}