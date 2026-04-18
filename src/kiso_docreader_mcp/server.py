"""MCP server exposing document text extraction as a tool."""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import docreader_runner


mcp = FastMCP("kiso-docreader")


@mcp.tool()
def read_document(file_path: str, pages: str | None = None) -> dict:
    """Extract text from a document file (PDF, DOCX, XLSX, CSV, or plain text).

    Args:
        file_path: Path to the document file.
        pages: Optional PDF page selector (e.g. ``"1-5"``, ``"3,7,10-12"``).
            Ignored for non-PDF formats.

    Returns:
        A dict always containing ``success``, ``text``, ``format``,
        ``truncated``, and ``stderr``; plus format-specific extras:

        - PDF: ``total_pages``, ``pages_returned``
        - DOCX / plain text: ``total_chars``, ``shown_chars``
        - XLSX: ``sheets``
        - CSV: ``total_rows``, ``shown_rows``, ``columns``

        Output is truncated at 50 000 characters at a semantic boundary
        (page, row, paragraph, line) with ``truncated: true`` on the
        return payload.
    """
    return docreader_runner.read_document(file_path=file_path, pages=pages)


@mcp.tool()
def document_info(file_path: str) -> dict:
    """Return document metadata without extracting full text.

    Args:
        file_path: Path to the document.

    Returns:
        ``{"success": bool, "file_name": str | None, "size_bytes": int | None,
           "format": str | None, "pages": int | None,
           "sheets": [str] | None, "rows": int | None, "stderr": str}``.
    """
    return docreader_runner.document_info(file_path=file_path)


@mcp.tool()
def list_supported_formats() -> dict:
    """Return the set of file extensions this server can parse.

    Returns:
        ``{"structured": [ext, ...], "text": [ext, ...], "notes": str}``.
    """
    return docreader_runner.list_supported_formats()


@mcp.tool()
def doctor() -> dict:
    """Verify the Python parsing libraries are importable.

    Returns ``{"healthy": bool, "issues": [str]}``.
    """
    return docreader_runner.check_health()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
