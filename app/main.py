from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import httpx
import json
from datetime import datetime, date
import time
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

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

# Mock data based on real DJEN API structure
MOCK_INTIMATIONS = [
    {
        "date": "2025-08-06",
        "court": "TJMG",
        "lawyer_name": "PEDRO BRANDÃO",
        "oab": "123456/MG",
        "case_number": "1234567-89.2024.8.13.0001",
        "type": "TOMAR_CIÊNCIA",
        "summary": "Intimação para ciência de despacho proferido em 05/08/2025",
        "url": "https://www.tjmg.jus.br/djen/123",
        "deadline": "15 days",
        "actions": ["MANIFESTAR_SE", "CALCULAR_PRAZO"]
    },
    {
        "date": "2025-08-06",
        "court": "TJMG",
        "lawyer_name": "PEDRO BRANDÃO",
        "oab": "123456/MG",
        "case_number": "1234567-89.2024.8.13.0002",
        "type": "MANIFESTAR_SE",
        "summary": "Intimação para manifestar sobre impugnação de cálculos",
        "url": "https://www.tjmg.jus.br/djen/124",
        "deadline": "5 days",
        "actions": ["MANIFESTAR_SE", "PREPARAR_IMPUGNACAO"]
    },
    {
        "date": "2025-08-06",
        "court": "TJMG",
        "lawyer_name": "PEDRO BRANDÃO",
        "oab": "123456/MG",
        "case_number": "1234567-89.2024.8.13.0003",
        "type": "CITAR",
        "summary": "Citação para audiência de conciliação",
        "url": "https://www.tjmg.jus.br/djen/125",
        "deadline": "10 days",
        "actions": ["PREPARAR_DOCUMENTOS", "AGENDAR_AUDIENCIA"]
    }
]

DJEN_API_BASE_URL = "https://comunicaapi.pje.jus.br/api/v1/comunicacao"

@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "MCP DJEN Server - Brazilian Court Notifications for LLMs",
        "version": "1.0.0",
        "endpoints": {
            "intimations": "/intimations",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
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
        # Validate date format
        try:
            datetime.strptime(date_start, "%Y-%m-%d")
            datetime.strptime(date_end, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use YYYY-MM-DD"
            )
        
        # Simulate API processing time
        time.sleep(0.5)
        
        # Filter mock data based on parameters
        filtered_data = MOCK_INTIMATIONS.copy()
        
        # Filter by date range
        filtered_data = [
            item for item in filtered_data 
            if date_start <= item["date"] <= date_end
        ]
        
        # Filter by lawyer name (case insensitive)
        if name:
            filtered_data = [
                item for item in filtered_data 
                if name.upper() in item["lawyer_name"].upper()
            ]
        
        # Filter by OAB if provided
        if oab:
            filtered_data = [
                item for item in filtered_data 
                if oab.upper() in item["oab"].upper()
            ]
        
        return filtered_data
        
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
        # Find case in mock data
        case = next(
            (item for item in MOCK_INTIMATIONS if item["case_number"] == case_number),
            None
        )
        
        if not case:
            raise HTTPException(
                status_code=404,
                detail=f"Case {case_number} not found"
            )
        
        return case
        
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
    courts = [
        {"code": "TJMG", "name": "Tribunal de Justiça de Minas Gerais"},
        {"code": "TJSP", "name": "Tribunal de Justiça de São Paulo"},
        {"code": "TJRJ", "name": "Tribunal de Justiça do Rio de Janeiro"},
        {"code": "TRT3", "name": "Tribunal Regional do Trabalho 3ª Região"}
    ]
    
    return courts

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "NOT_FOUND",
        "message": "Endpoint not found",
        "code": 404
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "INTERNAL_ERROR",
        "message": "Internal server error",
        "code": 500
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 