#!/usr/bin/env python3
"""
Startup script for MCP DJEN Server
Handles PORT environment variable and provides detailed logging
"""

import os
import sys
import logging
from uvicorn import run
from app.main import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Get port from environment or default to 8000
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    
    logger.info(f"Starting MCP DJEN Server on {host}:{port}")
    logger.info(f"Environment variables: PORT={os.getenv('PORT', '8000')}, HOST={host}")
    
    try:
        # Start the server
        run(
            "app.main:app",
            host=host,
            port=port,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 