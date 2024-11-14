from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel import select, Session
from app.core.rds_config import get_read_replica_engine
from app.schema.mysql_schema import Book, Series

router = APIRouter()

@router.get("/search/gb/{q}/{last_id}", response_model=List[Book])
def search_general_books(
    q: str,
    last_id: Optional[int] = None,
    session: Session = Depends(get_read_replica_engine)
):
    query = select(Book).where(Book.title.like(f"%{q}%"))
    if last_id is not None:
        query = query.where(Book.id > last_id)
    query = query.order_by(Book.id.asc()).limit(10)

    results = session.exec(query).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No more serial books found.")
    
    return JSONResponse(content=results)

@router.get("/search/sn/{q}/{last_id}", response_model=List[Series])
def search_serial_books(
    q: str,
    last_id: Optional[int] = None,
    session: Session = Depends(get_read_replica_engine)
):
    query = select(Series).where(Series.title.like(f"%{q}%"))
    if last_id is not None:
        query = query.where(Series.id > last_id)
    query = query.order_by(Series.id.asc()).limit(10)

    results = session.exec(query).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No more serial books found.")
    
    return JSONResponse(content=results)