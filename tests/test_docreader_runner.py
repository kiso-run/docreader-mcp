"""Unit tests for kiso_docreader_mcp.docreader_runner."""
from __future__ import annotations

from pathlib import Path

import pytest

from kiso_docreader_mcp.docreader_runner import (
    check_health,
    document_info,
    list_supported_formats,
    read_document,
)


FIXTURES = Path(__file__).parent / "fixtures"


class TestReadPdf:
    def test_reads_sample_pdf(self):
        result = read_document(file_path=str(FIXTURES / "sample.pdf"))
        assert result["success"] is True
        assert result["format"] == "pdf"
        assert result["total_pages"] >= 1
        assert result["pages_returned"] >= 1

    def test_page_range(self):
        result = read_document(
            file_path=str(FIXTURES / "sample.pdf"), pages="1",
        )
        assert result["success"] is True
        assert result["pages_returned"] == 1

    def test_missing_pdf_fails(self, tmp_path):
        result = read_document(file_path=str(tmp_path / "missing.pdf"))
        assert result["success"] is False
        assert "not found" in result["stderr"].lower()


class TestReadDocx:
    def test_reads_sample_docx(self):
        result = read_document(file_path=str(FIXTURES / "sample.docx"))
        assert result["success"] is True
        assert result["format"] == "docx"
        assert isinstance(result["text"], str)
        assert result["total_chars"] >= 0


class TestReadXlsx:
    def test_reads_sample_xlsx(self):
        result = read_document(file_path=str(FIXTURES / "sample.xlsx"))
        assert result["success"] is True
        assert result["format"] == "xlsx"
        assert result["sheets"]


class TestReadCsv:
    def test_reads_sample_csv(self):
        result = read_document(file_path=str(FIXTURES / "sample.csv"))
        assert result["success"] is True
        assert result["format"] == "csv"
        assert result["total_rows"] >= 1
        assert result["columns"]


class TestReadText:
    def test_reads_sample_txt(self):
        result = read_document(file_path=str(FIXTURES / "sample.txt"))
        assert result["success"] is True
        assert result["format"] == "txt"
        assert isinstance(result["text"], str)

    def test_unknown_binary_ext_rejected(self, tmp_path):
        binary = tmp_path / "x.bin"
        binary.write_bytes(bytes(range(256)))
        result = read_document(file_path=str(binary))
        assert result["success"] is False
        assert "unsupported" in result["stderr"].lower()

    def test_unknown_text_ext_accepted_via_heuristic(self, tmp_path):
        weird = tmp_path / "notes.xyz"
        weird.write_text("plain ASCII content here\n")
        result = read_document(file_path=str(weird))
        assert result["success"] is True

    def test_large_text_truncates_at_newline(self, tmp_path):
        big = tmp_path / "big.txt"
        big.write_text("line\n" * 20_000)  # 100 000 chars
        result = read_document(file_path=str(big))
        assert result["success"] is True
        assert result["truncated"] is True
        assert result["shown_chars"] <= 50_000
        assert result["text"].endswith("line")


class TestParsePageRanges:
    def test_range_dash(self):
        from kiso_docreader_mcp.docreader_runner import _parse_page_ranges
        assert _parse_page_ranges("1-3", total=10) == [0, 1, 2]

    def test_mixed(self):
        from kiso_docreader_mcp.docreader_runner import _parse_page_ranges
        assert _parse_page_ranges("1,3-5,7", total=10) == [0, 2, 3, 4, 6]

    def test_reversed_range_is_auto_fixed(self):
        from kiso_docreader_mcp.docreader_runner import _parse_page_ranges
        assert _parse_page_ranges("5-2", total=10) == [1, 2, 3, 4]

    def test_out_of_bounds_clamped(self):
        from kiso_docreader_mcp.docreader_runner import _parse_page_ranges
        assert _parse_page_ranges("8-20", total=10) == [7, 8, 9]

    def test_invalid_raises(self):
        from kiso_docreader_mcp.docreader_runner import _parse_page_ranges
        with pytest.raises(ValueError, match="invalid page"):
            _parse_page_ranges("abc", total=10)


class TestDocumentInfo:
    def test_pdf_info(self):
        info = document_info(file_path=str(FIXTURES / "sample.pdf"))
        assert info["success"] is True
        assert info["format"] == "pdf"
        assert info["pages"] >= 1

    def test_xlsx_info(self):
        info = document_info(file_path=str(FIXTURES / "sample.xlsx"))
        assert info["success"] is True
        assert info["sheets"]

    def test_csv_info(self):
        info = document_info(file_path=str(FIXTURES / "sample.csv"))
        assert info["success"] is True
        assert info["rows"] >= 1

    def test_missing_file(self, tmp_path):
        info = document_info(file_path=str(tmp_path / "missing.pdf"))
        assert info["success"] is False


class TestListFormats:
    def test_lists_structured_and_text(self):
        formats = list_supported_formats()
        assert ".pdf" in formats["structured"]
        assert ".txt" in formats["text"]


class TestCheckHealth:
    def test_all_modules_importable(self):
        # In a normal dev environment all three modules are installed.
        h = check_health()
        assert h["healthy"] is True
        assert h["issues"] == []
