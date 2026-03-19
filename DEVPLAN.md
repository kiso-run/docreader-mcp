# tool-docreader — Development Plan

Document text extraction tool for kiso. Reads PDF, DOCX, XLSX, CSV, and plain text files from the session workspace.

## Architecture

```
stdin (JSON) → run.py → dispatch action → format reader → stdout (text)
```

- **Entry point**: `run.py` reads JSON from stdin, dispatches to action handler
- **Actions**: `read` (default), `info`, `list`
- **Format readers**: `_read_pdf`, `_read_docx`, `_read_xlsx`, `_read_csv`, `_read_text`
- **Security**: path traversal guard (resolved path must be under workspace)
- **Limits**: output truncated at 100K chars

## Capabilities

| Action | Description | Required Args | Output | Status |
|--------|-------------|---------------|--------|--------|
| read | Extract text from file | file_path | Extracted text | Done |
| info | File metadata | file_path | Size, pages/sheets | Done |
| list | List uploads/ files | none | File listing with sizes | Done |

## Dependencies

- `pypdf>=4.0` — PDF text extraction
- `python-docx>=1.1` — DOCX paragraph extraction
- `openpyxl>=3.1` — XLSX sheet/cell reading
- stdlib `csv` — CSV parsing

---

## M1 — Core implementation ✅

Initial implementation of all three actions and five format readers.

- [x] Project structure: kiso.toml, pyproject.toml, run.py, deps.sh, README, LICENSE
- [x] `read` action: PDF (with page ranges), DOCX, XLSX, CSV, plain text
- [x] `info` action: file metadata (size, format, pages/sheets/rows)
- [x] `list` action: enumerate uploads/ directory
- [x] Path traversal guard
- [x] Output truncation (100K chars)
- [x] Unknown extension heuristic (85% printable ASCII)

## M2 — Unit tests

- [ ] Test `do_read` for each format: PDF, DOCX, XLSX, CSV, plain text
- [ ] Test `do_read` with page ranges for PDF
- [ ] Test `do_info` for each format
- [ ] Test `do_list` with files and empty directory
- [ ] Test path traversal guard (rejected)
- [ ] Test output truncation on large file
- [ ] Test unknown extension heuristic
- [ ] Test missing file_path error
- [ ] Test unsupported format error

## M3 — Integration with kiso registry

- [ ] Add docreader to the kiso plugin registry (kiso-run org)
- [ ] Verify `kiso tool install docreader` works end-to-end
- [ ] Verify `kiso tool test docreader` passes

## M4 — Advanced features (deferred)

- [ ] Table extraction from PDF (structured tables, not just text)
- [ ] Image extraction from DOCX/PDF (save to pub/)
- [ ] OCR fallback for scanned PDFs (tesseract)
- [ ] Password-protected PDF/DOCX support

---

## Known Issues

- pypdf text extraction quality varies by PDF — scanned PDFs produce empty text (no OCR)
- XLSX read_only mode may not evaluate formulas (data_only=True helps but not always)
