from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from app.core.rds_config import get_read_replica_engine
from app.schema.mysql_schema import Book, Series

router = APIRouter()

@router.get("/search/gb/{q}", response_model=List[Book])
def search_general_books(
    q: str,
    last_id: int = 0,
    session: Session = Depends(get_read_replica_engine)
):
    query = select(Book).where(Book.book_name.like(f"%{q}%"))
    if last_id is not None:
        query = query.where(Book.book_id > last_id)
    query = query.order_by(Book.book_id.asc()).limit(10)

    results = session.exec(query).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="더 이상의 일반 도서를 찾을 수 없습니다.")
    
    return results

@router.get("/search/sn/{q}", response_model=List[Series])
def search_serial_books(
    q: str,
    last_id: int = 0,
    session: Session = Depends(get_read_replica_engine)
):
    query = select(Series).where(Series.series_name.like(f"%{q}%"))
    if last_id is not None:
        query = query.where(Series.series_id > last_id)
    query = query.order_by(Series.series_id.asc()).limit(10)

    results = session.exec(query).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="더 이상의 시리즈 도서를 찾을 수 없습니다.")
    
    return results