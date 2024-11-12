from sqlmodel import Field, SQLModel
from typing import List, Optional

# 모델 정의
class Ebook(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str  # 예시 필드, 실제 테이블 구조에 맞게 수정 필요

class SerialBook(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str  # 예시 필드, 실제 테이블 구조에 맞게 수정 필요