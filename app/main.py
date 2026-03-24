from fastapi import FastAPI
from app.interfaces.api.router import router

app = FastAPI(title="Jokenpoke API")

app.include_router(router)