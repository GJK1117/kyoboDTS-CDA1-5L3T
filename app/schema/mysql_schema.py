from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from enum import Enum

# 요일을 정의하는 Enum 클래스
class DayOfWeek(str, Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"

# Book 테이블에 대응하는 모델
class Book(SQLModel, table=True):
    __tablename__ = "Book"  # 테이블 이름을 명시적으로 지정
    book_id: Optional[int] = Field(default=None, primary_key=True)
    book_name: str
    book_author: Optional[str] = None
    thumbnail: Optional[str] = None  # 필요에 따라 추가

# Series 테이블에 대응하는 모델
class Series(SQLModel, table=True):
    __tablename__ = "Series"  # 테이블 이름을 명시적으로 지정
    series_id: Optional[int] = Field(default=None, primary_key=True)
    series_name: str
    series_author: Optional[str] = None
    upload_day: DayOfWeek
    thumbnail: Optional[str] = None  # 필요에 따라 추가