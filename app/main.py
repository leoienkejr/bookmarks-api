from fastapi import FastAPI

from . import models
from .config import Settings, get_settings
from .db.db import engine
from .routers.api import api


settings: Settings = get_settings()

app = FastAPI(title=settings.app_name,
              description='A RESTful bookmarks API.',
              version='0.1.0')

app.include_router(api)


@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
