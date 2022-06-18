from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.application_error import ApplicationErrorResponse
from ..crud.user import get_user_by_email
from ..schemas.user import UserCreate
from ..dependencies.get_session import get_session
from ..exceptions.exceptions import InvalidCredentialsError
from ..security.hash import verify_password
from ..security.token import generate_access_token, generate_refresh_token


APPLICATION_ERROR_RESPONSE = {'model': ApplicationErrorResponse}

v1_auth = APIRouter(prefix='/auth')


@v1_auth.post('/', tags=['auth'], status_code=200,
              responses={400: APPLICATION_ERROR_RESPONSE,
                         403: APPLICATION_ERROR_RESPONSE})
async def signin(user: UserCreate, db: AsyncSession = Depends(get_session)):
    """
    Sign the user in.
    Looks for an user with the given email,
    verify the received password against the hashed password and
    return a refresh token if the passwords match.

    Refresh token must then be used to get an access token.
    """
    async with db as db:
        async with db.begin():

            found_user = await get_user_by_email(email=user.email, db=db)

            if found_user is not None and verify_password(user.password, str(found_user.hashed_password)):
                return generate_refresh_token(int(found_user.id))

            else:
                raise InvalidCredentialsError


@v1_auth.get('/token', tags=['auth'], status_code=200,
             responses={400: APPLICATION_ERROR_RESPONSE,
                        403: APPLICATION_ERROR_RESPONSE})
async def get_access_token():
    pass
