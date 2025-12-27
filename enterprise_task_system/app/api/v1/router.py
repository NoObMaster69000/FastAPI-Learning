# enterprise_task_system/app/api/v1/router.py

from fastapi import APIRouter

from app.api.v1.endpoints import tasks, users, login

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
