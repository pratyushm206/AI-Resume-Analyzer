"""Print raw and calibrated Gemini embedding cosine scores for text pairs.

Usage: python scripts/calibrate_semantic.py [pairs.json]
Set GEMINI_API_KEY and optionally GEMINI_EMBEDDING_MODEL, SEMANTIC_FLOOR,
and SEMANTIC_CEILING in the environment (or .env).
"""
import json
import sys
from pathlib import Path

# Ensure invoking this script by path also imports repo-root modules.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai_engine import cosine_similarity, embed_texts, rescale_semantic_similarity


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("semantic_calibration_examples.json")
    pairs = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(pairs, list):
        raise ValueError("Calibration JSON must contain a list of text pair objects")

    for pair in pairs:
        a, b = pair["text_a"], pair["text_b"]
        vector_a, vector_b = embed_texts([a, b])
        raw = cosine_similarity(vector_a, vector_b)
        scaled = rescale_semantic_similarity(raw)
        print(f"{pair.get('label', '(unlabeled)')}: raw cosine={raw:.4f}, rescaled={scaled:.2f}")


if __name__ == "__main__":
    main()
