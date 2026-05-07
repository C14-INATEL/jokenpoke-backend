from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.shared.exceptions.domain_exception import DomainException
from app.shared.exceptions.not_found_exception import NotFoundException
from app.shared.exceptions.unauthorized_exception import UnauthorizedException

async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )

async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )

async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=401,
        content={"detail": exc.message},
    )

# Função auxiliar para registrar todos de uma vez
def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(DomainException, domain_exception_handler)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)