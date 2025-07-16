import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.accounts import accounts
from api.productlog import productlog
from api.productrequests import productrequests
from db import init_db

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI(
        title="Supply Chain Tracker API",
        description="API for managing supply chain products and inventory",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        root_path="/api"
    )
    
    # Add CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["https://staging-sctracker.aimingmed.local", "http://localhost:3005", "https://localhost", "http://localhost"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    application.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
    application.include_router(
        productlog.router, prefix="/productlog", tags=["productlog"]
    )
    application.include_router(
        productrequests.router, prefix="/productrequests", tags=["productrequests"]
    )

    return application


app = create_application()


@app.get("/")
async def root():
    return {"message": "Supply Chain Tracker API", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/debug/openapi")
async def debug_openapi():
    return app.openapi()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
