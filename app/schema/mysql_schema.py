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
    # book_thumbnail: Optional[str] = None  # 필요에 따라 추가

# Series 테이블에 대응하는 모델
class Series(SQLModel, table=True):
    __tablename__ = "Series"  # 테이블 이름을 명시적으로 지정
    series_id: Optional[int] = Field(default=None, primary_key=True)
    series_name: str
    series_author: Optional[str] = None
    upload_day: DayOfWeek
    # book_thumbnail: Optional[str] = None  # 필요에 따라 추가
    contents: List["Content"] = Relationship(back_populates="series")  # Content와의 관계 설정

# Content 테이블에 대응하는 모델 (복합 기본 키 사용)
class Content(SQLModel, table=True):
    __tablename__ = "Content"  # 테이블 이름을 명시적으로 지정
    series_id: int = Field(foreign_key="Series.series_id", primary_key=True)
    episode_id: int = Field(primary_key=True)
    episode_title: str
    series: Optional[Series] = Relationship(back_populates="contents")