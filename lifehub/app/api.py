from os import getenv

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import lifehub.app.util.load  # noqa: F401
from lifehub.app.util.schemas import *  # noqa: F401,F403
from lifehub.core.module.api.router import router as modules_router
from lifehub.core.provider.api.router import router as providers_router

# from lifehub.core.user.modules.router import router as user_modules_router
# from lifehub.core.user.providers.router import router as user_providers_router
from lifehub.core.user.api.router import router as user_router

# from lifehub.modules.finance.router import router as finance_router
# from lifehub.modules.server.router import router as server_router

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
    "http://localhost:5173",
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
# api.include_router(
#     user_providers_router, prefix="/user/providers", tags=["user/providers"]
# )
# api.include_router(user_modules_router, prefix="/user/modules", tags=["user/modules"])
api.include_router(providers_router, prefix="/providers", tags=["providers"])
api.include_router(modules_router, prefix="/modules", tags=["modules"])
# api.include_router(finance_router, prefix="/finance", tags=["finance"])
# api.include_router(server_router, prefix="/server", tags=["server"])

# TODO: Eventually replace this with a reverse proxy
app.include_router(api, prefix="/api/v0")


def run():
    host = getenv("UVICORN_HOST", "localhost")
    uvicorn.run("lifehub.app.api:app", host=host, port=8000, reload=True)


if __name__ == "__main__":
    run()
