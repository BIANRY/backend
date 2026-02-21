from fastapi import APIRouter

from app.api.v1.endpoints import users, boards, grass

api_router = APIRouter()

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    boards.router,
    prefix="/boards",
    tags=["boards"]
)

api_router.include_router(
    grass.router,
    prefix="/grass",
    tags=["grass"]
)