from fastapi import FastAPI
from app.api.twin import router as twin_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DigitalTwin.ai API",
    description="Predictive Digital Twin for Vehicle Assembly Lines",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(twin_router)


@app.get("/")
def root():
    return {
        "message": "DigitalTwin.ai API is running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "digitaltwin-api",
    }
