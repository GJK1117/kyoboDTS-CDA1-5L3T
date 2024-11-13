import os
from sqlmodel import create_engine, Session

# RDS 연결 설정 (환경 변수로 RDS 연결 정보 받아오기)
# 환경변수 값이 없는 경우 기본 값 설정(mysql+pymysql://username:password@host/dbname)
READ_REPLICA_DATABASE_URL = os.getenv("READ_REPLICA_DATABASE_URL", "mysql+pymysql://username:password@host/dbname")

# 연결 풀 설정
# 요청마다 연결을 구성하는 것은 시간이 오래 걸릴 것으로 판단, 계속된 연결을 유지하는 연결 풀을 생성
read_replica_engine = create_engine(
    f"mysql+pymysql://{READ_REPLICA_DATABASE_URL}",
    pool_size=10,          # 최대 10개의 연결을 유지
    max_overflow=20,       # 최대 풀 크기 초과 시 20개의 추가 연결 허용
    pool_timeout=30,       # 풀에 연결이 없을 때 최대 대기 시간(초)
    pool_recycle=1800      # 연결을 30분마다 새로 고침하여 끊어짐 방지
)

# 요청마다 세션 생성 종속성
def get_read_replica_engine():
    with Session(read_replica_engine) as session:
        yield session
        
# 어드민용 Primary RDS 연결
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://username:password@host/dbname")

engine = create_engine(
    f"mysql+pymysql://{DATABASE_URL}",
    pool_size=10,          # 최대 10개의 연결을 유지
    max_overflow=20,       # 최대 풀 크기 초과 시 20개의 추가 연결 허용
    pool_timeout=30,       # 풀에 연결이 없을 때 최대 대기 시간(초)
    pool_recycle=1800      # 연결을 30분마다 새로 고침하여 끊어짐 방지
)