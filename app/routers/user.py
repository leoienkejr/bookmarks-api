from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies.get_session import get_session
from ..security.hash import hash_password
from ..crud.user import create_user, get_user_by_email
from ..schemas.user import UserCreate, UserRead
from ..schemas.application_error import ApplicationErrorResponse
from ..exceptions.exceptions import EmailAlreadyInUseError

v1_user = APIRouter(prefix='/users')


@v1_user.post('/', tags=['users'], response_model=UserRead, status_code=201,
              responses={400: {'model': ApplicationErrorResponse}})
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    async with db as db:
        async with db.begin():
            existing_user = await get_user_by_email(db=db, email=user.email)

            if existing_user is not None:
                raise EmailAlreadyInUseError

            user = await create_user(db=db, email=user.email, password=user.password, hash_func=hash_password)
            return user
