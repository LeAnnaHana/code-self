import hashlib
import secrets
import logging
import json


def get_log_handler(level=logging.INFO):
    # Create a console handler and set the level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create a formatter and set the formatter for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    return console_handler


def generate_random_string(length=16):
    """
    Generates a random string of the specified length.
    """
    return secrets.token_hex(length // 2)  # Convert to bytes


def generate_request_id(max_length=32):
    """
    Generates a random string and hashes it using SHA-256.
    """
    random_string = generate_random_string()
    h = hashlib.sha256()
    h.update(random_string.encode('utf-8'))
    return h.hexdigest()[:max_length+1]


def extract_post_request(request):
    try:
        return json.loads(request.body.decode('utf-8'))
    except ValueError as err:
        logging.error(err)
        return {}
    

from typing import List
import re

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    text = re.sub(r'\s+', ' ', text.strip())
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:])
            break
        last_period = text.rfind('.', start, end)
        if last_period != -1 and last_period > start + chunk_size // 2:
            end = last_period + 1
        else:
            last_space = text.rfind(' ', start, end)
            if last_space != -1:
                end = last_space
        chunks.append(text[start:end].strip())
        start = end - overlap if end - overlap > start else end
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    return chunks

class TextChunker:
    @staticmethod
    def chunk_by_size(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        return chunk_text(text, chunk_size, overlap)
    
    @staticmethod
    def chunk_by_sentences(text: str, max_sentences: int = 5) -> List[str]:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) <= max_sentences:
            return [text]
        chunks = []
        current_chunk = []
        for sentence in sentences:
            current_chunk.append(sentence)
            if len(current_chunk) >= max_sentences:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        return chunks

# if __name__ == "__main__":
#     sample_text = """This is a long piece of text that needs to be split into 
#     smaller chunks. It contains multiple sentences. Each sentence should ideally 
#     be kept together. We don't want to split in the middle of a sentence."""
#     chunks = chunk_text(sample_text, chunk_size=100)
#     print("\nSimple chunking:")
#     for i, chunk in enumerate(chunks):
#         print(f"Chunk {i+1}: {chunk}")
#     chunker = TextChunker()
#     chunks = chunker.chunk_by_sentences(sample_text, max_sentences=2)
#     print("\nChunking by sentences:")
#     for i, chunk in enumerate(chunks):
#         print(f"Chunk {i+1}: {chunk}")


