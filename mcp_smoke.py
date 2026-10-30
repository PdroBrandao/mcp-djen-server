#!/usr/bin/env python3
"""Check MCP tool discovery and one successful call, plus a controlled error.

Does not start the REST server and does not call the DJEN API.

    python mcp_smoke.py
"""

import asyncio
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters

ROOT = Path(__file__).resolve().parent
EXPECTED_TOOLS = ["get_case_details", "get_intimations", "list_courts"]


def text_of(result) -> str:
    chunks = []
    for block in result.content or []:
        text = getattr(block, "text", None)
        if text:
            chunks.append(text)
    return "\n".join(chunks)


def payload(result):
    data = result.structured_content
    if isinstance(data, dict) and set(data) == {"result"}:
        return data["result"]
    return data


async def main() -> int:
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.mcp_server"],
        cwd=ROOT,
    )
    async with Client(params) as client:
        listed = await client.list_tools()
        names = sorted(tool.name for tool in listed.tools)
        if names != EXPECTED_TOOLS:
            print(f"FAIL tool list: {names}")
            return 1
        print("tools:", ", ".join(names))

        courts = await client.call_tool("list_courts", {})
        court_rows = payload(courts)
        if courts.is_error or not isinstance(court_rows, list) or len(court_rows) != 4:
            print("FAIL list_courts:", text_of(courts) or court_rows)
            return 1
        print(f"list_courts: {len(court_rows)} courts")

        intimations = await client.call_tool(
            "get_intimations",
            {
                "name": "PEDRO BRANDÃO",
                "date_start": "2025-08-06",
                "date_end": "2025-08-06",
            },
        )
        rows = payload(intimations)
        if intimations.is_error or not isinstance(rows, list) or len(rows) != 3:
            print("FAIL get_intimations:", text_of(intimations) or rows)
            return 1
        print(f"get_intimations: {len(rows)} notifications")

        invalid = await client.call_tool(
            "get_intimations",
            {
                "name": "PEDRO BRANDÃO",
                "date_start": "invalid-date",
                "date_end": "2025-08-06",
            },
        )
        message = text_of(invalid)
        if not invalid.is_error or "Invalid date format" not in message:
            print(f"FAIL invalid date: is_error={invalid.is_error} message={message!r}")
            return 1
        print("invalid date:", message)

    print("OK")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except Exception as exc:
        print(f"FAIL {type(exc).__name__}: {exc}")
        sys.exit(1)
