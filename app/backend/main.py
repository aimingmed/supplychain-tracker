import logging

from fastapi import FastAPI

from api.accounts import accounts
from api.productlog import productlog
from db import init_db

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
    application.include_router(productlog.router, prefix="/productlog", tags=["productlog"])

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
