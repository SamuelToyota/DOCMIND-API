from pathlib import Path


def extract_text_from_document(document):
    extension = Path(document.file.name).suffix.lower()

    if extension != ".txt":
        return ""

    document.file.open("rb")

    try:
        content = document.file.read().decode("utf-8", errors="ignore")
    finally:
        document.file.close()

    return content.strip()


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
