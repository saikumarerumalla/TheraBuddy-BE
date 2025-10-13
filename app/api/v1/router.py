from fastapi import APIRouter
from app.api.v1 import auth, chat, mood, users, exercises, resources, analytics

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(chat.router)
api_router.include_router(mood.router)
api_router.include_router(exercises.router)
api_router.include_router(resources.router)
api_router.include_router(analytics.router)
