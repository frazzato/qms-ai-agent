import os
import re
import datetime
from dateutil.relativedelta import relativedelta
from docx import Document
from config.settings import DOCS_DIR

REVIEW_CYCLE_MONTHS = 6


def _extract_docx_metadata(filepath: str) -> dict:
    """
    Reads metadata from inside a .docx file.
    Tries two sources:
      1. Built-in document properties (core_properties)
      2. First table in the doc (common QMS approval block)
    """
    meta = {
        "revision":      None,
        "approved_by":   None,
        "approval_date": None,
    }

    try:
        doc = Document(filepath)
        props = doc.core_properties

        # ── Source 1: Built-in properties ──
        # "last_modified_by" is often the approver in controlled docs
        if props.last_modified_by:
            meta["approved_by"] = props.last_modified_by

        # Built-in revision number (Word tracks this automatically)
        if props.revision:
            meta["revision"] = f"Rev {props.revision}"

        # Version field (if manually set in File > Properties)
        if props.version:
            meta["revision"] = props.version

        # Modified date as fallback approval date
        if props.modified:
            meta["approval_date"] = props.modified.date()

        # ── Source 2: First table (QMS approval block) ──
        # Many AS9100 docs have a table like:
        # | Revision | Approved By    | Date       |
        # | Rev C    | Marcelo F.     | 2025-11-01 |
        if doc.tables:
            table = doc.tables[0]
            headers = [
                cell.text.strip().lower()
                for cell in table.rows[0].cells
            ]

            # Find column indices by common header names
            rev_keys      = ["revision", "rev", "version", "rev."]
            approver_keys = ["approved by", "approver", "approved",
                             "approval authority", "authorized by"]
            date_keys     = ["date", "approval date", "effective date",
                             "date approved"]

            rev_idx      = _find_column(headers, rev_keys)
            approver_idx = _find_column(headers, approver_keys)
            date_idx     = _find_column(headers, date_keys)

            # Read the LAST data row (most recent revision)
            if len(table.rows) > 1:
                last_row = table.rows[-1].cells

                if rev_idx is not None:
                    val = last_row[rev_idx].text.strip()
                    if val:
                        meta["revision"] = val

                if approver_idx is not None:
                    val = last_row[approver_idx].text.strip()
                    if val:
                        meta["approved_by"] = val

                if date_idx is not None:
                    val = last_row[date_idx].text.strip()
                    parsed = _parse_date(val)
                    if parsed:
                        meta["approval_date"] = parsed

    except Exception:
        # Not a valid docx, or no table — fall back gracefully
        pass

    return meta


def _find_column(headers: list, keywords: list) -> int | None:
    """Find the index of a column whose header matches any keyword."""
    for i, h in enumerate(headers):
        for kw in keywords:
            if kw in h:
                return i
    return None


def _parse_date(text: str) -> datetime.date | None:
    """Try multiple date formats commonly used in QMS docs."""
    formats = [
        "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y",
        "%B %d, %Y", "%b %d, %Y",
        "%d-%b-%Y", "%d %B %Y",
    ]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(text.strip(), fmt).date()
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

        # ── Parse Document ID and Title from filename ──
        if " - " in name_no_ext:
            doc_id, title = name_no_ext.split(" - ", 1)
            title = re.sub(r'\s*[Rr]ev\s*[A-Za-z0-9]+', '', title).strip() or title
        else:
            doc_id, title = "N/A", name_no_ext

        # ── File system dates as fallback ──
        stat = os.stat(filepath)
        mod_date = datetime.date.fromtimestamp(stat.st_mtime)

        # ── Extract metadata from inside the Word doc ──
        if ext in ("DOCX", "DOC"):
            meta = _extract_docx_metadata(filepath)
        else:
            meta = {"revision": None, "approved_by": None, "approval_date": None}

        # ── Use extracted values, with fallbacks ──
        revision      = meta["revision"]      or "Rev A"
        approved_by   = meta["approved_by"]   or "—"
        approval_date = meta["approval_date"] or mod_date

        # ── Next review = approval + 6 months ──
        next_review = approval_date + relativedelta(months=REVIEW_CYCLE_MONTHS)
        status = _calculate_status(next_review)

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
