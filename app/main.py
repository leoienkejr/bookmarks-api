from fastapi import FastAPI
from .routers.api import api

app = FastAPI(title='Bookmarks API',
              description='A RESTful bookmarks API.',
              version='0.1.0')

app.include_router(api)
