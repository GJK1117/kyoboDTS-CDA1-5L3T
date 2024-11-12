# 11월05일 업데이트 적용버전 
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.core.s3_config import s3_client, BUCKET_NAME
import boto3

router = APIRouter()

# 일반 도서의 ID을 입력하면 해당 epub을 반환하는 라우터
@router.get("/read/{book_id}")
async def get_presigned_url(book_id: str, chapter: int):
    epub_key = f"general_books/{book_id}/book.epub"
    
    try:
        # 프리사인드 URL 생성
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': epub_key},
            ExpiresIn=1800  # URL의 유효기간, 30분 (1800초)
        )
        return JSONResponse({"url": presigned_url})
    
    except boto3.exceptions.Boto3Error as e:
        raise HTTPException(status_code=500, detail="Could not generate presigned URL")

