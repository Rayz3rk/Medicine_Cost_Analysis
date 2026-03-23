import sys
import os

# Add the project root to sys.path so that 'backend.x' imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router as api_router
from backend.api.reports import router as reports_router
from backend.agents.runner import start_all_agents

app = FastAPI(
    title="Multi-Agent Cost Analysis System",
    description="Backend API for orchestrating multi-agent cost and pricing analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Start agent listener threads in the background
    start_all_agents()
    print("Application startup complete.")

@app.get("/")
def read_root():
    return {"message": "Multi-Agent Backend is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
