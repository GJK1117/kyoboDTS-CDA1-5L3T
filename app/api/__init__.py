from fastapi import APIRouter
from app.api.general_book_read import router as gbr_router
from app.api.general_book_search import router as gbs_router
from app.api.serial_novel_read import router as snr_router
from app.api.serial_novel_search import router as sns_router
from app.api.search_ebooks import router as sb_router
from app.api.list_ebook import router as home_router

api_router = APIRouter()

api_router.include_router(gbr_router, prefix="/general_book", tags=["general_book"])
api_router.include_router(gbs_router, prefix="/general_book", tags=["general_book"])
api_router.include_router(snr_router, prefix="/serial_novel", tags=["serial_novel"])
api_router.include_router(sns_router, prefix="/serial_novel", tags=["serial_novel"])
api_router.include_router(sb_router, prefix="/books", tags=["allbooks"])
api_router.include_router(home_router, prefix="/books", tags=["allbooks"])