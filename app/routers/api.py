from fastapi import APIRouter

api = APIRouter(prefix='/api')
v1 = APIRouter(prefix='/v1')

api.include_router(v1)
