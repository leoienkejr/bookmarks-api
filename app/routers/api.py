from fastapi import APIRouter
from .user import v1_user

api = APIRouter(prefix='/api')

v1 = APIRouter(prefix='/v1')
v1.include_router(v1_user)

api.include_router(v1)
