from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from app.core.rds_config import get_read_replica_engine
from app.schema.mysql_schema import Ebook, SerialBook

router = APIRouter()

# 검색어를 경로 매개변수로 받아 검색하는 엔드포인트
@router.get("/search/{q}/{type}/{last_id}", response_model=List[Ebook])
def search_books(
    q: str,
    type: int,
    last_id: Optional[int],  # 마지막 ID를 경로 매개변수로 사용
    session: Session = Depends(get_read_replica_engine)
):
    # 쿼리를 저장할 변수 초기화
    query = None

    # type 값에 따라 다른 테이블에서 검색
    if type == 0:
        # Ebook 테이블에서 검색
        query = select(Ebook).where(Ebook.title.like(f"%{q}%"))
        if last_id is not None:
            query = query.where(Ebook.id > last_id)
        query = query.order_by(Ebook.id.asc()).limit(10)
        
    elif type == 1:
        # SerialBook 테이블에서 검색
        query = select(SerialBook).where(SerialBook.title.like(f"%{q}%"))
        if last_id is not None:
            query = query.where(SerialBook.id > last_id)
        query = query.order_by(SerialBook.id.asc()).limit(10)

    # query가 설정되지 않았으면 잘못된 type 값이 전달된 것으로 처리
    if query is None:
        raise HTTPException(status_code=400, detail="Invalid type parameter. Use 0 for Ebook or 1 for Series.")

    # 쿼리 실행
    results = session.exec(query).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No more books found.")
    
    return results