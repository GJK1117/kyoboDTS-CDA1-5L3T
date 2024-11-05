## 도서 찾기 읽기 작동 확인 가이드

Root 디렉토리에 폴더 data/metadata.json 더미파일 추가
data/metadata.json  ``` {
    "title": "Sample Book",
    "author": "Author Name",
    "description": "A description of the sample book.",
    "chapters": 10
}
```

### 테스트용 Bucket 만들기 

aws --endpoint-url=http://localhost:4566 s3 mb s3://test-bucket

### 테스트 버켓 생성됬는지 확인

aws --endpoint-url=http://localhost:4566 s3 ls
— 
### Step 1. 더미 메타데이터 파일을 테스트 버켓에 업로드 

aws --endpoint-url=http://localhost:4566 s3 cp data/metadata.json s3://test-bucket/general_books/sample_book/metadata.json

### Step 2. 올라간지 확인 

aws --endpoint-url=http://localhost:4566 s3 ls s3://test-bucket/general_books/sample_book/

### Step 3. CURL로 request 가능한지 체크 
curl -X GET http://localhost:8000/

###Step 4. 읽기, 찾기 request 테스트 해보기 
- 읽기 
curl -X GET "http://localhost:8000/general_book/read/sample_book/1"
- 찾기 
curl -X GET "http://localhost:8000/general_book/search/sample_book"

---

## 결과창 (에러 확인):
* presigned_url —> NoneType 에러뜨는게 정상.
