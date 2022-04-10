from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies.get_session import get_session
from ..security.hash import hash_password
from ..crud.user import create_user
from ..schemas.user import UserCreate, UserRead

v1_user = APIRouter(prefix='/users')


@v1_user.post('/', tags=['users'], response_model=UserRead)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    async with db as db:
        async with db.begin():
            user = await create_user(db=db, email=user.email, password=user.password, hash_func=hash_password)
            return user
