import sys
import types

import numpy as np


class FakeSentenceTransformer:
    def __init__(self, *_args, **_kwargs):
        pass

    def encode(self, texts):
        rows = []
        for text in texts:
            text = text or ""
            rows.append([
                float(len(text)),
                float(sum(ord(ch) for ch in text) % 997),
                float(len(set(text.lower().split()))),
            ])
        return np.array(rows)


sentence_transformers = types.ModuleType("sentence_transformers")
sentence_transformers.SentenceTransformer = FakeSentenceTransformer
sys.modules.setdefault("sentence_transformers", sentence_transformers)


class FakeModels:
    def generate_content(self, *_args, **_kwargs):
        return types.SimpleNamespace(text="{}")


class FakeClient:
    def __init__(self, *_args, **_kwargs):
        self.models = FakeModels()


google = types.ModuleType("google")
genai = types.ModuleType("google.genai")
genai.Client = FakeClient
google.genai = genai
sys.modules.setdefault("google", google)
sys.modules.setdefault("google.genai", genai)
