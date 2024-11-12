from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router

app = FastAPI()
app.include_router(api_router)

# 모든 출처에서의 요청을 허용하기 위한 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 요청 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

# include_in_schema=False 설정 시
# 1. OpenAPI 스키마 생성 시간 단축
# 2. 라우터 정보에 표시되지 않아 보안적 이점
@app.get("/", include_in_schema=False)
async def health():
    return PlainTextResponse(content="ok", status_code=200)