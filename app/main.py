from fastapi import FastAPI
from .routers.api import api
from .config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name,
              description='A RESTful bookmarks API.',
              version='0.1.0')

app.include_router(api)
