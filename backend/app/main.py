from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.events import router as events_router
from app.routes.alerts import router as alerts_router
from app.routes.ingestion import router as ingestion_router
from app.routes.dashboard import router as dashboard_router
from app.routes.rag import router as rag_router
from app.routes.assistant import router as assistant_router
from app.routes.incidents import router as incidents_router
app = FastAPI(
    title="AI X Cyber",
    description="AI X Cyber is a platform that leverages artificial intelligence to enhance cybersecurity measures. It provides tools and services for threat detection, vulnerability assessment, and incident response.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(events_router)
app.include_router(alerts_router)
app.include_router(ingestion_router)
app.include_router(dashboard_router)
app.include_router(rag_router)
app.include_router(assistant_router)
app.include_router(incidents_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to AI X Cyber!",
        "status": "running",
        }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }