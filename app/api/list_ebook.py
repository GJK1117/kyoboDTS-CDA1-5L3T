from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel import select, Session, func
from app.core.rds_config import get_read_replica_engine
from app.schema.mysql_schema import Book, Series

router = APIRouter()

@router.get("/home/gb", response_model=List[Book])
def search_general_books(
    session: Session = Depends(get_read_replica_engine)
):
    query = select(Book).order_by(func.rand()).limit(20)
    results = session.exec(query).all()
    
    if not results:
        return JSONResponse(status_code=404, content={"detail": "No more General books found."})
    
    return results

@router.get("/home/sn/{day}", response_model=List[Series])
def search_serial_books(
    day: str,
    session: Session = Depends(get_read_replica_engine)
):
    valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
    if day not in valid_days:
        return JSONResponse(status_code=400, content={"detail": "Invalid day parameter. Use a valid weekday name (e.g., Monday, Tuesday)."})
    
    query = select(Series).where(Series.upload_day == day).limit(20)
    results = session.exec(query).all()
    
    if not results:
        return JSONResponse(status_code=404, content={"detail": "No more serial books found for the selected day."})
    
    return results