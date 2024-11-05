from fastapi import APIRouter
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
from app.core.s3_config import s3_client, BUCKET_NAME
import json

router = APIRouter()

@router.get("/search/{novel_id}")
async def sn_search(novel_id: str):
    metadata_path = f"serial_novels/{novel_id}/metadata.json"
    try:
        # S3에서 metadata.json 가져오기
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=metadata_path)
        metadata_content = response['Body'].read().decode('utf-8')
        metadata = json.loads(metadata_content)
        
        # JSONResponse를 사용해 반환
        return JSONResponse(content=metadata)
    
    except ClientError as e:
        # 파일을 찾지 못한 경우, 404 상태 코드 반환
        return JSONResponse(content={"detail": "Metadata not found."}, status_code=404)