from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import router
from backend.app.database import Base, engine
from backend.app.models import ActivityModel, ProjectModel


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EVM Project Management API",
    version="0.1.0",
    docs_url="/api-docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)