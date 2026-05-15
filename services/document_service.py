import os
import re
import datetime
from dateutil.relativedelta import relativedelta
from docx import Document
from config.settings import DOCS_DIR

REVIEW_CYCLE_MONTHS = 6


def _extract_docx_metadata(filepath: str) -> dict:
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

    for table in doc.tables:
        rows = table.rows
        if len(rows) < 2:
            continue

        first_row = [cell.text.strip() for cell in rows[0].cells]

        if _is_key_value_table(rows):
            _parse_key_value_table(rows, meta)
        elif _is_revision_table(first_row):
            _parse_revision_table(rows, first_row, meta)

    return meta


def _is_key_value_table(rows) -> bool:
    known_labels = [
        "version", "revision", "approved by", "prepared by",
        "reviewed by", "document number", "revision date",
        "effective date", "field", "doc number", "document id",
    ]

    label_hits = 0
    for row in rows:
        cells = [c.text.strip().lower() for c in row.cells]
        if len(cells) >= 2 and cells[0]:
            for label in known_labels:
                if label in cells[0]:
                    label_hits += 1
                    break

    return label_hits >= 2


def _is_revision_table(first_row: list) -> bool:
    headers_lower = [h.lower() for h in first_row]
    rev_keywords = ["version", "revision", "rev", "rev."]
    date_keywords = ["date", "effective date"]

    has_rev  = any(kw in h for h in headers_lower for kw in rev_keywords)
    has_date = any(kw in h for h in headers_lower for kw in date_keywords)

    return has_rev and has_date


def _parse_key_value_table(rows, meta: dict):
    """
    Parse a 2-column key-value table.
    CRITICAL: patterns sorted LONGEST FIRST so
    'revision date' matches before 'revision'.
    """
    FIELD_MAP = [
        # ── Date fields (MUST be checked before shorter matches) ──
        ("revision date",      "approval_date"),
        ("effective date",     "approval_date"),
        ("date approved",      "approval_date"),
        # ── Multi-word fields ──
        ("approval authority", "approved_by"),
        ("document number",    "doc_number"),
        ("document id",        "doc_number"),
        ("doc number",         "doc_number"),
        ("approved by",        "approved_by"),
        ("authorized by",      "approved_by"),
        ("reviewed by",        "reviewed_by"),
        ("prepared by",        "prepared_by"),
        # ── Short fields (checked LAST) ──
        ("version",            "revision"),
        ("revision",           "revision"),
        ("rev",                "revision"),
    ]

    for row in rows:
        cells = [c.text.strip() for c in row.cells]
        if len(cells) < 2 or not cells[0]:
            continue

        label = cells[0].lower().rstrip(":")
        value = cells[1].strip()

        if not value:
            continue

        for key_pattern, meta_key in FIELD_MAP:
            if key_pattern in label:
                if meta_key == "approval_date":
                    parsed = _parse_date(value)
                    if parsed:
                        meta[meta_key] = parsed
                elif meta_key == "revision":
                    meta[meta_key] = _clean_revision(value)
                else:
                    meta[meta_key] = value
                break


def _parse_revision_table(rows, headers: list, meta: dict):
    headers_lower = [h.lower() for h in headers]

    ver_idx  = _find_col(headers_lower, ["version", "revision", "rev", "rev."])
    date_idx = _find_col(headers_lower, ["date", "effective date", "revision date"])

    if len(rows) < 2:
        return

    last_row = [c.text.strip() for c in rows[-1].cells]

    if ver_idx is not None and not meta["revision"]:
        val = last_row[ver_idx] if ver_idx < len(last_row) else ""
        if val:
            meta["revision"] = _clean_revision(val)

    if date_idx is not None and not meta["approval_date"]:
        val = last_row[date_idx] if date_idx < len(last_row) else ""
        parsed = _parse_date(val)
        if parsed:
            meta["approval_date"] = parsed


def _clean_revision(raw: str) -> str:
    """
    Extracts ONLY the revision number or letter.

    '3.0'         → '3.0'
    'Rev C'       → 'C'
    'Revision 5'  → '5'
    'v2.1'        → '2.1'
    'Rev. B'      → 'B'
    'A'           → 'A'
    """
    if not raw:
        return "—"

    text = raw.strip()

    # Remove prefixes: Revision, Version, Rev., Rev, Ver., Ver
    text = re.sub(
        r'^(?:revision|version|ver|rev)\.?\s*',
        '',
        text,
        flags=re.IGNORECASE,
    ).strip()

    # Remove leading v/V before a digit (v2.1 → 2.1)
    text = re.sub(r'^[vV](?=\d)', '', text).strip()

    return text if text else "—"


def _find_col(headers: list, keywords: list):
    for i, h in enumerate(headers):
        for kw in keywords:
            if kw in h:
                return i
    return None


def _parse_date(text: str):
    if not text:
        return None
    text = text.strip()
    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d-%b-%Y",
        "%d %B %Y",
        "%b. %d, %Y",
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

        if " - " in name_no_ext:
            doc_id, title = name_no_ext.split(" - ", 1)
            title = re.sub(r'\s*[Rr]ev\s*[A-Za-z0-9]+', '', title).strip() or title
        else:
            doc_id, title = "N/A", name_no_ext

        stat = os.stat(filepath)
        file_mod_date = datetime.date.fromtimestamp(stat.st_mtime)

        if ext == "DOCX":
            meta = _extract_docx_metadata(filepath)
        else:
            meta = {
                "revision": None, "approved_by": None,
                "approval_date": None, "doc_number": None,
            }

        if meta.get("doc_number"):
            doc_id = meta["doc_number"]

        revision      = meta.get("revision")      or "—"
        approved_by   = meta.get("approved_by")   or "—"
        approval_date = meta.get("approval_date") or file_mod_date
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
