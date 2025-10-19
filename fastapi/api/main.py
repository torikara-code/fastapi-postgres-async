from fastapi import APIRouter
from api.routers.hello import router as hello_router


router = APIRouter()

router.include_router(hello_router, prefix="/v1")
