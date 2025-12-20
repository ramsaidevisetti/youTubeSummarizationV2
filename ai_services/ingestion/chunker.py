from typing import List, Dict

def chunk_transcript(
    transcript: List[Dict],
    max_words: int = 150
) -> List[Dict]:

    chunks = []
    current_words = []
    word_count = 0
    start_time = None

    for item in transcript:
        words = item["text"].split()

        if start_time is None:
            start_time = item["start"]

        current_words.extend(words)
        word_count += len(words)

        if word_count >= max_words:
            end_time = item["start"] + item["duration"]

            chunks.append({
                "text": " ".join(current_words),
                "start_time": round(start_time, 2),
                "end_time": round(end_time, 2)
            })

            current_words = []
            word_count = 0
            start_time = None

    if current_words:
        chunks.append({
            "text": " ".join(current_words),
            "start_time": round(start_time, 2),
            "end_time": round(start_time + 5, 2)
        })

    return chunks