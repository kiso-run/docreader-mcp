# kiso-docreader-mcp

Document text extraction exposed as a
[Model Context Protocol](https://modelcontextprotocol.io) server.
Reads PDF, DOCX, XLSX, CSV, **PPTX, HTML, Markdown, RTF, ODT, EPUB**,
and plain text files.

Pure-Python — **no API key required, zero network egress**. Ships with
`pypdf`, `python-docx`, `openpyxl`, `python-pptx`, `beautifulsoup4`,
`html2text`, `striprtf`, `odfpy`, and `ebooklib`.

Part of the [`kiso-run`](https://github.com/kiso-run) project.

## Install

```sh
uvx --from git+https://github.com/kiso-run/docreader-mcp@v0.2.0 kiso-docreader-mcp
```

## MCP client config

```json
{
  "mcpServers": {
    "docreader": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/kiso-run/docreader-mcp@v0.2.0",
        "kiso-docreader-mcp"
      ]
    }
  }
}
```

No environment variables required.

## Tools

### `read_document(file_path, pages?)`

Extract text from a document. `pages` selects a range in PDFs only
(e.g. `"1-5"`, `"3,7,10-12"`).

Returns a dict always containing `success`, `text`, `format`,
`truncated`, `stderr`; plus format-specific fields:

- **PDF** — `total_pages`, `pages_returned`
- **DOCX** / **text** / **RTF** / **ODT** — `total_chars`, `shown_chars`
- **XLSX** — `sheets`
- **CSV** — `total_rows`, `shown_rows`, `columns`
- **PPTX** — `total_slides`, `slides_returned` (includes speaker notes)
- **HTML** — `total_chars`, `shown_chars` (output is Markdown)
- **EPUB** — `chapters_returned`

Output is truncated at **50 000 chars** at a semantic boundary
(page, row, paragraph, line). When truncated, the reply exposes
both the served slice and the full size so the caller can page
through.

### `document_info(file_path)`

Metadata-only — size, format, pages (PDF), sheets (XLSX), rows (CSV).

### `list_supported_formats()`

Lists known structured and text extensions.

### `doctor()`

`{healthy, issues}` — verifies that `pypdf`, `docx`, and `openpyxl`
are importable.

## Supported formats

**Structured**: `pdf`, `docx`, `xlsx`, `csv`.

**Plain text** (read as-is): `txt`, `md`, `rst`, `log`, `json`,
`yaml`, `yml`, `toml`, `ini`, `cfg`, `conf`, `sh`, `bash`, `py`,
`js`, `ts`, `html`, `htm`, `xml`, `css`, `sql`. Unknown extensions
are probed with a heuristic (first 512 bytes look textual → treat
as text).

## Development

```sh
uv sync
uv run pytest tests/ -q
```

## License

MIT.
