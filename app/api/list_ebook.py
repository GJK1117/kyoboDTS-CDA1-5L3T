from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session, func
from app.core.rds_config import get_read_replica_engine
from app.schema.mysql_schema import Generalbook, SerialBook

router = APIRouter()

# 요일별로 일반 도서 검색어의 결과를 20개씩 보여주는 API
@router.get("/home/gb", response_model=List[Generalbook])
def search_general_books(
    session: Session = Depends(get_read_replica_engine)
):
    # Generalbook 테이블에서 랜덤하게 20개 검색
    query = select(Generalbook).order_by(func.rand()).limit(20)
    
    results = session.exec(query).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No more General books found.")
    
    return results


# 요일별로 연재 소설 검색어의 결과를 20개씩 보여주는 API
@router.get("/home/sn/{day}", response_model=List[SerialBook])
def search_serial_books(
    day: str,  # 요일 이름을 문자열로 받음 (Monday, Tuesday, ...)
    session: Session = Depends(get_read_replica_engine)
):
    # 유효한 요일 문자열을 리스트로 정의
    valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
    
    # 입력된 day가 유효한 요일인지 확인
    if day not in valid_days:
        raise HTTPException(status_code=400, detail="Invalid day parameter. Use a valid weekday name (e.g., Monday, Tuesday).")
    
    # 선택한 요일에 따라 SerialBook 테이블에서 검색
    query = select(SerialBook).where(SerialBook.upload_day == day).limit(20)
    
    results = session.exec(query).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No more serial books found for the selected day.")
    
    return results