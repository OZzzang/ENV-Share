from fastapi import FastAPI

from app.config import settings
from app.routers.vaults import router as vaults_router

app = FastAPI(title=settings.app_name)
app.include_router(vaults_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
