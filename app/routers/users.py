from fastapi import APIRouter

v1_users = APIRouter(prefix='/users')


@v1_users.post('/', tags=['users'])
async def create_new_user():
    pass
