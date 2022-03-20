from fastapi import APIRouter
from .users import v1_users

api = APIRouter(prefix='/api')

v1 = APIRouter(prefix='/v1')
v1.include_router(v1_users)

api.include_router(v1)
