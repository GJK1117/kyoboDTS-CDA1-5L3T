from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from app.core.rds_config import get_read_replica_engine
from app.schema.mysql_schema import Generalbook, SerialBook

router = APIRouter()

# 10개씩 일반 도서 검색어의 결과를 보여주는 API
@router.get("/search/gb/{q}/{last_id}", response_model=List[Generalbook])
def search_general_books(
    q: str,
    last_id: Optional[int] = None,  # 마지막 ID를 경로 매개변수로 사용
    session: Session = Depends(get_read_replica_engine)
):
    # Ebook 테이블에서 검색
    query = select(Generalbook).where(Generalbook.title.like(f"%{q}%"))
    if last_id is not None:
        query = query.where(Generalbook.id > last_id)
    query = query.order_by(Generalbook.id.asc()).limit(10)

    results = session.exec(query).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No more General books found.")
    
    return results


# 10개씩 연재 소설 검색어의 결과를 보여주는 API
@router.get("/search/sn/{q}/{last_id}", response_model=List[SerialBook])
def search_serial_books(
    q: str,
    last_id: Optional[int] = None,  # 마지막 ID를 경로 매개변수로 사용
    session: Session = Depends(get_read_replica_engine)
):
    # SerialBook 테이블에서 검색
    query = select(SerialBook).where(SerialBook.title.like(f"%{q}%"))
    if last_id is not None:
        query = query.where(SerialBook.id > last_id)
    query = query.order_by(SerialBook.id.asc()).limit(10)

    results = session.exec(query).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No more serial books found.")
    
    return results