from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
from sqlmodel import select, Session
from app.core.s3_config import get_s3_client, BUCKET_NAME
from app.core.rds_config import get_read_replica_engine
from app.schema.mysql_schema import Series, Content
import json

router = APIRouter()

@router.get("/search/{novel_name}")
def sn_search(novel_name: str, s3_client = Depends(get_s3_client), session: Session = Depends(get_read_replica_engine)):
    metadata_path = f"serial_novels/{novel_name}/metadata.json"
    
    try:
        # 1. S3에서 metadata.json 파일 가져오기
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=metadata_path)
        metadata_content = response['Body'].read().decode('utf-8')
        metadata = json.loads(metadata_content)

        # 2. Series 테이블에서 series_id 가져오기
        series_query = select(Series.series_id).where(Series.series_name.ilike(novel_name))
        series_result = session.exec(series_query).first()
        
        if not series_result:
            raise HTTPException(status_code=404, detail="Serial novel not found in RDS.")
        
        # 3. Content 테이블에서 해당 series_id의 회차 정보 가져오기
        episodes_query = (
            select(Content.episode_id, Content.episode_title)
            .where(Content.series_id == series_result)
            .order_by(Content.episode_id)
        )
        episodes_result = session.exec(episodes_query).all()
        
        # 회차 정보 배열 생성
        episodes = [
            {
                "episode_id": episode.episode_id,
                "episode_title": episode.episode_title,
            }
            for episode in episodes_result
        ]
        
        # metadata에 episodes 배열 추가
        metadata["episodes"] = episodes
        
        # JSONResponse로 반환
        return JSONResponse(content=metadata)
    
    except ClientError:
        return JSONResponse(content={"detail": "Metadata not found in S3."}, status_code=404)
    except HTTPException as e:
        return JSONResponse(content={"detail": e.detail}, status_code=404)