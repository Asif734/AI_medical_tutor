from typing import List


def chunk_text(text: str, max_words: int= 700, overlap_words: int= 50) -> List[str]:
    words= text.split()
    chunks=[]
    i=0

    while i<len(words):
        chunk= words[i:i+max_words]

        chunks.append(" ".join(chunk))
        i+= max_words - overlap_words
    return chunks

