from FlagEmbedding import FlagReranker

reranker = FlagReranker("BAAI/bge-reranker-base", use_fp16=True)


def rerank(query: str, docs: list[str], k: int = 5) -> list[str]:
    pairs = [(query, doc) for doc in docs]
    scores = reranker.compute_score(pairs, normalize=True)
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in ranked[:k]]
