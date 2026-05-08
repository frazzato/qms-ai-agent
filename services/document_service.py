import os
import datetime
from config.settings import DOCS_DIR

def scan_documents():
    docs = []
    files = []

    if not os.path.exists(DOCS_DIR):
        return docs, files

    for file in os.listdir(DOCS_DIR):
        if file.startswith('.') or file == ".keep":
            continue

        files.append(file)

        name_no_ext = file.rsplit('.', 1)[0]
        ext = file.rsplit('.', 1)[1].upper()

        if " - " in name_no_ext:
            doc_id, title = name_no_ext.split(" - ", 1)
        else:
            doc_id, title = "N/A", name_no_ext

        stat = os.stat(os.path.join(DOCS_DIR, file))
        mod_date = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')

        docs.append({
            "Document ID": doc_id,
            "Title": title,
            "Format": ext,
            "Status": "Active Control",
            "Last Sync Date": mod_date
        })

    return docs, files
