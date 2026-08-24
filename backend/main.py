from fastapi import FastAPI

app = FastAPI(
    title="AI-Driven SOC Assistant API",
    version="0.1.0"
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