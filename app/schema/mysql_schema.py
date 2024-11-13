from sqlmodel import Field, SQLModel
from typing import List, Optional
from enum import Enum

# 모델 정의
class Generalbook(SQLModel, table=True):
    book_id: Optional[int] = Field(default=None, primary_key=True)  # 기본 키로 book_id 사용
    book_name: str  # 책 제목
    book_author: Optional[str] = None  # 작가 이름
    book_thumbnail: str # 썸네일이 저장된 s3 주소

# 요일을 정의하는 Enum 클래스
class DayOfWeek(str, Enum):
    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"
    saturday = "Saturday"
    sunday = "Sunday"

class SerialBook(SQLModel, table=True):
    series_id: Optional[int] = Field(default=None, primary_key=True)  # 기본 키로 series_id 사용
    series_name: str  # 소설 제목
    series_author: Optional[str] = None  # 작가 이름
    series_thumbnail: str  # 썸네일 이미지의 S3 URL 주소
    upload_day: DayOfWeek  # 요일 (ENUM 필드에 맞게 Enum 사용)