import sys
import types

import numpy as np


class FakeEmbedding:
    def __init__(self, values):
        self.values = values


class FakeModels:
    def __init__(self):
        self.embedding_calls = []

    def generate_content(self, *_args, **_kwargs):
        return types.SimpleNamespace(text="{}")

    def embed_content(self, *, model, contents, **_kwargs):
        self.embedding_calls.append((model, list(contents)))
        vectors = []
        for text in contents:
            tokens = (text or "").lower().split()
            vectors.append(FakeEmbedding([
                float(len(text or "")),
                float(sum(ord(ch) for ch in (text or "")) % 997),
                float(len(set(tokens))),
            ]))
        return types.SimpleNamespace(embeddings=vectors)


class FakeClient:
    def __init__(self, *_args, **_kwargs):
        self.models = FakeModels()


google = types.ModuleType("google")
genai = types.ModuleType("google.genai")
genai.Client = FakeClient
google.genai = genai
sys.modules.setdefault("google", google)
sys.modules.setdefault("google.genai", genai)
