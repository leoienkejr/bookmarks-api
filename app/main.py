from fastapi import FastAPI
from routers.api import api

app = FastAPI()
app.include_router(api)
