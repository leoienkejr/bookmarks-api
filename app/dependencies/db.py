from ..db.db import SessionLocal


def get_session():
    '''
    Database session generator
    '''

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
