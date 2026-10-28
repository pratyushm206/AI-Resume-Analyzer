import math
import os
import re
from collections import Counter
from functools import lru_cache

import numpy as np

from llm_utils import run_with_timeout
from secrets_config import get_secret

DEFAULT_EMBEDDING_MODEL = "gemini-embedding-001"
DEFAULT_SEMANTIC_FLOOR = 0.55
DEFAULT_SEMANTIC_CEILING = 0.90


def cosine_similarity(left, right) -> float:
    """Return cosine similarity for two vectors, or zero for empty vectors."""
    a = np.asarray(left, dtype=float).reshape(-1)
    b = np.asarray(right, dtype=float).reshape(-1)
    if a.size == 0 or a.size != b.size:
        return 0.0
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if not denom:
        return 0.0
    return float(np.dot(a, b) / denom)


def rescale_semantic_similarity(similarity: float) -> float:
    """Map raw embedding cosine similarity to a clipped 0–100 score."""
    floor = float(os.getenv("SEMANTIC_FLOOR", DEFAULT_SEMANTIC_FLOOR))
    ceiling = float(os.getenv("SEMANTIC_CEILING", DEFAULT_SEMANTIC_CEILING))
    if ceiling <= floor:
        raise ValueError("SEMANTIC_CEILING must be greater than SEMANTIC_FLOOR")
    return max(0.0, min(1.0, (float(similarity) - floor) / (ceiling - floor))) * 100


def _term_frequency_cosine(left: str, right: str) -> float:
    """Pure Python cosine similarity over lowercase word frequencies."""
    tokenize = lambda value: re.findall(r"\b\w+\b", (value or "").lower())
    a, b = Counter(tokenize(left)), Counter(tokenize(right))
    if not a or not b:
        return 0.0
    dot = sum(count * b.get(term, 0) for term, count in a.items())
    denom = math.sqrt(sum(n * n for n in a.values()) * sum(n * n for n in b.values()))
    return dot / denom if denom else 0.0


@lru_cache(maxsize=1)
def _get_client(api_key: str):
    from google import genai
    return genai.Client(api_key=api_key)


def _embedding_values(response):
    embeddings = getattr(response, "embeddings", None)
    if not embeddings or len(embeddings) < 1:
        raise ValueError("Embedding response contained no vectors")
    return [embedding.values for embedding in embeddings]


def embed_texts(texts):
    """Embed multiple texts in one Gemini request; return vectors in input order."""
    key = get_secret("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not configured")
    client = _get_client(key)
    model = os.getenv("GEMINI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
    response = run_with_timeout(
        lambda: client.models.embed_content(model=model, contents=list(texts))
    )
    vectors = _embedding_values(response)
    if len(vectors) != len(texts):
        raise ValueError("Embedding response vector count did not match input count")
    return vectors


def calculate_match_score(resume_text, job_description):
    try:
        resume_embedding, jd_embedding = embed_texts([resume_text, job_description])
        similarity = cosine_similarity(resume_embedding, jd_embedding)
        return round(rescale_semantic_similarity(similarity), 2)
    except Exception:
        similarity = _term_frequency_cosine(resume_text, job_description)
    return round(max(0.0, min(1.0, similarity)) * 100, 2)
