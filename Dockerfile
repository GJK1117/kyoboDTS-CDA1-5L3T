# 베이스 이미지로 Python 3.11-slim 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요 라이브러리 설치를 위한 requirements.txt 파일 복사
COPY requirements.txt .

# 필요한 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY ./app /app

# Uvicorn을 통해 애플리케이션 실행 (포트 8000)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]