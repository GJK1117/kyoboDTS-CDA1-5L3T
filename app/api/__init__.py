from fastapi import APIRouter
from app.api.general_book_read import router as gbr_router
from app.api.general_book_search import router as gbs_router
from app.api.serial_novel_read import router as snr_router
from app.api.serial_novel_search import router as sns_router

api_router = APIRouter()
api_router.include_router(gbr_router, prefix="/general_book", tags=["general_book"])
api_router.include_router(gbs_router, prefix="/general_book", tags=["general_book"])
api_router.include_router(snr_router, prefix="/serial_novel", tags=["serial_novel"])
api_router.include_router(sns_router, prefix="/serial_novel", tags=["serial_novel"])