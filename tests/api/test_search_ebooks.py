import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlmodel import SQLModel, create_engine, Session
from app.main import app  # FastAPI app 객체
from app.schema.mysql_schema import Book, Series
from app.core.rds_config import get_read_replica_engine

# 테스트용 데이터베이스 설정
test_engine = create_engine("mysql+pymysql://user:1234@localhost:3306/testdb", echo=True)

# 테스트용 세션 의존성 오버라이드
def get_test_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_read_replica_engine] = get_test_session

# 테스트 클라이언트 생성
client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    SQLModel.metadata.create_all(test_engine)
    with test_engine.begin() as conn:
        # 기존 데이터 초기화
        conn.execute(text("TRUNCATE TABLE `Book`;"))
        conn.execute(text("TRUNCATE TABLE `Series`;"))
        
        # 테스트 데이터 추가
        conn.execute(
            text("INSERT INTO Book (book_name, book_author) VALUES "
                 "('Test Book 1', 'Author 1'), ('Another Book', 'Author 2');")
        )
        conn.execute(
            text("INSERT INTO Series (series_name, series_author, upload_day) VALUES "
                 "('Series One', 'Author A', 'Monday'), ('Second Series', 'Author B', 'Tuesday');")
        )
    with test_engine.connect() as conn:
        books = conn.execute(text("SELECT * FROM Book;")).fetchall()
        series = conn.execute(text("SELECT * FROM Series;")).fetchall()
        print("Books:", books)
        print("Series:", series)

# 일반 도서 이름 검색 테스트
def test_search_general_books():
    response = client.get("/books/search/gb/Test")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["book_name"] == "Test Book 1"

# 연재 소설 이름 검색 테스트
def test_search_serial_books():
    response = client.get("/books/search/sn/Series")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "Series" in data[0]["series_name"]

# 일반 도서 검색 시 더 이상 도서가 없을 경우 에러 발생 테스트
def test_search_general_books_no_results():
    response = client.get("/books/search/gb/Nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "더 이상의 일반 도서를 찾을 수 없습니다."

# 연재 소설 검색 시 더 이상 도서가 없을 경우 에러 발생 테스트
def test_search_serial_books_no_results():
    response = client.get("/books/search/sn/Nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "더 이상의 시리즈 도서를 찾을 수 없습니다."