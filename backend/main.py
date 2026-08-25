from fastapi import FastAPI

from database import engine
from models import Base
from api.alerts import router as alerts_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Driven SOC Assistant API",
    version="0.4.0"
)


@app.get("/")
def root():
    return {
        "message": "AI-Driven SOC Assistant Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


app.include_router(alerts_router)