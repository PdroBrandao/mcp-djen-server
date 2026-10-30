"""MCP server for the DJEN sample data.

Run from the repository root:

    python -m app.mcp_server

The process speaks MCP over stdio and waits for a client. Logs go to stderr.
Tools call ``app.service`` and therefore return the same in-memory mock data
as the REST API. ``app.adapter.DJENAdapter`` is not used.
"""

import logging

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from app.service import (
    InvalidRequest,
    NotFound,
    get_case_by_number,
    list_courts as list_court_records,
    search_intimations,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

mcp = MCPServer(
    "mcp-djen-server",
    instructions=(
        "Court notification tools backed by in-memory mock data in app/service.py. "
        "The DJEN external API adapter in app/adapter.py is not connected to these tools."
    ),
    version="1.0.0",
)


@mcp.tool()
def get_intimations(
    name: str,
    date_start: str,
    date_end: str,
    oab: str | None = None,
) -> list[dict]:
    """List mock court notifications for a lawyer between two dates.

    Dates use YYYY-MM-DD. ``oab`` is optional. Results come from the in-memory
    sample set, not from the DJEN API.
    """
    try:
        return search_intimations(name, date_start, date_end, oab)
    except InvalidRequest as exc:
        raise ToolError(str(exc)) from exc


@mcp.tool()
def get_case_details(case_number: str) -> dict:
    """Get one mock court notification by case number.

    The lookup uses the in-memory sample set, not the DJEN API.
    """
    try:
        return get_case_by_number(case_number)
    except NotFound as exc:
        raise ToolError(str(exc)) from exc


@mcp.tool()
def list_courts() -> list[dict]:
    """List the court codes included in the mock dataset."""
    return list_court_records()


if __name__ == "__main__":
    logger.info("Starting mcp-djen-server on stdio")
    mcp.run()
