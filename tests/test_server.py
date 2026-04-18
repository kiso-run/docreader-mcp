"""MCP tool-surface tests for kiso_docreader_mcp.server."""
from __future__ import annotations

import json
from unittest.mock import patch


def _decode(result) -> dict:
    blocks = result if isinstance(result, list) else list(result)
    return json.loads(blocks[0].text)


def test_mcp_instance_named():
    from kiso_docreader_mcp import server
    assert server.mcp.name == "kiso-docreader"


async def test_all_tools_registered():
    from kiso_docreader_mcp import server
    tools = await server.mcp.list_tools()
    names = {t.name for t in tools}
    assert {"read_document", "document_info", "list_supported_formats", "doctor"} <= names


async def test_read_document_delegates():
    from kiso_docreader_mcp import server
    stub = {
        "success": True, "text": "hello", "format": "txt",
        "total_chars": 5, "shown_chars": 5, "truncated": False,
        "stderr": "",
    }
    with patch(
        "kiso_docreader_mcp.server.docreader_runner.read_document",
        return_value=stub,
    ) as run:
        result = await server.mcp.call_tool(
            "read_document", {"file_path": "/tmp/x.txt", "pages": "1-3"},
        )
    run.assert_called_once_with(file_path="/tmp/x.txt", pages="1-3")
    assert _decode(result) == stub


async def test_document_info_delegates():
    from kiso_docreader_mcp import server
    stub = {
        "success": True, "file_name": "x.pdf", "size_bytes": 123,
        "format": "pdf", "pages": 3, "sheets": None, "rows": None,
        "stderr": "",
    }
    with patch(
        "kiso_docreader_mcp.server.docreader_runner.document_info",
        return_value=stub,
    ) as run:
        result = await server.mcp.call_tool(
            "document_info", {"file_path": "/tmp/x.pdf"},
        )
    run.assert_called_once_with(file_path="/tmp/x.pdf")
    assert _decode(result) == stub


async def test_list_supported_formats_delegates():
    from kiso_docreader_mcp import server
    stub = {"structured": [".pdf"], "text": [".txt"], "notes": "..."}
    with patch(
        "kiso_docreader_mcp.server.docreader_runner.list_supported_formats",
        return_value=stub,
    ) as run:
        result = await server.mcp.call_tool("list_supported_formats", {})
    run.assert_called_once_with()
    assert _decode(result) == stub


async def test_doctor_delegates():
    from kiso_docreader_mcp import server
    stub = {"healthy": True, "issues": []}
    with patch(
        "kiso_docreader_mcp.server.docreader_runner.check_health",
        return_value=stub,
    ) as run:
        result = await server.mcp.call_tool("doctor", {})
    run.assert_called_once_with()
    assert _decode(result) == stub


def test_main_calls_run():
    from kiso_docreader_mcp import server
    with patch.object(server.mcp, "run") as run:
        server.main()
    run.assert_called_once()
