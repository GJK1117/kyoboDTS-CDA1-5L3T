# 베이스 이미지로 Python 3.11-slim 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 소스 코드 복사 - 로컬의 app 폴더를 /app 디렉토리로 복사
COPY . /app

# 필요한 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# Uvicorn을 통해 애플리케이션 실행 (포트 8000)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]