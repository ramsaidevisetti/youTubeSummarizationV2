def retrieve_top_k(chunks: list, query: str, k: int = 5):
    query_words = set(query.lower().split())
    scored = []

    for chunk in chunks:
        chunk_words = set(chunk["text"].lower().split())
        score = len(query_words & chunk_words)
        scored.append((score, chunk))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [chunk for _, chunk in scored[:k]]