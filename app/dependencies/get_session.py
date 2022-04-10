from ..db.db import SessionLocal


async def get_session():
    '''
    Database session generator
    '''

    session = SessionLocal()

    try:
        yield session
    finally:
        await session.close()
