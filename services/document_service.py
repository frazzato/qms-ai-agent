import os
import re
import datetime
from dateutil.relativedelta import relativedelta
from docx import Document
from config.settings import DOCS_DIR

REVIEW_CYCLE_MONTHS = 6


def _extract_docx_metadata(filepath: str) -> dict:
    """
    Reads metadata from INSIDE a .docx file by scanning ALL tables.
    Handles two common QMS layouts:

    Layout 1 — Key-Value table (Document Control Information):
        | Field        | Details                              |
        | Version      | 3.0                                  |
        | Approved By  | James Carter, Director of Operations |
        | Revision Date| May 6, 2026                          |

    Layout 2 — Revision History table:
        | Version | Description | Date         | Author         |
        | 1.0     | Initial     | Jan 15, 2024 | Sarah Mitchell |
        | 3.0     | Update      | May 6, 2026  | Sarah Mitchell |
    """
    meta = {
        "revision":      None,
        "approved_by":   None,
        "approval_date": None,
        "reviewed_by":   None,
        "prepared_by":   None,
        "doc_number":    None,
    }

    try:
        doc = Document(filepath)
    except Exception:
        return meta

    # ─────────────────────────────────────
    # SCAN ALL TABLES
    # ─────────────────────────────────────
    for table in doc.tables:
        rows = table.rows
        if len(rows) < 2:
            continue

        # Get first row cells to determine table type
        first_row = [cell.text.strip() for cell in rows[0].cells]

        # ── Detect KEY-VALUE table (2 columns: Field | Details) ──
        if _is_key_value_table(first_row, rows):
            _parse_key_value_table(rows, meta)

        # ── Detect REVISION HISTORY table ──
        elif _is_revision_table(first_row):
            _parse_revision_table(rows, first_row, meta)

    return meta


def _is_key_value_table(first_row: list, rows) -> bool:
    """
    A key-value table typically has 2 columns and the left column
    contains known field labels like 'Version', 'Approved By', etc.
    """
    if len(first_row) < 2:
        return False

    known_labels = [
        "version", "revision", "approved by", "prepared by",
        "reviewed by", "document number", "revision date",
        "effective date", "field", "doc number", "document id",
    ]

    label_hits = 0
    for row in rows:
        cells = [c.text.strip().lower() for c in row.cells]
        if len(cells) >= 2:
            for label in known_labels:
                if label in cells[0]:
                    label_hits += 1

    return label_hits >= 2  # At least 2 recognized labels → key-value table


def _is_revision_table(first_row: list) -> bool:
    """
    A revision history table has headers like Version, Date, Author, etc.
    """
    headers_lower = [h.lower() for h in first_row]
    rev_keywords = ["version", "revision", "rev", "rev."]
    date_keywords = ["date", "effective date"]

    has_rev  = any(kw in h for h in headers_lower for kw in rev_keywords)
    has_date = any(kw in h for h in headers_lower for kw in date_keywords)

    return has_rev and has_date


def _parse_key_value_table(rows, meta: dict):
    """
    Parse a 2-column key-value table.
    Reads every row as:  label (col 0)  →  value (col 1)
    """
    FIELD_MAP = {
        "version":          "revision",
        "revision":         "revision",
        "rev":              "revision",
        "approved by":      "approved_by",
        "approval authority": "approved_by",
        "authorized by":    "approved_by",
        "reviewed by":      "reviewed_by",
        "prepared by":      "prepared_by",
        "revision date":    "approval_date",
        "effective date":   "approval_date",
        "date approved":    "approval_date",
        "date":             "approval_date",
        "document number":  "doc_number",
        "doc number":       "doc_number",
        "document id":      "doc_number",
    }

    for row in rows:
        cells = [c.text.strip() for c in row.cells]
        if len(cells) < 2 or not cells[1]:
            continue

        label = cells[0].lower().rstrip(":")
        value = cells[1].strip()

        for key_pattern, meta_key in FIELD_MAP.items():
            if key_pattern in label:
                # Don't overwrite with empty values
                if not value:
                    break

                if meta_key == "approval_date":
                    parsed = _parse_date(value)
                    if parsed:
                        meta[meta_key] = parsed
                elif meta_key == "revision":
                    # Store as-is from the document (e.g., "3.0")
                    meta[meta_key] = value
                else:
                    meta[meta_key] = value
                break


def _parse_revision_table(rows, headers: list, meta: dict):
    """
    Parse a revision history table. Reads the LAST data row
    (= most recent revision).
    """
    headers_lower = [h.lower() for h in headers]

    # Find column indices
    ver_idx    = _find_col(headers_lower, ["version", "revision", "rev", "rev."])
    date_idx   = _find_col(headers_lower, ["date", "effective date", "revision date"])
    author_idx = _find_col(headers_lower, ["author", "revised by", "approved by",
                                            "changed by", "updated by"])

    if len(rows) < 2:
        return

    # Read the LAST data row (most recent revision)
    last_row = [c.text.strip() for c in rows[-1].cells]

    # Only use revision history as FALLBACK
    # (key-value table takes priority)
    if ver_idx is not None and not meta["revision"]:
        val = last_row[ver_idx] if ver_idx < len(last_row) else ""
        if val:
            meta["revision"] = val

    if date_idx is not None and not meta["approval_date"]:
        val = last_row[date_idx] if date_idx < len(last_row) else ""
        parsed = _parse_date(val)
        if parsed:
            meta["approval_date"] = parsed

    # Note: Author in revision history ≠ Approver
    # We do NOT set approved_by from here


def _find_col(headers: list, keywords: list) -> int | None:
    """Find column index matching any keyword."""
    for i, h in enumerate(headers):
        for kw in keywords:
            if kw in h:
                return i
    return None


def _parse_date(text: str) -> datetime.date | None:
    """Try multiple date formats commonly used in QMS docs."""
    if not text:
        return None
    text = text.strip()
    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%B %d, %Y",     # May 6, 2026
        "%b %d, %Y",     # May 6, 2026 (short month)
        "%d-%b-%Y",       # 06-May-2026
        "%d %B %Y",       # 06 May 2026
        "%b. %d, %Y",     # May. 6, 2026
        "%m-%d-%Y",
    ]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def _calculate_status(next_review: datetime.date) -> str:
    today = datetime.date.today()
    days_until = (next_review - today).days
    if days_until < 0:
        return "Overdue"
    elif days_until <= 30:
        return "Review Soon"
    return "Active"


def scan_documents():
    """
    Scans DOCS_DIR. For .docx files, reads metadata from INSIDE the document.
    Returns: (docs_list, filenames_list)
    """
    docs = []
    files = []

    if not os.path.exists(DOCS_DIR):
        return docs, files

    for file in sorted(os.listdir(DOCS_DIR)):
        if file.startswith('.') or file == ".keep":
            continue

        files.append(file)
        filepath = os.path.join(DOCS_DIR, file)

        name_no_ext = file.rsplit('.', 1)[0]
        ext = file.rsplit('.', 1)[-1].upper() if '.' in file else "N/A"

        # ── Parse Document ID and Title from filename ──
        if " - " in name_no_ext:
            doc_id, title = name_no_ext.split(" - ", 1)
            title = re.sub(r'\s*[Rr]ev\s*[A-Za-z0-9]+', '', title).strip() or title
        else:
            doc_id, title = "N/A", name_no_ext

        # ── File system date as last resort fallback ──
        stat = os.stat(filepath)
        file_mod_date = datetime.date.fromtimestamp(stat.st_mtime)

        # ── Extract from inside the Word doc ──
        if ext == "DOCX":
            meta = _extract_docx_metadata(filepath)
        else:
            meta = {
                "revision": None, "approved_by": None,
                "approval_date": None, "doc_number": None,
            }

        # ── Use doc_number from inside doc if available ──
        if meta.get("doc_number"):
            doc_id = meta["doc_number"]

        # ── Build final values with fallbacks ──
        revision      = meta["revision"]      or "—"
        approved_by   = meta["approved_by"]   or "—"
        approval_date = meta["approval_date"] or file_mod_date
        next_review   = approval_date + relativedelta(months=REVIEW_CYCLE_MONTHS)
        status        = _calculate_status(next_review)

        docs.append({
            "Document ID":   doc_id,
            "Title":         title,
            "Format":        ext,
            "Revision":      revision,
            "Approved By":   approved_by,
            "Approval Date": approval_date.strftime('%Y-%m-%d'),
            "Next Review":   next_review.strftime('%Y-%m-%d'),
            "Status":        status,
        })

    return docs, files
