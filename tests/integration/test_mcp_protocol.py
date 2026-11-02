"""Protocol checks through the official MCP client.

Tools are discovered and invoked with ``Client``. These tests do not call the
Python tool functions directly.
"""

import asyncio

from mcp import Client

from app.mcp_server import mcp


def _payload(result):
    data = result.structured_content
    if isinstance(data, dict) and set(data) == {"result"}:
        return data["result"]
    return data


def _call(action):
    async def _run():
        async with Client(mcp) as client:
            return await action(client)

    return asyncio.run(_run())


def test_discovers_tools():
    async def action(client):
        listed = await client.list_tools()
        return sorted(tool.name for tool in listed.tools)

    assert _call(action) == ["get_case_details", "get_intimations", "list_courts"]


def test_list_courts_via_client():
    async def action(client):
        result = await client.call_tool("list_courts", {})
        assert result.is_error is False
        return _payload(result)

    rows = _call(action)
    assert isinstance(rows, list)
    assert len(rows) == 4


def test_get_intimations_via_client():
    async def action(client):
        result = await client.call_tool(
            "get_intimations",
            {
                "name": "PEDRO BRANDÃO",
                "date_start": "2025-08-06",
                "date_end": "2025-08-06",
            },
        )
        assert result.is_error is False
        return _payload(result)

    rows = _call(action)
    assert isinstance(rows, list)
    assert len(rows) == 3
