from io import BytesIO
from pathlib import Path
import re


EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
PHONE_PATTERN = (
    r"(?<!\d)"
    r"(?:\+?55[\s.-]*)?"
    r"\(?\d{2}\)?[\s.-]*"
    r"\d{4,5}[\s.-]*\d{4}"
    r"(?!\d)"
)


def extract_emails(text):
    emails = re.findall(EMAIL_PATTERN, text)

    normalized_emails = {
        email.lower()
        for email in emails
    }

    return sorted(normalized_emails)


def extract_phones(text):
    phones = re.findall(PHONE_PATTERN, text)

    normalized_phones = {
        re.sub(r"\D", "", phone)
        for phone in phones
    }

    return sorted(normalized_phones)


def extract_text_from_docx(file):
    from docx import Document as WordDocument

    file.open("rb")

    try:
        content = file.read()
    finally:
        file.close()

    document = WordDocument(BytesIO(content))
    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n\n".join(paragraphs).strip()


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
        return extract_text_from_docx(document.file)

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


