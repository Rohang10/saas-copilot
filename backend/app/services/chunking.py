def chunk_text(text: str, chunk_size=300, overlap=50):
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append((chunk_id, chunk))
        start += chunk_size - overlap
        chunk_id += 1

    return chunks
