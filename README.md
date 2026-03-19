# tool-docreader

Document text extraction tool for [kiso](https://github.com/kiso-run/core). Reads PDF, DOCX, XLSX, CSV, and plain text files.

## Installation

```bash
kiso tool install docreader
```

## How it works

1. Files arrive in the session workspace — typically via connector uploads (`uploads/`), exec tasks (`curl`), or user-placed files.
2. The planner emits a `tool` task with `tool=docreader` and the file path.
3. The tool extracts text content and returns it as stdout.
4. The planner/messenger can then use the extracted text to answer questions or perform analysis.

## Actions

| Action | Description |
|--------|-------------|
| `read` | Extract full text content from a file (default action) |
| `info` | Get file metadata (size, pages, sheets) without full extraction |
| `list` | List files in the `uploads/` directory |

## Args

| Arg | Type | Required | Description |
|-----|------|----------|-------------|
| `action` | string | no | One of: read (default), info, list |
| `file_path` | string | for read/info | Path relative to workspace (e.g. `uploads/report.pdf`) |
| `pages` | string | no | Page range for PDF files (e.g. `1-5`, `3,7,10-12`) |

## Supported formats

| Format | Extension | Library | Notes |
|--------|-----------|---------|-------|
| PDF | `.pdf` | pypdf | Page-level extraction, supports page ranges |
| Word | `.docx` | python-docx | Paragraph-level extraction |
| Excel | `.xlsx` | openpyxl | All sheets, tab-separated values |
| CSV | `.csv` | stdlib csv | Tab-separated output |
| Plain text | `.txt`, `.md`, `.json`, `.py`, etc. | stdlib | Read as-is |

Unknown extensions are tested with a heuristic (85% printable ASCII in first 512 bytes).

## Examples

```
# Read a PDF
action="read" file_path="uploads/report.pdf"

# Read specific pages
action="read" file_path="uploads/report.pdf" pages="1-5"

# Get file metadata
action="info" file_path="uploads/report.pdf"

# List uploaded files
action="list"
```

Output is truncated at 100,000 characters to prevent memory exhaustion on large files.

## License

MIT
