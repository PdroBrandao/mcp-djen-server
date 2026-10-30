from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import httpx
import json
from datetime import datetime, date
import logging
import os

from app.service import InvalidRequest, NotFound, get_case_by_number, list_courts, search_intimations
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log startup information
logger.info("Starting MCP DJEN Server...")
logger.info(f"Environment: PORT={os.getenv('PORT', '8000')}")
logger.info(f"Python version: {os.sys.version}")

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="MCP DJEN Server", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("FastAPI app initialized successfully")

class IntimationResponse(BaseModel):
    date: str
    court: str
    lawyer_name: str
    oab: str
    case_number: str
    type: str
    summary: str
    url: str
    deadline: Optional[str] = None
    actions: List[str] = []

class ErrorResponse(BaseModel):
    error: str
    message: str
    code: int

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
        "status": "success",
        "message": "MCP DJEN Server - Brazilian Court Notifications for LLMs",
        "version": "1.0.0",
        "data_source": "mock",
        "note": "Responses use in-memory sample data. app/adapter.py is not connected to this API.",
        "endpoints": {
            "intimations": "/intimations",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "mcp-djen-server"
    }

@app.get("/intimations", response_model=List[IntimationResponse])
@limiter.limit("100/minute")
async def get_intimations(
    name: str = Query(..., description="Lawyer's full name"),
    oab: Optional[str] = Query(None, description="OAB registration number"),
    date_start: str = Query(..., description="Start date (YYYY-MM-DD)"),
    date_end: str = Query(..., description="End date (YYYY-MM-DD)"),
    request: Request = None
):
    """
    Get court notifications for a lawyer
    
    Args:
        name: Lawyer's full name (required)
        oab: OAB registration number (optional)
        date_start: Start date in YYYY-MM-DD format (required)
        date_end: End date in YYYY-MM-DD format (required)
    
    Returns:
        List of court notifications with structured data
    
    Example:
        GET /intimations?name=ALFREDO+RAMOS&date_start=2025-08-06&date_end=2025-08-06
    """
    try:
        return search_intimations(name, date_start, date_end, oab)
    except InvalidRequest as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

@app.get("/intimations/{case_number}")
@limiter.limit("100/minute")
async def get_case_details(case_number: str, request: Request = None):
    """
    Get detailed information about a specific case
    
    Args:
        case_number: Process number to search for
    
    Returns:
        Case details if found
    """
    try:
        return get_case_by_number(case_number)
    except NotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

@app.get("/courts")
@limiter.limit("50/minute")
async def get_available_courts(request: Request = None):
    """
    Get list of available courts
    
    Returns:
        List of court codes and names
    """
    return list_courts()

@app.exception_handler(404)
async def not_found_handler(request, exc):
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return JSONResponse(
        status_code=404,
        content={"error": "NOT_FOUND", "message": "Endpoint not found", "code": 404},
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "INTERNAL_ERROR", "message": "Internal server error", "code": 500},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 