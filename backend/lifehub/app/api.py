import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from lifehub.config.checks import pre_run_checks
from lifehub.config.constants import UVICORN_HOST
from lifehub.config.util.schemas import *  # noqa: F401,F403
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.module.api.router import router as modules_router
from lifehub.core.provider.api.router import router as providers_router
from lifehub.core.user.api.router import router as user_router
from lifehub.core.user.api.user_modules.router import router as user_modules_router
from lifehub.core.user.api.user_providers.router import router as user_providers_router
from lifehub.modules.calendar.router import router as calendar_router
from lifehub.modules.finance.router import router as finance_router

#### Config ####
app = FastAPI(
    title="LifeHub API",
    description="API for LifeHub",
    version="0.1.0",
    openapi_url="/api/v0/openapi.json",
    docs_url="/api/v0/docs",
    redoc_url="/api/v0/redoc",
)

#### CORS ####
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#### Routers ####
api = APIRouter()
api.include_router(user_router, prefix="/user", tags=["user"])
api.include_router(
    user_providers_router, prefix="/user/providers", tags=["user/providers"]
)
api.include_router(user_modules_router, prefix="/user/modules", tags=["user/modules"])
api.include_router(providers_router, prefix="/providers", tags=["providers"])
api.include_router(modules_router, prefix="/modules", tags=["modules"])
api.include_router(finance_router, prefix="/finance", tags=["finance"])
api.include_router(calendar_router, prefix="/calendar", tags=["calendar"])

# TODO: Eventually replace this with a reverse proxy
app.include_router(api, prefix="/api/v0")


#### Exception Handlers ####
@app.exception_handler(ServiceException)
async def service_exception_handler(
    request: Request, exc: ServiceException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


def run() -> None:
    pre_run_checks()
    uvicorn.run("lifehub.app.api:app", host=UVICORN_HOST, port=8000, reload=True)


if __name__ == "__main__":
    run()
