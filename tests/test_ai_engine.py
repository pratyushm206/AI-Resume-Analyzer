import ai_engine


def test_cosine_similarity():
    assert ai_engine.cosine_similarity([1, 0], [1, 0]) == 1.0
    assert ai_engine.cosine_similarity([1, 0], [0, 1]) == 0.0


def test_falls_back_when_embedding_api_raises(monkeypatch):
    monkeypatch.setattr(ai_engine, "embed_texts", lambda _texts: (_ for _ in ()).throw(RuntimeError("offline")))
    assert ai_engine.calculate_match_score("python python developer", "python role") == 63.25

