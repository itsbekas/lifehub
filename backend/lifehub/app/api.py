import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from lifehub.config.checks import pre_run_setup
from lifehub.config.constants import cfg
from lifehub.core.admin.router import router as admin_router
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.provider.api.router import router as providers_router
from lifehub.core.user.api.router import router as user_router
from lifehub.core.user.api.user_providers.router import router as user_providers_router
from lifehub.modules.finance.router import router as finance_router
from lifehub.modules.routine.router import router as routine_router

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
    "http://localhost:3000",  # Frontend development server
    "http://127.0.0.1:3000",  # Alternative localhost address
    cfg.FRONTEND_URL,  # Production frontend URL from config
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
api.include_router(admin_router, prefix="/admin", tags=["admin"])
api.include_router(providers_router, prefix="/providers", tags=["providers"])
api.include_router(finance_router, prefix="/finance", tags=["finance"])
api.include_router(routine_router, prefix="/routine", tags=["routine"])

# TODO: Eventually replace this with a reverse proxy
app.include_router(api, prefix="/api/v0")


#### Exception Handlers ####
@app.exception_handler(ServiceException)
async def service_exception_handler(
    request: Request, exc: ServiceException
) -> JSONResponse:
    if cfg.ENVIRONMENT == "development":
        print(f"{exc.__class__.__name__}: {exc}")

    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


def run() -> None:
    pre_run_setup()
    uvicorn.run("lifehub.app.api:app", host=cfg.UVICORN_HOST, port=8000, reload=True)


if __name__ == "__main__":
    run()
