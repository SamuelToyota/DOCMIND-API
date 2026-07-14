from io import BytesIO
from pathlib import Path


def extract_text_from_pdf(file):
    from pypdf import PdfReader

    file.open("rb")

    try:
        content = file.read()
    finally:
        file.close()

    reader = PdfReader(BytesIO(content))
    pages_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages_text.append(text.strip())

    return "\n\n".join(pages_text).strip()


def extract_text_from_document(document):
    extension = Path(document.file.name).suffix.lower()

    if extension == ".txt":
        document.file.open("rb")

        try:
            content = document.file.read().decode("utf-8", errors="ignore")
        finally:
            document.file.close()

        return content.strip()

    if extension == ".pdf":
        return extract_text_from_pdf(document.file)

    if extension == ".docx":
        return ""

    return ""


def split_text_into_chunks(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
