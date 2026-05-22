from fastapi import FastAPI

from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine
from app.interfaces.api.exception_handlers import register_exception_handlers
from app.interfaces.api.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Jokenpoke API")

register_exception_handlers(app)

app.include_router(router)

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}