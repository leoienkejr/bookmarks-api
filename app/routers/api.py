from fastapi import APIRouter
from .user import v1_users
from .auth import v1_auth

api = APIRouter(prefix='/api')

v1 = APIRouter(prefix='/v1')
v1.include_router(v1_users)
v1.include_router(v1_auth)

api.include_router(v1)
