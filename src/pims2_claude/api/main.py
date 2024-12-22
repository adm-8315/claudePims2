from fastapi import FastAPI, HTTPException, Depends
from typing import Dict, Any
from ..config import Config
from ..interface import PIMS2Interface

app = FastAPI(title="PIMS2-Claude Integration API")

# Initialize configuration
config = Config()
config.load_config('config.yaml')  # Load from default path

# Initialize interface
interface = PIMS2Interface(config)

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    await interface.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    await interface.close()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze_pims2_data(endpoint: str, params: Dict[str, Any] = None):
    """Analyze PIMS2 data using Claude."""
    try:
        result = await interface.process_pims2_request(endpoint, params)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
