from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from . import models
from .config import Settings, get_settings
from .db.db import engine
from .routers.api import api
from .exceptions.exceptions import ApplicationError


settings: Settings = get_settings()

app = FastAPI(title=settings.app_name,
              description='A RESTful bookmarks API.',
              version='0.1.0')

app.include_router(api)


@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        if settings.drop_all_tables_on_startup:
            await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


@app.exception_handler(ApplicationError)
def application_error_handler(req: Request, exc: ApplicationError):
    return JSONResponse(content=exc.__dict__, status_code=exc.http_status)
