"""
Functions for performing database operations related
to the "User" entity.
"""

from typing import Callable
from ..models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """
    Fetch the user with the given email, or return None
    if such user does not exist.
    """

    query = select(User).filter_by(email=email)
    result = await db.execute(query)
    return result.scalars().first()


async def create_user(
    db: AsyncSession, email: str, password: str, hash_func: Callable[[str], str]
) -> User:
    """
    Create a new user
    """

    new_user = User(email=email, hashed_password=hash_func(password))
    db.add(new_user)
    await db.flush()

    return new_user
