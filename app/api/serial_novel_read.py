from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.core.s3_config import get_s3_client, BUCKET_NAME
import boto3

router = APIRouter()

# 연재 소설 작품명과 화수를 입력하면 해당 epub을 반환하는 라우터
@router.get("/read/{novel_id}/{num}")
async def get_presigned_url(novel_id: str, num: int, s3_client = Depends(get_s3_client)):
    epub_key = f"serial_novels/{novel_id}/chapter{num}.epub"
    
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