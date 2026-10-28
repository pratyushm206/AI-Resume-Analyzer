import ai_engine


def test_cosine_similarity():
    assert ai_engine.cosine_similarity([1, 0], [1, 0]) == 1.0
    assert ai_engine.cosine_similarity([1, 0], [0, 1]) == 0.0


def test_rescale_boundaries_and_clipping(monkeypatch):
    monkeypatch.setenv("SEMANTIC_FLOOR", "0.55")
    monkeypatch.setenv("SEMANTIC_CEILING", "0.90")
    assert ai_engine.rescale_semantic_similarity(0.55) == 0
    assert ai_engine.rescale_semantic_similarity(0.90) == 100
    assert ai_engine.rescale_semantic_similarity(0.40) == 0
    assert ai_engine.rescale_semantic_similarity(0.95) == 100


def test_falls_back_when_embedding_api_raises(monkeypatch):
    monkeypatch.setattr(ai_engine, "embed_texts", lambda _texts: (_ for _ in ()).throw(RuntimeError("offline")))
    monkeypatch.setenv("SEMANTIC_FLOOR", "0.0")
    monkeypatch.setenv("SEMANTIC_CEILING", "0.01")
    score = ai_engine.calculate_match_score("python python developer", "python role")
    assert score == 63.25

