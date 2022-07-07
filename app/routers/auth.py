from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.application_error import ApplicationErrorResponse
from ..crud.user import get_user_by_email
from ..schemas.user import UserCreate
from ..dependencies.get_session import get_session
from ..exceptions.exceptions import InvalidCredentialsError
from ..security.hash import verify_password
from ..security.token import (build_token_from_preset_and_serialize,
                              refresh_token_preset, full_jwt_serializer)


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
                token = refresh_token_preset
                token.uid = int(found_user.id)  # type: ignore
                return build_token_from_preset_and_serialize(token, full_jwt_serializer)

            else:
                raise InvalidCredentialsError


@v1_auth.get('/token', tags=['auth'], status_code=200,
             responses={400: APPLICATION_ERROR_RESPONSE,
                        403: APPLICATION_ERROR_RESPONSE})
async def get_access_token():
    pass
