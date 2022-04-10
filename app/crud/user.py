'''
Functions for performing database operations related
to the "User" entity.
'''

from typing import Callable
from ..models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, email: str, password: str, hash_func: Callable[[str], str]) -> User:
    '''
    Create a new user
    '''

    new_user = User(email=email, hashed_password=hash_func(password))
    db.add(new_user)
    await db.flush()

    return new_user
