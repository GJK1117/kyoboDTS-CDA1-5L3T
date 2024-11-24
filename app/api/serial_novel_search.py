from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
from app.core.s3_config import get_s3_client, BUCKET_NAME
import re
import json

router = APIRouter()

@router.get("/search/{novel_name}")
def sn_search(novel_name: str, s3_client=Depends(get_s3_client)):
    metadata_path = f"serial_novels/{novel_name}/metadata.json"
    prefix = f"serial_novels/{novel_name}/"
    pattern = re.compile(r'chapter(\d+)\.epub')  # chapter{num}.epub 패턴
    
    try:
        # 1. S3에서 metadata.json 파일 가져오기
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=metadata_path)
        metadata_content = response['Body'].read().decode('utf-8')
        metadata = json.loads(metadata_content)
        
        # 2. S3에서 파일 목록 가져오기
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        if 'Contents' not in response:
            raise HTTPException(status_code=404, detail="No files found in S3 for the given novel.")

        # 3. chapter{num}.epub 파일만 필터링 및 회차 정보 생성
        episodes = []
        for obj in response['Contents']:
            key = obj['Key']
            match = pattern.search(key)
            if match:
                episode_id = int(match.group(1))
                episodes.append({
                    "episode_id": episode_id,
                    "episode_title": f"{episode_id}화"
                })

        if not episodes:
            raise HTTPException(status_code=404, detail="No chapters found in S3 for the given novel.")

        # 4. episodes 배열을 metadata에 추가
        metadata["episodes"] = sorted(episodes, key=lambda x: x["episode_id"])

        # 5. JSONResponse로 반환
        return JSONResponse(content=metadata)
    
    except ClientError:
        raise HTTPException(status_code=404, detail="Metadata not found in S3.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))