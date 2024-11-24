import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlmodel import SQLModel, create_engine, Session
from app.main import app  # FastAPI app 객체를 가져옵니다
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
        conn.execute(text("TRUNCATE TABLE `Book`;"))
        conn.execute(text("TRUNCATE TABLE `Series`;"))
        
        conn.execute(
            text("INSERT INTO Book (book_name, book_author) VALUES ('Test Book 1', 'Author 1');")
        )
        conn.execute(
            text("INSERT INTO Series (series_name, series_author, upload_day) VALUES ('Test Series 1', 'Author 2', 'Monday');")
        )
        conn.execute(
            text("INSERT INTO Series (series_name, series_author, upload_day) VALUES ('Test Series 2', 'Author 3', 'Tuesday');")
        )
    with test_engine.connect() as conn:
        books = conn.execute(text("SELECT * FROM Book;")).fetchall()
        series = conn.execute(text("SELECT * FROM Series;")).fetchall()
        print("Books:", books)
        print("Series:", series)


def test_search_general_books():
    response = client.get("/books/home/gb")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "book_name" in data[0]
    assert "book_author" in data[0]


def test_search_serial_books_valid_day():
    response = client.get("/books/home/sn/Monday")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "series_name" in data[0]
    assert "series_author" in data[0]
    assert data[0]["upload_day"] == "Monday"


def test_search_serial_books_invalid_day():
    response = client.get("/books/home/sn/Notady")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid day parameter. Use a valid weekday name (e.g., Monday, Tuesday)."


def test_search_serial_books_no_results():
    response = client.get("/books/home/sn/Wednesday")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No more serial books found for the selected day."